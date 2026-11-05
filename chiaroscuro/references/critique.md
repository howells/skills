# Critique

Use this when someone shows you a screen, code or a change and asks what's off, and when you step back from your own work. A critique changes nothing. It names what is visibly wrong, asks about the calls only the designer can make, and leaves the next move with them. Build only when they ask.

## Method

1. **Name the screen's job.** Give its one job and its primary action in a line, and judge everything against that. If you can't tell who it's for or what it must do, say your reading and ask. If the image holds several screens, say which one you mean.
2. **Look at the system before the style.** Most "something feels off" comes from drifting type sizes, alignment, spacing, radii or colour roles, not from the aesthetic. Check those first.
3. **Give findings and judgement.** Something visible that breaks a rule in this skill is a finding: state it plainly and say what it costs the person using the screen. On judgement calls (what should lead, what should go, the density) give your call and the reason, marked as your call. Ask only about missing product decisions.
4. **Report only what's there.** A finding cites the screen element, a rendered measurement or `file:line`. Contrast read from a screenshot is an estimate, and screenshot pixels are CSS pixels only when the capture scale is known; measure from code or the rendered page when you have it, and otherwise put estimates under Questions ("looks under 4.5:1 - can you check?").
5. **Pick what matters most.** Run every lens below silently. Report at most five findings and three questions, most consequential first, starting with whatever stops someone reading or using the screen: an unnamed or unfocusable control, a pointer-only path, text that fails contrast, meaning carried by colour alone, content clipped at a phone width or 200% zoom, an error with no way forward. One root cause is one finding, with every place it shows. If the work is strong, say so and push it further.
6. **Suggest one experiment.** One change small enough to try in ten minutes that tests the biggest finding. An experiment, not a redesign.

## Reviewing code or a change

Read the whole diff before judging it, including the removed lines: a deleted `aria-label`, focus style or reduced-motion guard is a regression unless something in the change replaces it. Follow a changed token or shared component to a few of the screens that render it. Look for the incomplete change: a new variant missing hover, focus, disabled or loading; a new component with no empty, error or narrow state; a control added to one screen but not its siblings. Tag each finding as introduced, a regression, or pre-existing; mention at most three pre-existing ones. Read refs in place; never check out or stash over someone's working tree.

## Report

```markdown
**Reading:** <who it's for, its one job, its primary action - correct me if I'm off>

**What's off**
- <severity> - <screen element or file:line>: <confirmed observation, its evidence and what it costs the user> (<lens>)

**Questions**
1. <question that makes them look again> (<lens>)

**Try**
<one ten-minute experiment>

**Working**
<one specific strength and why it works, if there is one>
```

Severity is high when it blocks a task, misleads or hides content; medium when it harms comprehension or consistency; low for isolated polish. Leave out any section with nothing worth saying. Be direct and specific, with no hedging and no generic praise.

When they answer or send a new version, don't start over. Say what improved and which lens it serves, and what is still off.

## Lenses

These catch what feels off before anyone can say why. The rule and its fix live in the reference file named in brackets, beside this one.

**Clarity.** Can you name the screen's job and its one primary action within seconds? Would the purpose still read with the styling stripped back? Is it built for someone hunting for one thing or someone browsing, and does the layout match? Does anything show the system rather than the user's work?

**Order.** Is the most important thing ranked first, or is something less important just louder? Is there a one-off colour, size, gap, stroke or radius that should match an existing value? Could you explain every value in a sentence? (`layout.md`)

**Type.** Three sizes or fewer per section? Could weight, colour, space or position have done the job of the extra size? Does each piece of text have one role, styled the same way every time? Any caps, tracking or decorative mono? Is long text a comfortable measure? (`type.md`)

**Grid and proportion.** Do edges line up to a column structure? Does empty space look placed or left over? Are gaps tighter inside a group than between groups? Do edges or gaps almost match without matching? (`layout.md`)

**Colour.** Do action colours stay interactive, with nothing static imitating a control? Does each extra hue mean one thing? Does contrast follow importance? Does it still read in greyscale, and in dark mode? (`color.md`)

**Actions.** One primary treatment for the next step? Two or three clear tiers? Does weight match consequence, with destructive actions serious and set apart? Does everything pressable look pressable, and nothing static? (`components.md`)

**Restraint.** What can be removed before anything is added? Does every border, shadow, gradient and blur have a job? Has each departure from a common pattern earned its place? Look for the machine-made tells in the skill's main file, and the furniture in `marketing.md` on a landing page.

**Precision.** Where the maths is right but it looks wrong, such as an icon in a circle, a play triangle or text in a button, was it corrected by eye? Zoom in on icon-to-label gaps, line breaks, nested corners and hover states. (`layout.md`)

**States and real content.** Are empty, loading, error, partial and overflow states designed? Does it hold with long names, dense data, missing images and translated text? Does every error, blocked or finished state offer a way forward? Can it be used by keyboard alone, with every control named? (`interaction.md`, `forms.md`)

**Imagery.** Does each image do real work? Do icons share one size, stroke and style? Do highlights and shadows agree on one light source? (`components.md`)

**Copy.** Does the title say what happens and the button name the action? Does helper text explain why? Does the placeholder repeat the label? Use `signage` for the full pass.

**Motion.** Does each animation explain a change of state, where something came from or where it went? Is anything frequent animated at all? Does it still make sense with motion reduced? (`motion.md`)
