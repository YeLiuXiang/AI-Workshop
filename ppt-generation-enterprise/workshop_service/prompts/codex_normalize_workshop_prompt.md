Read `{request_path}` and return JSON only.

Use the same sparse workshop input schema as the request file.

Keep these top-level keys:
- `workshop`
- `event_input`
- `mvp_spec`
- `current_process`
- `detected_cards`
- `recognized_cards`
- `card_photo_paths`
- `product_mapping`

Rules:
- keep `event_input.scene_name` if it exists
- keep all business text in Chinese
- preserve customer intent
- do not modify repository files
- if images are attached, use them to fill `recognized_cards` and, when confident, `detected_cards`
- if no images are attached, keep card arrays empty unless the request already provides them
- infer concise `current_process` and missing `mvp_spec` items only when needed
- avoid placeholders such as `待补充`

Attached image paths:
{image_paths}
