# Cutler Hammer — product images

Brand Cutler Hammer: 218 SKUs in the product lists. Variant images were delivered for **174 SKUs (79.8%)**, plus **234 gallery images** (max 4 per SKU).

| List | SKUs | Variant images | Gallery images |
|---|---|---|---|
| List_1 | 0 | 0 | 0 |
| List_2 | 218 | 174 | 234 |
| List_3 | 0 | 0 | 0 |
| List_4 | 0 | 0 | 0 |

* 121 of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.
* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.
* Image sources (files): eaton.com (405), breakeroutlet.com (3). No Lumera Electric source was used.

## Sources searched

eaton.com (official; Cutler-Hammer is an Eaton brand): product page skuPage.<SKU>.html per SKU, JSON-LD sku must equal the list SKU; images = the page's product image assets, downloaded full size from Eaton's image server dynamicmedia.eaton.com. Pages fetched at robots.txt Crawl-delay (20 s). Second source for SKUs without an eaton.com page/image: Breaker Outlet (breakeroutlet.com, Shopify reseller), exact variant SKU, refurbished '-R' variants excluded.

## Matching rules

* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source links to that SKU — or the product's main image when the product has one variant or its variants differ only in non-visual options (colour temperature, wattage, voltage, beam, length…).
* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).
* Gallery images (G) come from the same product; images the source links to a different variant are never used.
* A random sample of variant images was checked visually for product identity.

## SKUs without a variant image — reasons

| Reason | SKUs |
|---|---|
| source photo is of GHB3100 (re-used by the source for this SKU) - not used | 11 |
| source photo is of BAB2020 (re-used by the source for this SKU) - not used | 8 |
| Source product has no images | 5 |
| source photo is of QBGFT2020 (re-used by the source for this SKU) - not used | 4 |
| source photo is of BAB3030H (re-used by the source for this SKU) - not used | 4 |
| source photo is of CSR2200N (re-used by the source for this SKU) - not used | 3 |
| No exact SKU match in the harvested source catalog(s) | 2 |
| source photo is of BRD220230 (re-used by the source for this SKU) - not used | 2 |
| source photo is of GHB1020 (re-used by the source for this SKU) - not used | 2 |
| source photo is of BAB3060H (re-used by the source for this SKU) - not used | 1 |
| source photo is of CCV2200 (re-used by the source for this SKU) - not used | 1 |
| source photo is of QB1020AFGF (re-used by the source for this SKU) - not used | 1 |

## Brand-specific notes

* Circuit breakers: the reseller often re-uses one series photo for several ampere ratings/poles. Variant images whose identical photo is also used for a different product are marked Medium (OK-REVIEW-RECOMMENDED) with the other SKUs named in Notes - the rating printed on the handle in the photo may differ from the SKU.
* Some Breaker Outlet photos carry a faint 'BREAKEROUTLET' watermark; they were kept (no image editing was allowed) and should be replaced if watermark-free images are required.

## Folder structure

`List_N/Cutler_Hammer/` images per original list (empty lists hold a marker file); `Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs.
