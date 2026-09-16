import { readdirSync, readFileSync, existsSync, statSync } from "node:fs";
import { join } from "node:path";
const root = process.argv[2] ?? `${process.env.HOME}/Sites`;
const skip = new Set(["node_modules", ".git", ".next", "dist", ".turbo", ".worktrees", "build", "coverage"]);
const pkgs = [];
const walk = (d, depth) => {
  if (depth > 4) return;
  let ents; try { ents = readdirSync(d, { withFileTypes: true }); } catch { return; }
  if (ents.some(e => e.name === "package.json")) pkgs.push(d);
  for (const e of ents) if (e.isDirectory() && !skip.has(e.name) && !e.name.startsWith(".")) walk(join(d, e.name), depth + 1);
};
walk(root, 0);
const rows = [];
for (const d of pkgs) {
  let pj; try { pj = JSON.parse(readFileSync(join(d, "package.json"), "utf8")); } catch { continue; }
  const deps = { ...pj.dependencies, ...pj.devDependencies };
  const usesLint = "@howells/lint" in deps;
  const names = readdirSync(d).filter(n => /^oxlint\.config\./.test(n) || n === ".oxlintrc.json");
  const lintScript = pj.scripts?.lint ?? "";
  const hasReact = "react" in deps; const hasNext = "next" in deps;
  if (!usesLint && names.length === 0) continue;
  const issues = [];
  const good = names.filter(n => /\.(ts|mts)$/.test(n));
  const bad = names.filter(n => !/\.(ts|mts)$/.test(n));
  let extendsWhat = "";
  for (const n of good) {
    const src = readFileSync(join(d, n), "utf8");
    const imp = src.match(/from\s+["']@howells\/lint([^"']*)["']/g) || [];
    for (const i of imp) { const sub = i.match(/@howells\/lint([^"']*)/)[1]; if (sub && !existsSync(join(d, "node_modules/@howells/lint", sub)) && !existsSync(join(d, "node_modules/@howells/lint", sub + ".mjs")) && !existsSync(join(d, "node_modules/@howells/lint", sub + ".js"))) issues.push(`imports @howells/lint${sub} (missing)`); }
    const ext = src.match(/extends:\s*\[([^\]]*)\]/); extendsWhat = ext ? ext[1].replace(/\s+/g, "") : (/@howells\/lint/.test(src) ? "no-extends" : "no-howells");
    if (extendsWhat === "no-howells") issues.push("config does not import @howells/lint");
    if (/\bjsx\b|\bJSX\b|"jsx-a11y"|plugins/.test(src) && !/extends/.test(src)) {}
    if (hasNext && !/next/.test(extendsWhat) && extendsWhat !== "no-howells") issues.push(`next app extends ${extendsWhat}`);
    else if (hasReact && !hasNext && !/react|next/.test(extendsWhat) && extendsWhat !== "no-howells") issues.push(`react pkg extends ${extendsWhat}`);
  }
  if (bad.length) issues.push(`config never loads: ${bad.join(",")}`);
  if (usesLint && names.length === 0) {
    // is there a config above it (monorepo root)?
    let up = d, found = false; while (up.startsWith(root) && up !== root) { up = join(up, ".."); if (readdirSync(up).some(n => /^oxlint\.config\.(ts|mts)$/.test(n))) { found = true; break; } if (readdirSync(up).some(n => /^oxlint\.config\./.test(n))) { issues.push(`inherits a config that never loads at ${up.replace(root + "/", "")}`); found = true; break; } }
    if (!found) issues.push("no oxlint config anywhere");
  }
  if (/--config/.test(lintScript)) issues.push("lint script passes --config");
  if (usesLint && !/howells-check|oxlint/.test(lintScript) && !pj.workspaces && !existsSync(join(d, "pnpm-workspace.yaml"))) issues.push(`lint script: ${lintScript || "(none)"}`);
  rows.push({ d: d.replace(root + "/", ""), v: deps["@howells/lint"] ?? "-", cfg: names.join(",") || "-", ext: extendsWhat, issues });
}
rows.sort((a, b) => a.d.localeCompare(b.d));
for (const r of rows) console.log(`${r.issues.length ? "✗" : "✓"} ${r.d} | ${r.v} | ${r.cfg} | ${r.ext} ${r.issues.length ? "| " + r.issues.join("; ") : ""}`);
console.log(`\n${rows.length} packages, ${rows.filter(r => r.issues.length).length} with issues`);
