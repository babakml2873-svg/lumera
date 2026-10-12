# Damar — product images

Brand Damar: 746 SKUs in the product lists. Variant images were delivered for **662 SKUs (88.7%)**, plus **0 gallery images** (max 4 per SKU).

| List | SKUs | Variant images | Gallery images |
|---|---|---|---|
| List_1 | 0 | 0 | 0 |
| List_2 | 746 | 662 | 0 |
| List_3 | 0 | 0 | 0 |
| List_4 | 0 | 0 | 0 |

* 8 of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.
* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.
* Image sources (files): damarww.com (662). No Lumera Electric source was used.

## Sources searched

damarww.com (official Damar Worldwide; damarworldwide.com does not resolve): product page /products/details/di/x/<SKU>/ per SKU, JSON-LD Product sku must equal the list SKU; JSON-LD image(s).

## Matching rules

* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source links to that SKU — or the product's main image when the product has one variant or its variants differ only in non-visual options (colour temperature, wattage, voltage, beam, length…).
* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).
* Gallery images (G) come from the same product; images the source links to a different variant are never used.
* A random sample of variant images was checked visually for product identity.

## SKUs without a variant image — reasons

| Reason | SKUs |
|---|---|
| No exact SKU match in the harvested source catalog(s) | 21 |
| Source product has no images | 11 |
| V image failed processing: source only 309x315 px (too small) | 2 |
| V image failed processing: download failed | 2 |
| V image failed processing: source only 105x202 px (too small) | 2 |
| V image failed processing: source only 202x315 px (too small) | 1 |
| V image failed processing: source only 315x241 px (too small) | 1 |
| V image failed processing: source only 165x315 px (too small) | 1 |
| V image failed processing: source only 147x315 px (too small) | 1 |
| V image failed processing: source only 179x315 px (too small) | 1 |
| V image failed processing: source only 158x315 px (too small) | 1 |
| V image failed processing: source only 250x315 px (too small) | 1 |
| V image failed processing: source only 188x300 px (too small) | 1 |
| V image failed processing: source only 205x300 px (too small) | 1 |
| V image failed processing: source only 229x300 px (too small) | 1 |
| V image failed processing: source only 161x228 px (too small) | 1 |
| V image failed processing: source only 252x300 px (too small) | 1 |
| V image failed processing: source only 300x123 px (too small) | 1 |
| V image failed processing: source only 271x315 px (too small) | 1 |
| V image failed processing: source only 234x315 px (too small) | 1 |
| V image failed processing: source only 315x306 px (too small) | 1 |
| V image failed processing: source only 219x256 px (too small) | 1 |
| V image failed processing: source only 149x315 px (too small) | 1 |
| V image failed processing: source only 311x315 px (too small) | 1 |
| V image failed processing: source only 109x300 px (too small) | 1 |
| V image failed processing: source only 137x300 px (too small) | 1 |
| V image failed processing: source only 136x300 px (too small) | 1 |
| V image failed processing: source only 106x200 px (too small) | 1 |
| V image failed processing: source only 138x300 px (too small) | 1 |
| V image failed processing: source only 109x259 px (too small) | 1 |
| V image failed processing: source only 146x321 px (too small) | 1 |
| V image failed processing: source only 219x300 px (too small) | 1 |
| V image failed processing: source only 199x300 px (too small) | 1 |
| V image failed processing: source only 95x263 px (too small) | 1 |
| V image failed processing: source only 54x116 px (too small) | 1 |
| V image failed processing: source only 99x259 px (too small) | 1 |
| V image failed processing: source only 68x171 px (too small) | 1 |
| V image failed processing: source only 225x378 px (too small) | 1 |
| V image failed processing: source only 128x315 px (too small) | 1 |
| V image failed processing: source only 80x237 px (too small) | 1 |
| V image failed processing: source only 156x300 px (too small) | 1 |
| V image failed processing: source only 153x315 px (too small) | 1 |
| V image failed processing: source only 134x283 px (too small) | 1 |
| V image failed processing: source only 130x270 px (too small) | 1 |
| V image failed processing: source only 117x315 px (too small) | 1 |
| V image failed processing: source only 139x285 px (too small) | 1 |
| V image failed processing: source only 131x131 px (too small) | 1 |
| V image failed processing: source only 99x253 px (too small) | 1 |
| V image failed processing: source only 139x300 px (too small) | 1 |
| V image failed processing: source only 134x292 px (too small) | 1 |
| V image failed processing: source only 136x315 px (too small) | 1 |

## Folder structure

`List_N/Damar/` images per original list (empty lists hold a marker file); `Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs.
