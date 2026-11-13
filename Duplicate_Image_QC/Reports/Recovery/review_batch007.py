import json,pathlib,collections
W=pathlib.Path('/workspace/duplicate_qc_work');x=json.load(open(W/'review.json'));a=x['targets'][3000:3500];gids=json.load(open(W/'batch007_groups.json'));assert len(gids)==379 and len(a)==500
for t in a:
 k=gids.index(t['group_id']);t.update(review_part='Part_007',batch_review_level='group_visual_screen_plus_catalog_metadata_not_full_technical_QC',batch_review_basis={'group_screen_index':k,'same_sha_members_verified':True,'catalog_matches':len(t.get('catalog_evidence',[])),'source_metadata_not_independent_technical_validation':True})
 if t['decision']!='pending':continue
 if (t['brand']=='Leviton' and ('not one named for this exact SKU' in t['source'].get('Notes','') or k in [354,355,356,357,358,359,364,365])) or (t['brand']=='Intermatic' and k in [2,3,4,7,8,9,10]):
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: تصویر سری/خانواده یا محصول دارای نوشته/اتصال/چند رنگ است؛ رنگ و ولتاژ و چیدمان دقیق همین SKU در مدرک موجود روشن نیست. بازنویسی رتبه فنی، رنگ از کد SKU یا ساخت پین/کنتاکت حدس زده نشد. این وضعیت الزاماً به معنی خرابی همه عکس‌های گروه نیست.')
 elif k in [21,22,23,24,36,42,43,56,91,93,94,101,104,105,107,108,109,110,111,112,113,114,115,127,129,130,132,133,134,136,137,138,140,142,158,163,164,165,166,167,213,214,220,252,253,254,264,265,266,282,283,284,285,287,288,289,290,291,292]:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: بخشی از آویز/سقفی/کابل/میله از کادر خارج است؛ نمای کامل همان مدل و اتصالات برای تکمیل بدون حدس لازم است. عکس دیگرِ صرفاً مشابه یا پرداخت دارای رینگ اضافی جایگزین ساختار این SKU محسوب نشد.')

 else:
  t.update(decision='screened_no_obvious_mismatch',visual_review='batch_group_visual_and_metadata_screened_technical_QC_pending',review_note='عکس گروه و داده‌های موجود غربال شدند و ناسازگاری آشکارِ قابل اصلاح دیگری با مرجع معتبر در این مرحله مشخص نشد. اصلاح طول/رنگ/اثر اضافه فقط برای SKUهای دارای شاهد مشخص، جدا ثبت شد. این غربال، تأیید کیفیت ریزجزئیات، CCT، پرتو، اندازه، نوشته‌ها یا اجزای اضطراری و اتصالات نیست؛ QC دقیق همان SKU هنوز لازم است.')
json.dump(x,open(W/'review.json','w'),ensure_ascii=False,indent=2);print(dict(collections.Counter(t['decision'] for t in a)))
