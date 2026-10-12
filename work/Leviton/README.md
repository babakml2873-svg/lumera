# Leviton — product images

Brand Leviton: 4113 SKUs in the product lists. Variant images were delivered for **4059 SKUs (98.7%)**, plus **0 gallery images** (max 2 per SKU).

| List | SKUs | Variant images | Gallery images |
|---|---|---|---|
| List_1 | 2648 | 2623 | 0 |
| List_2 | 1465 | 1436 | 0 |
| List_3 | 0 | 0 | 0 |
| List_4 | 0 | 0 | 0 |

* 2818 of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.
* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.
* Image sources (files): leviton.com (4059). No Lumera Electric source was used.

## Sources searched

leviton.com (official): product sitemap (18,598 product pages, page path = SKU) -> each needed product page's og:image (main product image from Leviton's DAM).

## Matching rules

* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source links to that SKU — or the product's main image when the product has one variant or its variants differ only in non-visual options (colour temperature, wattage, voltage, beam, length…).
* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).
* Gallery images (G) come from the same product; images the source links to a different variant are never used.
* A random sample of variant images was checked visually for product identity.

## SKUs without a variant image — reasons

| Reason | SKUs |
|---|---|
| V image failed processing: source only 175x175 px (too small) | 13 |
| No exact SKU match in the harvested source catalog(s) | 12 |
| source photo is of MGFN2 (re-used by the source for this SKU) - not used | 5 |
| source photo is of MGFT1 (re-used by the source for this SKU) - not used | 4 |
| source photo is of MGFN1 (re-used by the source for this SKU) - not used | 4 |
| V image failed processing: download failed | 3 |
| source photo is of 15W47 (re-used by the source for this SKU) - not used | 3 |
| source photo is of M5262-S (re-used by the source for this SKU) - not used | 1 |
| source photo is of MGFT2 (re-used by the source for this SKU) - not used | 1 |
| source photo is of 1221-2W (re-used by the source for this SKU) - not used | 1 |
| source photo is of CR015 (re-used by the source for this SKU) - not used | 1 |
| source photo is of M8300-HW (re-used by the source for this SKU) - not used | 1 |
| source image is a placeholder/non-product graphic (ESL01-1LW LED Advanced Logo.jpg) | 1 |
| V image failed processing: source only 235x235 px (too small) | 1 |
| V image failed processing: source only 200x200 px (too small) | 1 |
| V image failed processing: source only 174x202 px (too small) | 1 |
| source photo is of 15W47-B (re-used by the source for this SKU) - not used | 1 |

## Brand-specific notes

* Leviton.com re-uses one series photo for several catalog numbers (e.g. 15 A and 20 A receptacles, standard and lighted switches). Variant images whose identical photo (same image and colour) is also used for a different product are marked Medium (OK-REVIEW-RECOMMENDED) with the other SKUs named in Notes. When the photo's file name is another SKU's catalog number the image was not used.

## Folder structure

`List_N/Leviton/` images per original list (empty lists hold a marker file); `Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs.
