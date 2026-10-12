# Intermatic — product images

Brand Intermatic: 738 SKUs in the product lists. Variant images were delivered for **693 SKUs (93.9%)**, plus **1667 gallery images** (max 4 per SKU).

| List | SKUs | Variant images | Gallery images |
|---|---|---|---|
| List_1 | 0 | 0 | 0 |
| List_2 | 0 | 0 | 0 |
| List_3 | 71 | 71 | 214 |
| List_4 | 667 | 622 | 1453 |

* 132 of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.
* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.
* Image sources (files): intermatic.com (2360). No Lumera Electric source was used.

## Sources searched

intermatic.com (official): the site's storefront API /api/v1/products?query=<SKU>&expand=images, erpNumber must equal the list SKU; product images as published (images named for a sibling model are marked Medium).

## Matching rules

* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source links to that SKU — or the product's main image when the product has one variant or its variants differ only in non-visual options (colour temperature, wattage, voltage, beam, length…).
* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).
* Gallery images (G) come from the same product; images the source links to a different variant are never used.
* A random sample of variant images was checked visually for product identity.

## SKUs without a variant image — reasons

| Reason | SKUs |
|---|---|
| V image failed processing: download failed | 17 |
| source image is a placeholder/non-product graphic (197903_photo-coming-soon.jpg) | 15 |
| No exact SKU match in the harvested source catalog(s) | 13 |

## Folder structure

`List_N/Intermatic/` images per original list (empty lists hold a marker file); `Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs.
