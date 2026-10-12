# Satco — product images

Brand Satco: 1252 SKUs in the product lists. Variant images were delivered for **619 SKUs (49.4%)**, plus **531 gallery images** (max 4 per SKU).

| List | SKUs | Variant images | Gallery images |
|---|---|---|---|
| List_1 | 436 | 231 | 105 |
| List_2 | 816 | 388 | 426 |
| List_3 | 0 | 0 | 0 |
| List_4 | 0 | 0 | 0 |

* 2 of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.
* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.
* Image sources (files): www.bulbamerica.com (1150). No Lumera Electric source was used.

## Sources searched

satco.com / nuvolighting.com return HTTP 429 (bot check) from this environment. Used BulbAmerica (bulbamerica.com, Shopify retailer) collections nuvo-lighting (2,637 products) and satco (2,099 products); exact variant SKU match (60-/65- item numbers are Nuvo/Satco).

## Matching rules

* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source links to that SKU — or the product's main image when the product has one variant or its variants differ only in non-visual options (colour temperature, wattage, voltage, beam, length…).
* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).
* Gallery images (G) come from the same product; images the source links to a different variant are never used.
* A random sample of variant images was checked visually for product identity.

## SKUs without a variant image — reasons

| Reason | SKUs |
|---|---|
| No exact SKU match in the harvested source catalog(s) | 633 |

## Folder structure

`List_N/Satco/` images per original list (empty lists hold a marker file); `Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs.
