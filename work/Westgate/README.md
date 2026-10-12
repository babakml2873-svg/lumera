# Westgate — product images

Brand Westgate: 5115 SKUs in the product lists. Variant images were delivered for **3747 SKUs (73.3%)**, plus **1764 gallery images** (max 2 per SKU).

| List | SKUs | Variant images | Gallery images |
|---|---|---|---|
| List_1 | 1037 | 779 | 330 |
| List_2 | 956 | 716 | 488 |
| List_3 | 2797 | 1966 | 867 |
| List_4 | 325 | 286 | 79 |

* 193 of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.
* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.
* Image sources (files): sonicelectric.com (4761), lightingsupply.com (750). No Lumera Electric source was used.

## Sources searched

westgatemfg.com (official) is Cloudflare-blocked from this environment. Used two Shopify distributors whose variant SKU is the exact Westgate part number: Sonic Electric collection westgate (5,289 products, priority) and LightingSupply.com collection westgate-manufacturing (5,037 products).

## Matching rules

* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source links to that SKU — or the product's main image when the product has one variant or its variants differ only in non-visual options (colour temperature, wattage, voltage, beam, length…).
* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).
* Gallery images (G) come from the same product; images the source links to a different variant are never used.
* A random sample of variant images was checked visually for product identity.

## SKUs without a variant image — reasons

| Reason | SKUs |
|---|---|
| Source product has no images | 761 |
| No exact SKU match in the harvested source catalog(s) | 513 |
| Product has visual variants (Size) and the source links no image to this SKU | 21 |
| Product has visual variants (Color, Wattage, Color Temperature) and the source links no image to this SKU | 9 |
| Product has visual variants (Finish) and the source links no image to this SKU | 8 |
| V image failed processing: source only 265x265 px (too small) | 8 |
| V image failed processing: source only 250x250 px (too small) | 6 |
| Product has visual variants (Color, Color Temperature) and the source links no image to this SKU | 6 |
| Product has visual variants (Finish, Color Temperature) and the source links no image to this SKU | 6 |
| Product has visual variants (Color) and the source links no image to this SKU | 4 |
| V image failed processing: source only 150x150 px (too small) | 3 |
| V image failed processing: source only 287x156 px (too small) | 3 |
| V image failed processing: source only 245x240 px (too small) | 2 |
| V image failed processing: source only 236x286 px (too small) | 2 |
| V image failed processing: source only 284x177 px (too small) | 2 |
| V image failed processing: source only 104x243 px (too small) | 1 |
| V image failed processing: source only 288x167 px (too small) | 1 |
| V image failed processing: source only 296x222 px (too small) | 1 |
| V image failed processing: source only 296x236 px (too small) | 1 |
| V image failed processing: source only 282x182 px (too small) | 1 |
| V image failed processing: source only 243x190 px (too small) | 1 |
| V image failed processing: source only 246x208 px (too small) | 1 |
| V image failed processing: source only 139x130 px (too small) | 1 |
| V image failed processing: source only 148x142 px (too small) | 1 |
| V image failed processing: source only 279x272 px (too small) | 1 |
| V image failed processing: source only 286x286 px (too small) | 1 |
| V image failed processing: source only 235x194 px (too small) | 1 |
| V image failed processing: source only 283x199 px (too small) | 1 |
| V image failed processing: source only 153x98 px (too small) | 1 |

## Folder structure

`List_N/Westgate/` images per original list (empty lists hold a marker file); `Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs.
