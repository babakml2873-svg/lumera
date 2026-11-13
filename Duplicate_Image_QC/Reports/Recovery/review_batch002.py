import json,pathlib,collections
W=pathlib.Path('/workspace/duplicate_qc_work');x=json.load(open(W/'review.json'));a=x['targets'][500:1000];gids=json.load(open(W/'batch002_groups.json'));assert len(gids)==88 and len(a)==500
for t in a:
 k=gids.index(t['group_id']);t.update(review_part='Part_002',batch_review_level='group_visual_screen_plus_catalog_metadata_not_full_technical_QC',batch_review_basis={'group_screen_index':k,'same_sha_members_verified':True,'catalog_matches':len(t.get('catalog_evidence',[])),'source_metadata_not_independent_technical_validation':True})
 if t['decision']!='pending':continue
 if k in [59,60,61,62]:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: تصویر فقط برش نمونه‌ای از نوار LED با مدار و نوشته‌های فنی است. انتهاها، طول کامل و هندسه مجموعه محصول در مرجع حاضر نیست؛ از ساخت قرقره، افزودن LED یا اتصالات/نوشته حدسی خودداری شد. این وضعیت به‌معنی اثبات خطای تمام عکس‌های نمونه در گروه نیست.')
 else:
  t.update(decision='screened_no_obvious_mismatch',visual_review='batch_group_visual_and_metadata_screened_technical_QC_pending',review_note='تصویر گروه و داده‌های موجود غربال شدند؛ رنگ و شکل کلی ایراد آشکارِ قابل اصلاح با مرجع معتبر نشان نداد. برای ساقه‌های دارای طول صریح در عنوان، کاندید جدا تولید شد. اختلاف CCT/توان/پرتو به‌تنهایی اثبات اختلاف ظاهری نیست؛ لنز، ابعاد، اتصالات و ریزجزئیات هر SKU همچنان نیازمند QC دقیق‌اند. این غربال، تأیید فنی یا پذیرش استفاده از عکس نیست.')
json.dump(x,open(W/'review.json','w'),ensure_ascii=False,indent=2);print(dict(collections.Counter(t['decision'] for t in a)))
