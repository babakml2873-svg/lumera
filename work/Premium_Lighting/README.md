# Premium Lighting — product images

Brand Premium Lighting: 142 SKUs in the product lists. Variant images were delivered for **16 SKUs (11.3%)**, plus **38 gallery images** (max 4 per SKU).

| List | SKUs | Variant images | Gallery images |
|---|---|---|---|
| List_1 | 0 | 0 | 0 |
| List_2 | 142 | 16 | 38 |
| List_3 | 0 | 0 | 0 |
| List_4 | 0 | 0 | 0 |

* 0 of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.
* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.
* Image sources (files): premiumlightinginc.com (54). No Lumera Electric source was used.

## Sources searched

premiumlightinginc.com (official, Shopify, 51 products): the store has no SKU field - model codes (EDI-/SU-/SMA-) are taken from each product description and the generation (G1-G5) from the title; matched exactly to the list SKU. Area lights, T8 tubes and most SU- items have no source listing.

## Matching rules

* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source links to that SKU — or the product's main image when the product has one variant or its variants differ only in non-visual options (colour temperature, wattage, voltage, beam, length…).
* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).
* Gallery images (G) come from the same product; images the source links to a different variant are never used.
* A random sample of variant images was checked visually for product identity.

## SKUs without a variant image — reasons

| Reason | SKUs |
|---|---|
| No exact SKU match in the harvested source catalog(s) | 126 |

## Folder structure

`List_N/Premium_Lighting/` images per original list (empty lists hold a marker file); `Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs.
