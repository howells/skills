# Critique

Use this when someone shows you a screen and asks what's off, and when you step back from your own work in step 5. A critique changes nothing. It names what is visibly wrong, asks about the calls only the designer can make, and leaves the next move with them. Build only when they ask.

## Method

1. **Name the screen's job.** Give its one job and its primary action in a line. Judge everything against that. If you can't tell who it's for or what it must do, say your reading and ask before going on. If the image holds several screens, say which one you mean.
2. **Look at the system before the style.** Most "something feels off" comes from type sizes, alignment, spacing, radii or colour roles drifting, not from the aesthetic. Check those first.
3. **Separate findings from questions.** If something is visible and breaks a rule in the reference files, state it plainly and say what it costs the person using the screen. If it's a judgement call, such as which element should lead, whether a section earns its place, or the density, ask a question that makes them look again. Don't present taste as fact.
4. **Report only what's visible.** Don't invent defects. A finding is confirmed and carries a severity and a citation to the screen element, a rendered measurement or code. Contrast read from a screenshot is an estimate, and screenshot pixels become CSS pixels only when the capture scale and any resizing are known. Measure from code or the rendered page when you have it. Otherwise put estimated contrast and unverified sizes under Questions ("looks under 4.5:1 - can you check?"), never as confirmed failures.
5. **Pick what matters most.** Run all the questions below silently. Report at most five findings and three questions, most consequential first, starting with whatever stops someone reading or using the screen. If the work is strong, say so and push it further.
6. **Suggest one experiment.** Offer one change small enough to try in ten minutes that tests the biggest finding. Offer it as an experiment, not a redesign.

## Report

```markdown
**Reading:** <who it's for, its one job, its primary action - correct me if I'm off>

**What's off**
- <severity> - <screen element>: <confirmed observation, its evidence and what it costs the user> (<lens>)

**Questions**
1. <question that makes them look again> (<lens>)

**Try**
<one ten-minute experiment>

**Working**
<one specific strength and why it works, if there is one>
```

Tag each line with the lens it comes from, using the lens names below, such as Type, Colour or Order. Leave out any section with nothing worth saying. Be direct and specific, with no hedging and no generic praise.

When they answer or send a new version, don't start over. Say what improved and which lens it serves, what is still off, and ask one new question.

## Lenses

The questions below catch what feels off before anyone can say why. The rule and its fix live in the reference file named in brackets.

**Clarity.** Can you name the screen's job and its one primary action within seconds? Would the purpose still read with the styling stripped back? Does anything distract from getting someone where they're going? Is it built for someone hunting for one thing or someone browsing, and does the layout match?

**Order.** Is the most important thing ranked first, or is something less important just louder? Is there a one-off colour, size, gap, stroke or radius that should match an existing value? Could you explain every value in a sentence? ([spacing.md](interface/spacing.md))

**Type.** Are there three sizes or fewer per section? Could weight, colour, space or position have done the job of the extra size? Does each piece of text have one role, styled the same way every time? Is long text a comfortable measure? ([typography.md](interface/typography.md))

**Grid and proportion.** Do edges line up to a column structure? Does the empty space look placed or left over? Are gaps tighter inside a group than between groups? Do edges or gaps almost match without actually matching? ([layout.md](interface/layout.md), [spacing.md](interface/spacing.md))

**Colour.** Do action colours stay interactive, with nothing static imitating a control? Does each extra hue mean one thing? Does contrast follow importance, or does something minor shout while something important fades? Does the screen still read in greyscale? ([colors.md](interface/colors.md))

**Actions.** Is one primary treatment kept for the next step? Are there two or three clear tiers? Does action weight match consequence, with destructive actions serious and set apart? Does everything pressable look pressable, and nothing static? ([buttons.md](interface/buttons.md))

**Restraint.** What can be removed before anything is added? Does every border, shadow, gradient and blur have a job? Has each departure from a common pattern earned its place? Look for the machine-made tells. ([design.md](interface/design.md), [surfaces.md](interface/surfaces.md))

**Precision.** Where the maths is right but it looks wrong, such as an icon in a circle, a play triangle or text in a button, was it corrected by eye? Zoom in on icon-to-label gaps, line breaks, nested corners and hover states. ([layout.md](interface/layout.md))

**States and real content.** Are the empty, loading, error, partial and overflow states designed? Does it hold up with long names, dense data, missing images and translated text? Does every error, blocked or finished state offer a way forward? Can people see and change the defaults that matter? ([content-accessibility.md](interface/content-accessibility.md))

**Imagery.** Does each image do real work? Do icons share one size, stroke and style? Do highlights and shadows agree on one light source? ([primitives.md](interface/primitives.md))

**Copy.** Does the title say what happens and the button name the action? Does helper text explain why? Does the placeholder repeat the label? Use `signage` for the full pass.

**Motion.** Does each animation explain a change of state, where something came from or where it went? Does it still make sense with motion reduced? Use `zoetrope` for depth.
