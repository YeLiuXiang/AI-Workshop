# Content Packs

This folder holds reusable content assets for workshop PPT generation.

## Layers

- `outlines/`: prebuilt deck skeletons that define the default narrative order
- `reference-cases/`: industry- and scenario-specific reusable cases
- `snippets/`: reusable value statements, POC wording, and product phrasing

## Generation Principle

The live event input is intentionally sparse. It should select and tailor these assets rather than force the generator to write a full deck from scratch.

## Current Focus

- `consumer-electronics-iot`
- `cross-border-ecommerce`

## Current Reference Cases

`consumer-electronics-iot`

- `proactive-service-loop`: device-state-driven after-sales service loop
- `predictive-maintenance-loop`: device health scoring and proactive maintenance
- `visual-service-diagnostics`: image-assisted installation, inspection, and field diagnosis
- `global-operations-command-center`: global device metrics, anomaly detection, and operations collaboration
- `security-governance-hub`: IoT access security monitoring, risk triage, and response actions
- `ai-knowledge-hub`: document, ticket, image, and service knowledge consolidation

`cross-border-ecommerce`

- `growth-retention-loop`: customer insight, campaign growth, and churn intervention
- `inventory-fulfillment-control-tower`: cross-region inventory and fulfillment coordination
- `multilingual-service-copilot`: multilingual customer service and return / after-sales support

## Selection Notes

- New case JSON files are discovered automatically by `scripts/compose_workshop_assets.py`.
- Keep each case focused on one business opportunity and one prototype direction.
- Add strong business keywords so sparse live input can select the right case with minimal user text.
- When a lane grows, keep the cases separated by problem family instead of making one oversized catch-all case.