import json,pathlib,collections
W=pathlib.Path('/workspace/duplicate_qc_work');x=json.load(open(W/'review.json'));a=x['targets'][4500:5000];gids=json.load(open(W/'batch010_groups.json'));assert len(gids)==126 and len(a)==500
for t in a:
 k=gids.index(t['group_id']);t.update(review_part='Part_010',batch_review_level='group_visual_screen_plus_catalog_metadata_not_full_technical_QC',batch_review_basis={'group_screen_index':k,'same_sha_members_verified':True,'catalog_matches':len(t.get('catalog_evidence',[])),'source_metadata_not_independent_technical_validation':True})
 if t['decision']!='pending':continue
 if t['brand']=='Morris' and ('not one named for this exact SKU' in t['source'].get('Notes','') or k in [4,11,12,17,18,19,20,21,22,25,26,58]):
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: عکس خانواده SKU دیگر یا چند جزء/نمای ترکیبی و کابل بریده‌شده است. قطر، رزوه، سوراخ، اندازه اتصال و نوشته دقیق SKU روشن نیست؛ بازطراحی فنی از شماره SKU حدس زده نشد. این ثبت الزاماً به معنی خرابی همه تصاویر گروه نیست.')
 elif k in [102,103,123]:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: عکس عمومی Nora با نام خانواده و کد تعداد/پرداخت متفاوت به اشتراک گذاشته شده؛ تعداد سرها، ترکیب قطعات یا محدوده پرداخت دقیق از داده موجود قابل تأیید نیست. تعداد سر یا رنگ از پسوند SKU به تنهایی تغییر داده نشد.')

 else:
  t.update(decision='screened_no_obvious_mismatch',visual_review='batch_group_visual_and_metadata_screened_technical_QC_pending',review_note='عکس گروه و داده‌های موجود غربال شدند و ناسازگاری آشکارِ قابل اصلاح دیگری با مرجع معتبر در این مرحله مشخص نشد. اصلاح طول/رنگ/اثر اضافه فقط برای SKUهای دارای شاهد مشخص، جدا ثبت شد. این غربال، تأیید کیفیت ریزجزئیات، CCT، پرتو، اندازه، نوشته‌ها یا اجزای اضطراری و اتصالات نیست؛ QC دقیق همان SKU هنوز لازم است.')
json.dump(x,open(W/'review.json','w'),ensure_ascii=False,indent=2);print(dict(collections.Counter(t['decision'] for t in a)))
