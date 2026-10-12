# EnVision — product images

Brand EnVision: 1497 SKUs in the product lists. Variant images were delivered for **1289 SKUs (86.1%)**, plus **3186 gallery images** (max 4 per SKU).

| List | SKUs | Variant images | Gallery images |
|---|---|---|---|
| List_1 | 589 | 551 | 1564 |
| List_2 | 908 | 738 | 1622 |
| List_3 | 0 | 0 | 0 |
| List_4 | 0 | 0 | 0 |

* 174 of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.
* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.
* Image sources (files): envisionledlighting.com (4475). No Lumera Electric source was used.

## Sources searched

envisionledlighting.com (official EnVision LED Lighting): the site's own DatoCMS content API queried by part number (field 'number' = full SKU); product images as published (originals ~1200 px).

## Matching rules

* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source links to that SKU — or the product's main image when the product has one variant or its variants differ only in non-visual options (colour temperature, wattage, voltage, beam, length…).
* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).
* Gallery images (G) come from the same product; images the source links to a different variant are never used.
* A random sample of variant images was checked visually for product identity.

## SKUs without a variant image — reasons

| Reason | SKUs |
|---|---|
| No exact SKU match in the harvested source catalog(s) | 208 |

## Folder structure

`List_N/EnVision/` images per original list (empty lists hold a marker file); `Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs.
