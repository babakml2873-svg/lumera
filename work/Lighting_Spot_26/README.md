# Lighting Spot 26 — product images

Brand Lighting Spot 26: 886 SKUs in the product lists. Variant images were delivered for **404 SKUs (45.6%)**, plus **81 gallery images** (max 4 per SKU).

| List | SKUs | Variant images | Gallery images |
|---|---|---|---|
| List_1 | 196 | 92 | 5 |
| List_2 | 107 | 48 | 14 |
| List_3 | 0 | 0 | 0 |
| List_4 | 583 | 264 | 62 |

* 285 of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.
* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.
* Image sources (files): lightingspot26.com (485). No Lumera Electric source was used.

## Sources searched

lightingspot26.com (official Lighting Spot 26): WooCommerce Store API (823 products); product name/slug = model number, matched exactly (case/punctuation-insensitive). Many list SKUs are written differently from the manufacturer's model numbers and are reported as unmatched rather than guessed.
 Rule-based aliases (Medium) only for colour-temperature notation (5K = 50K) and the LS26/LS prefix; colour suffixes are never dropped. Product page slug used as an additional exact model key.

## Matching rules

* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source links to that SKU — or the product's main image when the product has one variant or its variants differ only in non-visual options (colour temperature, wattage, voltage, beam, length…).
* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).
* Gallery images (G) come from the same product; images the source links to a different variant are never used.
* A random sample of variant images was checked visually for product identity.

## SKUs without a variant image — reasons

| Reason | SKUs |
|---|---|
| No exact SKU match in the harvested source catalog(s) | 473 |
| V image failed processing: source only 288x288 px (too small) | 5 |
| Source product has no images | 3 |
| V image failed processing: source only 25x200 px (too small) | 1 |

## Folder structure

`List_N/Lighting_Spot_26/` images per original list (empty lists hold a marker file); `Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs.
