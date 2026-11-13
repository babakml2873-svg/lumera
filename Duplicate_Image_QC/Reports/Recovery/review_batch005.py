import json,pathlib,collections
W=pathlib.Path('/workspace/duplicate_qc_work');x=json.load(open(W/'review.json'));a=x['targets'][2000:2500];gids=json.load(open(W/'batch005_groups.json'));assert len(gids)==154 and len(a)==500
for t in a:
 k=gids.index(t['group_id']);t.update(review_part='Part_005',batch_review_level='group_visual_screen_plus_catalog_metadata_not_full_technical_QC',batch_review_basis={'group_screen_index':k,'same_sha_members_verified':True,'catalog_matches':len(t.get('catalog_evidence',[])),'source_metadata_not_independent_technical_validation':True})
 if t['decision']!='pending':continue
 if k in [9,106,120,121,122,123,124,130]:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: فقط قطعه بریده‌شده نوار LED دیده می‌شود؛ طول کامل، انتهاها و اتصالات دقیق SKU از این عکس معلوم نیست و بازسازی مجموعه کامل حدسی است.')
 elif k in [0,30,48,49,50,90,135]:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: تصویر انفجاری، نقشه یا ترکیب چند جزء/پرداخت است. نمای واقعی تک‌محصول و مرجع دقیق اتصال یا رنگ همین SKU لازم است؛ مونتاژ و انتخاب اجزای مبهم حدس زده نشد.')
 elif k in [26,39,86,89,110]:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: اختلاف طول یا مدل در داده‌ها ثبت شده ولی عکس عمومی/برش‌خورده برای نسبت ابعاد، انتهای محصول یا نوع دقیق آویز کافی نیست. برای ساخت بدون تغییر حدسی هندسه، مرجع ابعادی همان SKU لازم است.')
 elif k in [42,67,131] or t['sku']=='EP850BZ':
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: ناسازگاری یا ابهام پرداخت دیده شد؛ عنوان رنگ، مرز دقیق رنگ قطعات دیگر/رینگ/بازو/کابل را مشخص نمی‌کند. برای رنگ‌آمیزی بدون تغییر جنس اجزای نامرتبط، مرجع همین پرداخت لازم است.')
 elif k==20:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: عکس مشترک EC840 برای مدل‌های EC841 و آمپراژهای دیگر نیز استفاده شده؛ نوع مسیر اتصال/فیوز و نوشته کلید همان SKU از این مرجع تأیید نمی‌شود. اصلاح رنگ به‌تنهایی اختلاف فنی را رفع نمی‌کند.')

 else:
  t.update(decision='screened_no_obvious_mismatch',visual_review='batch_group_visual_and_metadata_screened_technical_QC_pending',review_note='عکس گروه و داده‌های موجود غربال شدند و ناسازگاری آشکارِ قابل اصلاح دیگری با مرجع معتبر در این مرحله مشخص نشد. اصلاح طول/رنگ/اثر اضافه فقط برای SKUهای دارای شاهد مشخص، جدا ثبت شد. این غربال، تأیید کیفیت ریزجزئیات، CCT، پرتو، اندازه، نوشته‌ها یا اجزای اضطراری و اتصالات نیست؛ QC دقیق همان SKU هنوز لازم است.')
json.dump(x,open(W/'review.json','w'),ensure_ascii=False,indent=2);print(dict(collections.Counter(t['decision'] for t in a)))
