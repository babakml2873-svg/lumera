# UMAGE — product images

Brand UMAGE: 646 SKUs in the product lists. Variant images were delivered for **626 SKUs (96.9%)**, plus **15 gallery images** (max 4 per SKU).

| List | SKUs | Variant images | Gallery images |
|---|---|---|---|
| List_1 | 566 | 551 | 12 |
| List_2 | 80 | 75 | 3 |
| List_3 | 0 | 0 | 0 |
| List_4 | 0 | 0 | 0 |

* 436 of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.
* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.
* Image sources (files): umage.us (621), www.umage.com (20). No Lumera Electric source was used.

## Sources searched

umage.us (official US store, Shopify, 107 products/1,195 variants) and umage.com (official global store, 228 products) - exact variant SKU with the variant's own colour packshot. List bundle codes 'shade_component' are matched as UMAGE's combined code '<shade>C<component>' where it exists, otherwise to the shade alone (Medium: component colour not verified).

## Matching rules

* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source links to that SKU — or the product's main image when the product has one variant or its variants differ only in non-visual options (colour temperature, wattage, voltage, beam, length…).
* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).
* Gallery images (G) come from the same product; images the source links to a different variant are never used.
* A random sample of variant images was checked visually for product identity.

## SKUs without a variant image — reasons

| Reason | SKUs |
|---|---|
| No exact SKU match in the harvested source catalog(s) | 20 |

## Folder structure

`List_N/UMAGE/` images per original list (empty lists hold a marker file); `Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs.
