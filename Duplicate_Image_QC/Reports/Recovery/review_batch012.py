import json,pathlib,collections
W=pathlib.Path('/workspace/duplicate_qc_work');x=json.load(open(W/'review.json'));a=x['targets'][5500:6000];gids=json.load(open(W/'batch012_groups.json'));assert len(gids)==174 and len(a)==500
for t in a:
 k=gids.index(t['group_id']);t.update(review_part='Part_012',batch_review_level='group_visual_screen_plus_catalog_metadata_not_full_technical_QC',batch_review_basis={'group_screen_index':k,'same_sha_members_verified':True,'catalog_matches':len(t.get('catalog_evidence',[])),'source_metadata_not_independent_technical_validation':True})
 if t['decision']!='pending':continue
 if k in [23,34,112] or k>=120 and k<=167:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: مرجع بریده/نقشه‌ای یا عکس کلید حفاظتی دارای نوشته و آمپراژ/کنتاکت مدل دیگر است. برای برخی عکس‌ها شماره چاپ‌شده با SKU یکسان نیست یا واترمارک روی جزئیات افتاده؛ مشخصات هر SKU باید جدا تأیید شود. بازسازی رقم، برچسب، تعداد پل و اتصال از کد SKU حدس زده نشد؛ این وضعیت اثبات ایراد همه اعضای گروه نیست.')
 elif k==45:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: عکس NT-348 میان چند SKU مشترک است و مشخصات دقیق رنگ/اجزای اتصال هر SKU در داده موجود روشن نیست. رنگ از پسوند به تنهایی حدس زده نشد.')

 else:
  t.update(decision='screened_no_obvious_mismatch',visual_review='batch_group_visual_and_metadata_screened_technical_QC_pending',review_note='عکس گروه و داده‌های موجود غربال شدند و ناسازگاری آشکارِ قابل اصلاح دیگری با مرجع معتبر در این مرحله مشخص نشد. اصلاح طول/رنگ/اثر اضافه فقط برای SKUهای دارای شاهد مشخص، جدا ثبت شد. این غربال، تأیید کیفیت ریزجزئیات، CCT، پرتو، اندازه، نوشته‌ها یا اجزای اضطراری و اتصالات نیست؛ QC دقیق همان SKU هنوز لازم است.')
json.dump(x,open(W/'review.json','w'),ensure_ascii=False,indent=2);print(dict(collections.Counter(t['decision'] for t in a)))
