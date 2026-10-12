# Siemens — product images

Brand Siemens: 184 SKUs in the product lists. Variant images were delivered for **138 SKUs (75.0%)**, plus **138 gallery images** (max 4 per SKU).

| List | SKUs | Variant images | Gallery images |
|---|---|---|---|
| List_1 | 0 | 0 | 0 |
| List_2 | 184 | 138 | 138 |
| List_3 | 0 | 0 | 0 |
| List_4 | 0 | 0 | 0 |

* 60 of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.
* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.
* Image sources (files): breakeroutlet.com (276). No Lumera Electric source was used.

## Sources searched

Official catalogs (Siemens SiePortal / Schneider Electric se.com) return HTTP 403 (Akamai) from this environment; SupplyHouse/Standard/Crescent are Cloudflare-blocked. Used Breaker Outlet (breakeroutlet.com, Shopify surplus/new reseller - not an authorized distributor) vendor-filtered catalog; exact variant SKU match, refurbished '-R' variants excluded. Some listings show a family image of the same breaker series.

## Matching rules

* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source links to that SKU — or the product's main image when the product has one variant or its variants differ only in non-visual options (colour temperature, wattage, voltage, beam, length…).
* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).
* Gallery images (G) come from the same product; images the source links to a different variant are never used.
* A random sample of variant images was checked visually for product identity.

## SKUs without a variant image — reasons

| Reason | SKUs |
|---|---|
| No exact SKU match in the harvested source catalog(s) | 46 |

## Brand-specific notes

* Circuit breakers: the reseller often re-uses one series photo for several ampere ratings/poles. Variant images whose identical photo is also used for a different product are marked Medium (OK-REVIEW-RECOMMENDED) with the other SKUs named in Notes - the rating printed on the handle in the photo may differ from the SKU.
* Some Breaker Outlet photos carry a faint 'BREAKEROUTLET' watermark; they were kept (no image editing was allowed) and should be replaced if watermark-free images are required.

## Folder structure

`List_N/Siemens/` images per original list (empty lists hold a marker file); `Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs.
