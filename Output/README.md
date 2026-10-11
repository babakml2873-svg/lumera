# FIRST BRAND — ABBA Lighting: product images

Brand processed: **ABBA Lighting**. It is first in the deterministic order (all 44 brands sorted alphabetically, case-insensitive).
No other brand has been started.

## Results (actual counts)

| | List_1 | List_2 | List_3 | List_4 | Total |
|---|---|---|---|---|---|
| ABBA SKUs in list | 173 | 0 | 0 | 183 | **356** |
| SKUs with a verified Variant image (`-V.jpg`) | 158 | – | – | 170 | **328 (92.1%)** |
| Gallery images (`-G-NN.jpg`) | 694 | – | – | 914 | **1,608** |
| SKUs with no Variant image (manual review) | 15 | – | – | 13 | **28** |
| SKUs with no image at all | 4 | – | – | 6 | **10** |

* No SKU appears in more than one list for this brand, so there are no cross-list duplicates.
* 34 of the 328 Variant images are **Medium** confidence. They are marked `OK-REVIEW-RECOMMENDED`; see `Reports/review_queue.csv`.
* All 1,936 files were checked by script: exactly 800×800 px, JPEG, ≤ 100,000 bytes (largest 99,913 B, average 70 KB). Every file follows the `SKU-V.jpg` / `SKU-G-NN.jpg` naming. No identical files exist within a SKU, and near-duplicates were removed by perceptual hash (pHash distance ≤ 6).

## Folder structure

```
List_1/ABBA_Lighting/   SKU-V.jpg, SKU-G-01.jpg … (List 1 products)
List_2/ABBA_Lighting/   empty – list has no ABBA products (marker file)
List_3/ABBA_Lighting/   empty – list has no ABBA products (marker file)
List_4/ABBA_Lighting/   (List 4 products)
Reports/
  image_report.csv          one row per image (List, Brand, SKU, Image_Type, Filename, Source_URL,
                            Match_Confidence, Status, Notes) + Source_Page, Source_Site, pixels, bytes, JPEG quality
  brand_progress.csv        brand totals
  missing_images.csv        every SKU missing a V and/or G image, with reason and search attempts
  sku_filename_mapping.csv  original SKU -> normalized SKU -> output path
  review_queue.csv          Medium-confidence V images + missing V images, for manual review
```

SKU normalization: `/` → `-`, and spaces and characters not allowed in filenames are removed (e.g. `MR16 3W-5K` → `MR163W-5K`). No filename collisions occurred.

## Sources

* **1,931 images** come from **abbalightingusa.com**, the official ABBA Lighting USA site. Images were taken from its product catalog API in original resolution (WordPress `/wp-content/uploads/` originals, not thumbnails).
* **5 images** come from ABBA resellers, used only where the official site no longer lists the item:
  * Sonic Electric: STB18-DB and STB18-NB, exact variant SKUs with SKU-linked images, plus 1 dimension drawing each.
  * Kings Outdoor Lighting: CDPSR59-SS, an exact variant SKU.
* **No Lumera Electric site, CDN or mirrored asset was used.** Every URL was checked for this by assertion.

## How Variant (V) vs Gallery (G) was decided

* **V** is used only when the exact SKU is verified. That means one of the following, and in every case the image was also checked visually for the right model and finish:
  * an exact official variation SKU,
  * an official variation whose finish/CCT/length attributes equal the SKU code,
  * a single-SKU official product,
  * an exact reseller variant SKU.
* ABBA's own site has errors. These were caught by visual review and **not** copied:
  * `MR16-Red` shows a blue bulb.
  * Some "Black" variants show brown units (DL01, DL02), and "Stainless" shows black (STA07).
  * Some variants use images of other models: BA15S on BA15D, PL54 on PL15, DM52 slides on UNB pages, and others.

  Where an official image of the correct finish existed, it replaced the wrong one (Medium confidence). Where none existed, V was withheld.
* **G** images come from the same official product page. Images naming another model are dropped. For products sold in several finishes, every gallery image was tagged by finish by eye, and a SKU only gets images of its own finish (or finish-neutral dimension drawings). ABBA's filenames are not reliable for finish: for example, STB19 files named "BLACK" show white units.
* Gallery order follows the brief: white-background product shots, then lifestyle/photographic, then other images (graphics, drawings). Maximum 6 per SKU.

## Image processing

* Each image is resized to fit inside 800×800 with its aspect ratio kept, then padded to a square. Nothing is cropped or distorted.
* The padding colour is the image's own border colour. Backgrounds are never removed or whitened.
* 526 source files were transparent PNG cut-outs, which have no background. These were flattened onto white, as JPG requires, and this is noted per image.
* 98 images were upscaled because the best verified source was smaller than 800 px (mostly 500–750 px). Each is flagged in Notes with its scale factor. Nothing under 400 px was used: the 150 px official FPBCC04-DB image was rejected.
* JPEG quality was chosen per image as the highest that fits under 100 KB (progressive, optimized).

## Not delivered (28 SKUs without V): reason summary

| SKU(s) | Reason |
|---|---|
| SL102-RGB | Not an ABBA product found anywhere (SL102 results are other brands) |
| BP1-Wh, STB19-Bz | That finish is not offered for the model (official site and resellers) |
| E27-RGB, SL101-3K | Ambiguous identity (RGB vs RGBW bulb; string light vs replacement bulb) |
| CDPA52-Bk/Br, PLB01-DB | Official listing has no finish options, so the finish image cannot be identified |
| PLB10 | Official PLB10 page only shows PLB07 images |
| PL15 (7 SKUs) | Official PL15 page has only drawings/diagrams; its product photos are of the PL54 |
| SLGC111 | Only a dimension drawing exists |
| STB15-DB/NB, BPE24-DB/NB, PS6-Bk/Br, BR2-DB/NB, BRL2-DB/NB, UNB06-Bk | Finishes share one image or are visibly inconsistent, so the finish cannot be verified |

## Reproduce / resume

Scripts are in `scripts/` at the repository root:

1. `abba_plan.py` builds the SKU plan.
2. `abba_download.py` is a cached, resumable downloader. It skips files already downloaded.
3. `abba_process.py` produces the 800×800 output and applies the visual-review overrides and finish tags kept in `work/abba/`.
4. `abba_reports.py` writes the reports and runs validation.
