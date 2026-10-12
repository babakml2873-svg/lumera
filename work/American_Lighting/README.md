# American Lighting — product images

Brand American Lighting: 811 SKUs in the product lists. Variant images were delivered for **730 SKUs (90.0%)**, plus **536 gallery images** (max 4 per SKU).

| List | SKUs | Variant images | Gallery images |
|---|---|---|---|
| List_1 | 811 | 730 | 536 |
| List_2 | 0 | 0 | 0 |
| List_3 | 0 | 0 | 0 |
| List_4 | 0 | 0 | 0 |

* 0 of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.
* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.
* Image sources (files): americanlighting.com (1266). No Lumera Electric source was used.

## Sources searched

americanlighting.com (official, Magento 2): public GraphQL products(filter:{sku:{in:[...]}}) queried for every list SKU; main image + media gallery; placeholder/generic accessory images excluded.

## Matching rules

* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source links to that SKU — or the product's main image when the product has one variant or its variants differ only in non-visual options (colour temperature, wattage, voltage, beam, length…).
* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).
* Gallery images (G) come from the same product; images the source links to a different variant are never used.
* A random sample of variant images was checked visually for product identity.

## SKUs without a variant image — reasons

| Reason | SKUs |
|---|---|
| No exact SKU match in the harvested source catalog(s) | 39 |
| Source product has no images | 25 |
| source image is a placeholder/non-product graphic (_aml-product_ph_74.webp) | 1 |
| source image is a placeholder/non-product graphic (_aml-product_ph_75.webp) | 1 |
| source image is a placeholder/non-product graphic (_aml-product_ph_41.webp) | 1 |
| source image is a placeholder/non-product graphic (_aml-product_ph_21.webp) | 1 |
| V image failed processing: source only 136x96 px (too small) | 1 |
| source image is a placeholder/non-product graphic (_aml-product_ph_39.webp) | 1 |
| source image is a placeholder/non-product graphic (_aml-product_ph_37.webp) | 1 |
| source image is a placeholder/non-product graphic (_aml-product_ph_18.webp) | 1 |
| source image is a placeholder/non-product graphic (_aml-product_ph_17.webp) | 1 |
| source image is a placeholder/non-product graphic (_aml-product_ph_6.webp) | 1 |
| source image is a placeholder/non-product graphic (_aml-cc-product_ph.webp) | 1 |
| source image is a placeholder/non-product graphic (_aml-product_ph_44.webp) | 1 |
| source image is a placeholder/non-product graphic (_aml-product_ph_40.webp) | 1 |
| source image is a placeholder/non-product graphic (_aml-product_ph_31.webp) | 1 |
| source image is a placeholder/non-product graphic (_aml-product_ph_63.webp) | 1 |
| source image is a placeholder/non-product graphic (_aml-product_ph_20.webp) | 1 |
| source image is a placeholder/non-product graphic (_aml-product_ph_58.webp) | 1 |

## Folder structure

`List_N/American_Lighting/` images per original list (empty lists hold a marker file); `Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs.
