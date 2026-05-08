# Enterprise Forum Template

This folder contains template-specific assets for a business presentation deck.

## Intended Page Types

- cover
- cover-workshop
- company-intro
- capability-grid
- comparison
- step-flow
- scenario
- scenario-summary
- as-is-pain-map
- capability-selection
- ai-flow-steps
- product-mapping-table
- business-value
- poc-next-step
- table
- risk
- control
- conclusion

## Files

- `inventory.example.json`: minimal example of a template inventory
- `layout-map.example.json`: maps slide types and logical slots to shape ids

## How To Replace With A Real Template

1. Extract a real PPTX inventory into `inventory.json`.
2. Copy `layout-map.example.json` to `layout-map.json`.
3. Map each slide type and slot to actual `shape-*` ids.
4. Keep geometric information inside the inventory, not in the theme.

For AI Discovery Workshop decks, prefer dedicated slide types and slot mappings rather than reusing a generic 3-bullet layout for every page. The example layout map now includes workshop slide types, but the real template should eventually provide dedicated flow, mapping, and value page geometries.
