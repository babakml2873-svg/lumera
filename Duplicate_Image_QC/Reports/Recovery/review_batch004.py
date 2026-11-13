import json,pathlib,collections
W=pathlib.Path('/workspace/duplicate_qc_work');x=json.load(open(W/'review.json'));a=x['targets'][1500:2000];gids=json.load(open(W/'batch004_groups.json'));assert len(gids)==70 and len(a)==500
for t in a:
 k=gids.index(t['group_id']);t.update(review_part='Part_004',batch_review_level='group_visual_screen_plus_catalog_metadata_not_full_technical_QC',batch_review_basis={'group_screen_index':k,'same_sha_members_verified':True,'catalog_matches':len(t.get('catalog_evidence',[])),'source_metadata_not_independent_technical_validation':True})
 if t['decision']!='pending':continue
 if k in [22,33,34]:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: تصویر صرفاً برش نوار LED است و محصول کامل/انتهاها یا حلقه با طول و اتصالات دقیق را نشان نمی‌دهد. ساخت مجموعه کامل یا تکمیل مدار و تعداد اجزا از این نمونه، حدسی خواهد بود.')
 elif k in [23,69]:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: تصویر کیت، اجزای جداشده را در یک چیدمان انفجاری/ترکیبی نشان می‌دهد. برای تولید یک نمای محصول مونتاژشده، موقعیت و اتصال دقیق اجزا از مرجع فعلی قابل تأیید نیست. عکس واقعیِ مجموعه و تطبیق اجزای عادی/اضطراری هر SKU لازم است؛ اتصال یا قطعه حدسی اضافه نشد.')
 else:
  t.update(decision='screened_no_obvious_mismatch',visual_review='batch_group_visual_and_metadata_screened_technical_QC_pending',review_note='عکس گروه و داده‌های موجود غربال شدند و ناسازگاری آشکارِ قابل اصلاح دیگری با مرجع معتبر در این مرحله مشخص نشد. اصلاح طول/رنگ/اثر اضافه فقط برای SKUهای دارای شاهد مشخص، جدا ثبت شد. این غربال، تأیید کیفیت ریزجزئیات، CCT، پرتو، اندازه، نوشته‌ها یا اجزای اضطراری و اتصالات نیست؛ QC دقیق همان SKU هنوز لازم است.')
json.dump(x,open(W/'review.json','w'),ensure_ascii=False,indent=2);print(dict(collections.Counter(t['decision'] for t in a)))
