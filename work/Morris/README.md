# Morris — product images

Brand Morris: 1760 SKUs in the product lists. Variant images were delivered for **1713 SKUs (97.3%)**, plus **0 gallery images** (max 2 per SKU).

| List | SKUs | Variant images | Gallery images |
|---|---|---|---|
| List_1 | 0 | 0 | 0 |
| List_2 | 1760 | 1713 | 0 |
| List_3 | 0 | 0 | 0 |
| List_4 | 0 | 0 | 0 |

* 754 of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.
* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.
* Image sources (files): morrisproducts.com (1713). No Lumera Electric source was used.

## Sources searched

morrisproducts.com (official Morris Products): the site's own product-by-SKU JSON service; largePic image from Morris' image CDN (900x900). Child SKUs that only show the parent family image are marked Medium.

## Matching rules

* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source links to that SKU — or the product's main image when the product has one variant or its variants differ only in non-visual options (colour temperature, wattage, voltage, beam, length…).
* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).
* Gallery images (G) come from the same product; images the source links to a different variant are never used.
* A random sample of variant images was checked visually for product identity.

## SKUs without a variant image — reasons

| Reason | SKUs |
|---|---|
| V image failed processing: download failed | 34 |
| No exact SKU match in the harvested source catalog(s) | 13 |

## Folder structure

`List_N/Morris/` images per original list (empty lists hold a marker file); `Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs.
