# Dottie — product images

Brand Dottie: 2966 SKUs in the product lists. Variant images were delivered for **2895 SKUs (97.6%)**, plus **0 gallery images** (max 4 per SKU).

| List | SKUs | Variant images | Gallery images |
|---|---|---|---|
| List_1 | 93 | 89 | 0 |
| List_2 | 7 | 7 | 0 |
| List_3 | 2866 | 2799 | 0 |
| List_4 | 0 | 0 | 0 |

* 0 of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.
* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.
* Image sources (files): rspsupply.com (2895). No Lumera Electric source was used.

## Sources searched

lhdottie.com (official L.H. Dottie) is Cloudflare-blocked from this environment (HTTP 403 on every path). Used RSP Supply (rspsupply.com, distributor) per-part images /images/product/large/Dottie-<PART>.jpg, accepted only on HTTP 200 image responses (1000x1000).

## Matching rules

* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source links to that SKU — or the product's main image when the product has one variant or its variants differ only in non-visual options (colour temperature, wattage, voltage, beam, length…).
* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).
* Gallery images (G) come from the same product; images the source links to a different variant are never used.
* A random sample of variant images was checked visually for product identity.

## SKUs without a variant image — reasons

| Reason | SKUs |
|---|---|
| No exact SKU match in the harvested source catalog(s) | 70 |
| V image failed processing: source only 250x250 px (too small) | 1 |

## Folder structure

`List_N/Dottie/` images per original list (empty lists hold a marker file); `Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs.
