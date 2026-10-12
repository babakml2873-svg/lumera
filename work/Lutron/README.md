# Lutron — product images

Brand Lutron: 4858 SKUs in the product lists. Variant images were delivered for **4598 SKUs (94.6%)**, plus **1312 gallery images** (max 2 per SKU).

| List | SKUs | Variant images | Gallery images |
|---|---|---|---|
| List_1 | 3283 | 3145 | 1063 |
| List_2 | 1575 | 1453 | 249 |
| List_3 | 0 | 0 | 0 |
| List_4 | 0 | 0 | 0 |

* 791 of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.
* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.
* Image sources (files): lightingsupply.com (3823), buyriteelectric.com (2087). No Lumera Electric source was used.

## Sources searched

lutron.com is protected by Incapsula (HTTP 403 for every page incl. robots/sitemap); casetawireless.com covers only Caseta. Used Shopify distributors with exact variant SKU = Lutron model number: LightingSupply.com collection lutron (2,696 products, priority 1) and Buy Rite Electric collection lutron (4,764 products, priority 2).

## Matching rules

* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source links to that SKU — or the product's main image when the product has one variant or its variants differ only in non-visual options (colour temperature, wattage, voltage, beam, length…).
* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).
* Gallery images (G) come from the same product; images the source links to a different variant are never used.
* A random sample of variant images was checked visually for product identity.

## SKUs without a variant image — reasons

| Reason | SKUs |
|---|---|
| Product has visual variants (Color Options) and the source links no image to this SKU | 124 |
| No exact SKU match in the harvested source catalog(s) | 79 |
| V image failed processing: source only 225x225 px (too small) | 9 |
| Product has visual variants (Product Type) and the source links no image to this SKU | 6 |
| V image failed processing: source only 180x265 px (too small) | 3 |
| V image failed processing: source only 272x264 px (too small) | 3 |
| V image failed processing: source only 224x224 px (too small) | 2 |
| V image failed processing: source only 220x220 px (too small) | 2 |
| V image failed processing: source only 290x265 px (too small) | 2 |
| Product has visual variants (PRODUCT OPTION) and the source links no image to this SKU | 2 |
| V image failed processing: source only 259x299 px (too small) | 1 |
| V image failed processing: source only 249x293 px (too small) | 1 |
| V image failed processing: source only 221x269 px (too small) | 1 |
| V image failed processing: source only 220x179 px (too small) | 1 |
| V image failed processing: source only 218x220 px (too small) | 1 |
| V image failed processing: source only 177x285 px (too small) | 1 |
| V image failed processing: source only 189x291 px (too small) | 1 |
| V image failed processing: source only 175x176 px (too small) | 1 |
| V image failed processing: source only 250x250 px (too small) | 1 |
| V image failed processing: source only 285x285 px (too small) | 1 |
| V image failed processing: source only 181x246 px (too small) | 1 |
| V image failed processing: source only 216x275 px (too small) | 1 |
| V image failed processing: source only 256x280 px (too small) | 1 |
| V image failed processing: source only 238x290 px (too small) | 1 |
| V image failed processing: source only 260x262 px (too small) | 1 |
| V image failed processing: source only 229x274 px (too small) | 1 |
| V image failed processing: source only 257x295 px (too small) | 1 |
| V image failed processing: source only 156x166 px (too small) | 1 |
| V image failed processing: source only 158x201 px (too small) | 1 |
| V image failed processing: source only 156x198 px (too small) | 1 |
| V image failed processing: source only 175x189 px (too small) | 1 |
| V image failed processing: source only 165x194 px (too small) | 1 |
| V image failed processing: source only 190x198 px (too small) | 1 |
| V image failed processing: source only 134x193 px (too small) | 1 |
| V image failed processing: source only 225x224 px (too small) | 1 |
| V image failed processing: source only 215x283 px (too small) | 1 |
| V image failed processing: source only 174x176 px (too small) | 1 |
| Source product has no images | 1 |

## Brand-specific notes

* LightingSupply.com product galleries include text infographics (file names '*textimage*' / '*imagewithtext*'), often showing a different product of the kit or series; these were excluded (641 images).

## Folder structure

`List_N/Lutron/` images per original list (empty lists hold a marker file); `Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs.
