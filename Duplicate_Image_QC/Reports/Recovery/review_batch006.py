import json,pathlib,collections
W=pathlib.Path('/workspace/duplicate_qc_work');x=json.load(open(W/'review.json'));a=x['targets'][2500:3000];gids=json.load(open(W/'batch006_groups.json'));assert len(gids)==183 and len(a)==500
for t in a:
 k=gids.index(t['group_id']);t.update(review_part='Part_006',batch_review_level='group_visual_screen_plus_catalog_metadata_not_full_technical_QC',batch_review_basis={'group_screen_index':k,'same_sha_members_verified':True,'catalog_matches':len(t.get('catalog_evidence',[])),'source_metadata_not_independent_technical_validation':True})
 if t['decision']!='pending':continue
 if k in [5,6,7,8,11,14,26]:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: عکس عمومی Trimless/تریم یا مجموعه با اپتیک متفاوت، مرز واقعی پرداخت یا اجزای اپتیک همان SKU را روشن نمی‌کند. بخش سفید ممکن است فضای خالی باشد. برای تفاوت پرتو، رنگ‌کردن عکس عمومی یا افزودن لنز حدسی انجام نشد.')
 elif k in [12,19,20,21,22,28,29,30,77,94,95,110,111,112,113,114,115,116,119,120,121,122,123,124,125,127,128,129,130,131,132,134,135,136,137,140,141,142,143,144,145,147,148,149,150,151,153,154,155,156,157,158,161,162,163,174,175,176]:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: عکس فقط بخشی از محصول/انتهای بریده‌شده، نصب محیطی، طول کابل/زنجیر نامشخص یا تصویر خانواده با نوشته و اتصالات تأییدنشده را نشان می‌دهد. مرجع کامل همان SKU برای تکمیل هندسه و نوشته‌ها لازم است؛ اجزای پنهان حدس زده نشد.')
 elif k in [36,49,50,74,75,76,93]:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: چند قطعه/نما در یک تصویر یا اجزای جدا دیده می‌شود. نمای تک‌محصول مونتاژشده و تعیین اجزای دقیق SKU لازم است؛ مونتاژ یا محل اتصال حدس زده نشد.')

 else:
  t.update(decision='screened_no_obvious_mismatch',visual_review='batch_group_visual_and_metadata_screened_technical_QC_pending',review_note='عکس گروه و داده‌های موجود غربال شدند و ناسازگاری آشکارِ قابل اصلاح دیگری با مرجع معتبر در این مرحله مشخص نشد. اصلاح طول/رنگ/اثر اضافه فقط برای SKUهای دارای شاهد مشخص، جدا ثبت شد. این غربال، تأیید کیفیت ریزجزئیات، CCT، پرتو، اندازه، نوشته‌ها یا اجزای اضطراری و اتصالات نیست؛ QC دقیق همان SKU هنوز لازم است.')
json.dump(x,open(W/'review.json','w'),ensure_ascii=False,indent=2);print(dict(collections.Counter(t['decision'] for t in a)))
