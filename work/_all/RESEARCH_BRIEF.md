# Brand source research brief (for research agents)

Goal: for each assigned brand, find the BEST reliable source of product images that can be matched to the brand's SKUs
(sample SKUs are in work/_all/brands.json), and determine HOW to harvest it programmatically.

HARD RULE: never use Lumera Electric (lumeraelectric.com, its CDN, mirrors) as a source. Do not even fetch it.

Priority of sources: 1) official manufacturer site, 2) authorized distributor, 3) reputable retailer/catalog.

Use curl through the existing proxy with a browser User-Agent, e.g.
  curl -sS -m 30 -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36" -H "Accept: text/html,application/json;q=0.9,*/*;q=0.8" -H "Accept-Language: en-US,en;q=0.9" URL
(406/403 often disappear with full browser headers). Be polite: no more than ~2 requests/second per site, and do not
download images in bulk - this is research only (a handful of test requests per brand).

For each brand determine:
- official_site (URL) and whether it is reachable from here (HTTP status)
- platform & catalog endpoint, test in this order:
  * Shopify: GET {site}/products.json?limit=250&page=1  (and /products/<handle>.json) -> variants have sku + featured_image
  * WooCommerce: GET {site}/wp-json/wc/store/v1/products?per_page=100 (header X-WP-Total gives count; variations via /products/<id>)
  * BigCommerce / Magento / custom: look for sitemap.xml / product sitemaps, and whether product pages embed JSON-LD
    (application/ld+json with "@type":"Product", "sku", "image") or og:image; check a search URL that finds a SKU
  * any public JSON API the site's own front-end uses (e.g. search/autocomplete endpoints)
- total product count if knowable, and whether SKUs in the site match the format of the sample SKUs
- test: try to find 3 of the sample SKUs on the site (search endpoint or product page) and record the image URLs found
- if the official site is blocked/has no images: name 1-2 alternative authorized distributors/retailers with the same
  test (Shopify-based distributors are ideal because /products.json is machine readable)
- notes: anti-bot (Cloudflare/Akamai challenge), rate limits, image resolution, watermarks

Write ONE JSON file per brand to work/_all/sites/<Brand_Name_with_underscores>.json with keys:
  brand, official_site, reachable, platform, catalog_endpoint, est_products, sku_format_match (yes/partial/no + note),
  sample_tests: [{sku, found(bool), product_url, image_urls:[...] }],
  alternatives: [{name, url, platform, endpoint, tested(bool), notes}],
  recommended_strategy (short, concrete: which endpoint to harvest and how to match SKUs),
  blockers (string or null)
Keep each JSON factual: only record what you actually observed.
Finish with a 3-line-per-brand summary in your final message.
