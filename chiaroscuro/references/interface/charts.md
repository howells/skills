# Charts and visualisation collections

Use when designing charts or applying a shared visual system across them. Begin with the data's meaning and the question each chart should answer.

## Truthful encoding

- Establish whether values are discrete, ordered or continuous. A smooth curve or continuous surface can imply intermediate values that don't exist. Use distinct marks, steps or bands when that matches the data.
- Preserve units, domains, denominators, baseline meaning and scale transformations. When scales differ between examples, make that visible rather than inviting a false comparison.
- Choose example data that demonstrates the encoding, including gaps, extremes or mixed signs where supported. A decorative sample that makes every chart look like the same trend conceals its capabilities.
- Check legends, labels, tooltips and selected states against the plotted values. Trace a representative value from source to mark and back to the displayed unit.
- Draw a forecast as a dashed continuation with a labelled projected endpoint, so prediction never reads as observation.
- Omit the legend for a single series when the title or a selector already names it.
- Keep each entity the same hue in every chart of a collection, so colour keeps one meaning.
- Show uncertainty ranges where the data has them, and give each chart a text or table alternative that carries its values.

## Shared grammar with individual character

Inventory what the collection shares and what each family needs: type roles, axes, grids, palette roles, marks, line weight, texture, pattern and annotation. Preserve meaningful distinctions when consolidating them. Removing every texture or making every mark identical can erase the accepted look and the distinctions the data needs.

Borrow named visual features while retaining the target's product model. A palette can inform colour roles without importing unrelated controls or replacing the target's tasks. Verify that monochrome, selected and muted states remain distinguishable when they are in scope.

Inspect every changed chart in context and use the same data, dimensions and state for before/after comparisons. Separate visual encoding defects from data defects, and resting-frame parity from interaction or motion. Don't infer faster rendering from fewer components or less code; performance needs its own measurement.
