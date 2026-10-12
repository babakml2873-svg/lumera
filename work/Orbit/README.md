# Orbit — product images

Brand Orbit: 4507 SKUs in the product lists. Variant images were delivered for **1117 SKUs (24.8%)**, plus **21 gallery images** (max 2 per SKU).

| List | SKUs | Variant images | Gallery images |
|---|---|---|---|
| List_1 | 422 | 26 | 0 |
| List_2 | 18 | 0 | 0 |
| List_3 | 3200 | 819 | 2 |
| List_4 | 867 | 272 | 19 |

* 23 of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.
* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.
* Image sources (files): sonicelectric.com (1138). No Lumera Electric source was used.

## Sources searched

orbitelectric.com (official Orbit Industries) is Cloudflare-blocked from this environment. Used Sonic Electric (Shopify distributor) collection orbit-industries (1,255 products) and Wire & Co (shopwirenco.com) collection orbit-industries (671 products) as fallback; exact SKU match ignoring dashes (Orbit lists LB-200AS for LB200AS).

## Matching rules

* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source links to that SKU — or the product's main image when the product has one variant or its variants differ only in non-visual options (colour temperature, wattage, voltage, beam, length…).
* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).
* Gallery images (G) come from the same product; images the source links to a different variant are never used.
* A random sample of variant images was checked visually for product identity.

## SKUs without a variant image — reasons

| Reason | SKUs |
|---|---|
| No exact SKU match in the harvested source catalog(s) | 3380 |
| V image failed processing: source only 265x265 px (too small) | 8 |
| V image failed processing: source only 283x267 px (too small) | 1 |
| V image failed processing: source only 272x272 px (too small) | 1 |

## Folder structure

`List_N/Orbit/` images per original list (empty lists hold a marker file); `Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs.
