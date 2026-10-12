# General Electric — product images

Brand General Electric: 160 SKUs in the product lists. Variant images were delivered for **142 SKUs (88.8%)**, plus **310 gallery images** (max 4 per SKU).

| List | SKUs | Variant images | Gallery images |
|---|---|---|---|
| List_1 | 0 | 0 | 0 |
| List_2 | 160 | 142 | 310 |
| List_3 | 0 | 0 | 0 |
| List_4 | 0 | 0 | 0 |

* 101 of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.
* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.
* Image sources (files): superbreakers.com (450), breakeroutlet.com (2). No Lumera Electric source was used.

## Sources searched

geindustrial.com fails (certificate error); the official ABB eCatalog (empower.abb.com) has small images (max 720x540) and many SKUs without images. Used SuperBreakers (superbreakers.com, Shopify; sells new and re-certified) per-SKU search with exact variant SKU match, re-certified '-R' and non-genuine 'BE-' items excluded; Breaker Outlet (Shopify) vendor 'GE Industrial' as second source.

## Matching rules

* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source links to that SKU — or the product's main image when the product has one variant or its variants differ only in non-visual options (colour temperature, wattage, voltage, beam, length…).
* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).
* Gallery images (G) come from the same product; images the source links to a different variant are never used.
* A random sample of variant images was checked visually for product identity.

## SKUs without a variant image — reasons

| Reason | SKUs |
|---|---|
| Source product has no images | 6 |
| No exact SKU match in the harvested source catalog(s) | 4 |
| source photo is of THQB1120 (re-used by the source for this SKU) - not used | 1 |
| source photo is of THQB32015 (re-used by the source for this SKU) - not used | 1 |
| source photo is of THQB32025 (re-used by the source for this SKU) - not used | 1 |
| source photo is of THQB32020 (re-used by the source for this SKU) - not used | 1 |
| source photo is of THQB32100 (re-used by the source for this SKU) - not used | 1 |
| source photo is of THQB32050 (re-used by the source for this SKU) - not used | 1 |
| source photo is of THQB32060 (re-used by the source for this SKU) - not used | 1 |
| source photo is of THQB32030 (re-used by the source for this SKU) - not used | 1 |

## Brand-specific notes

* Circuit breakers: the reseller often re-uses one series photo for several ampere ratings/poles. Variant images whose identical photo is also used for a different product are marked Medium (OK-REVIEW-RECOMMENDED) with the other SKUs named in Notes - the rating printed on the handle in the photo may differ from the SKU.
* Some Breaker Outlet photos carry a faint 'BREAKEROUTLET' watermark; they were kept (no image editing was allowed) and should be replaced if watermark-free images are required.

## Folder structure

`List_N/General_Electric/` images per original list (empty lists hold a marker file); `Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs.
