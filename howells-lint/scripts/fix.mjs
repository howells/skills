// Usage: node lintfix.mjs <repo-abs-path>. Rewrites configs/deps in place, prints touched paths. No git, no install.
import { readdirSync, readFileSync, writeFileSync, existsSync, renameSync, unlinkSync } from "node:fs";
import { join, relative } from "node:path";
import { execSync } from "node:child_process";
const repo = process.argv[2];
const LATEST = "^3.3.2";
const touched = new Set();
const skip = new Set(["node_modules", ".git", ".next", "dist", ".turbo", "build", "coverage", ".worktrees", "docs"]);
const pkgDirs = [];
const walk = (d, depth) => { if (depth > 3) return; let ents; try { ents = readdirSync(d, { withFileTypes: true }); } catch { return; }
  if (ents.some(e => e.name === "package.json")) pkgDirs.push(d);
  for (const e of ents) if (e.isDirectory() && !skip.has(e.name) && !e.name.startsWith(".")) walk(join(d, e.name), depth + 1); };
walk(repo, 0);
const rel = p => relative(repo, p) || ".";
const tpl = preset => `import ${preset} from "@howells/lint/oxlint/${preset}";\n\nexport default {\n  extends: [${preset}],\n};\n`;

// 1. catalog + deps
const wsy = join(repo, "pnpm-workspace.yaml");
if (existsSync(wsy)) { let s = readFileSync(wsy, "utf8"); const n = s.replace(/("?@howells\/lint"?:\s*)"?[^\n"]+"?/g, `$1"${LATEST}"`); if (n !== s) { writeFileSync(wsy, n); touched.add(rel(wsy)); } }
for (const d of pkgDirs) {
  const pjPath = join(d, "package.json"); const pj = JSON.parse(readFileSync(pjPath, "utf8")); let changed = false;
  for (const field of ["dependencies", "devDependencies"]) { const deps = pj[field]; if (!deps) continue;
    for (const k of Object.keys(deps)) if (/^@howells\/lint-policy-v\d$/.test(k)) { delete deps[k]; deps["@howells/lint"] = LATEST; changed = true; }
    if ("@howells/lint" in deps && deps["@howells/lint"] !== "catalog:" && deps["@howells/lint"] !== LATEST) { deps["@howells/lint"] = LATEST; changed = true; }
    if ("@howells/lint" in deps) deps["@howells/lint"] === "catalog:" || (deps["@howells/lint"] = LATEST);
  }
  if (changed) { writeFileSync(pjPath, JSON.stringify(pj, null, 2) + "\n"); touched.add(rel(pjPath)); }
}
// 2. import specifiers for policy packages
const files = execSync(`rg -l --no-messages "@howells/lint-policy-v\\d" ${repo} -g '!node_modules' -g '!pnpm-lock.yaml' -g '!*.md' || true`, { encoding: "utf8" }).split("\n").filter(Boolean);
for (const f of files) { const s = readFileSync(f, "utf8"); const n = s.replace(/@howells\/lint-policy-v\d/g, "@howells/lint"); if (n !== s) { writeFileSync(f, n); touched.add(rel(f)); } }
// 3. configs
const rootHasLint = (() => { const pj = JSON.parse(readFileSync(join(repo, "package.json"), "utf8")); return "@howells/lint" in { ...pj.dependencies, ...pj.devDependencies }; })();
for (const d of pkgDirs) {
  const pj = JSON.parse(readFileSync(join(d, "package.json"), "utf8")); const deps = { ...pj.dependencies, ...pj.devDependencies };
  const preset = "next" in deps ? "next" : "react" in deps ? "react" : "core";
  // Only the spellings that act as this package's own config. A named rc such as
  // `.oxlintrc.barrels.json` belongs to a script that loads it by path; leave it.
  const names = readdirSync(d).filter(n => /^oxlint\.config\.|^\.oxlintrc\.jsonc?$/.test(n));
  const ts = names.find(n => /^oxlint\.config\.(ts|mts)$/.test(n));
  const bad = names.filter(n => !/^oxlint\.config\.(ts|mts)$/.test(n));
  if (ts) { const src = readFileSync(join(d, ts), "utf8"); if (!/@howells\/lint/.test(src)) console.log(`REVIEW ${rel(d)}/${ts}: does not import @howells/lint`); }
  for (const b of bad) {
    const from = join(d, b);
    if (ts) { unlinkSync(from); touched.add(rel(from)); console.log(`removed duplicate ${rel(from)}`); continue; }
    if (/\.mjs$/.test(b)) { const src = readFileSync(from, "utf8"); const to = join(d, "oxlint.config.ts");
      if (/@howells\/lint/.test(src)) { execSync(`git -C ${repo} mv "${from}" "${to}"`); } else { unlinkSync(from); writeFileSync(to, tpl(preset)); console.log(`replaced hand-rolled ${rel(from)} with ${preset}`); }
      touched.add(rel(from)); touched.add(rel(to)); }
    else { unlinkSync(from); writeFileSync(join(d, "oxlint.config.ts"), tpl(preset)); touched.add(rel(from)); touched.add(rel(join(d, "oxlint.config.ts"))); console.log(`replaced ${rel(from)} with ${preset}`); }
  }
  if (!ts && bad.length === 0) {
    const isRoot = d === repo; const wantsConfig = isRoot ? rootHasLint : (("@howells/lint" in deps) || rootHasLint);
    if (wantsConfig) { writeFileSync(join(d, "oxlint.config.ts"), tpl(preset)); touched.add(rel(join(d, "oxlint.config.ts"))); console.log(`created ${rel(d)}/oxlint.config.ts (${preset})`); }
  }
}
// 4. node version
const nv = join(repo, ".node-version"); const cur = existsSync(nv) ? readFileSync(nv, "utf8").trim() : "";
if (!cur || cur.localeCompare("24.15.0", undefined, { numeric: true }) < 0) { writeFileSync(nv, "24.15.0\n"); touched.add(".node-version"); console.log(`node-version ${cur || "none"} -> 24.15.0`); }
console.log("TOUCHED " + [...touched].sort().join(" "));
