# Reports

Overall_report.csv and Latest_variant_status.csv contain current repository image paths. Category_brand_index.csv links to the new category/brand folders. Organization_manifest.csv maps every previous image path to its current path.

Parts/ contains historical per-part reports, with image paths updated to the current layout. Parts_summary.csv retains links and commits on the previous generated-variants-20261106 branch for historical traceability.

Recovery_State/bootstrap.zip is an unchanged historical generation-recovery snapshot from before this layout change. Its embedded scripts and paths belong to that older workflow and must not be restarted for the reorganized tree. Current output paths are in Overall_report.csv.
