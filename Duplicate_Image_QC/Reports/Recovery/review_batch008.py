import json,pathlib,collections
W=pathlib.Path('/workspace/duplicate_qc_work');x=json.load(open(W/'review.json'));a=x['targets'][3500:4000];gids=json.load(open(W/'batch008_groups.json'));assert len(gids)==176 and len(a)==500
for t in a:
 k=gids.index(t['group_id']);t.update(review_part='Part_008',batch_review_level='group_visual_screen_plus_catalog_metadata_not_full_technical_QC',batch_review_basis={'group_screen_index':k,'same_sha_members_verified':True,'catalog_matches':len(t.get('catalog_evidence',[])),'source_metadata_not_independent_technical_validation':True})
 if t['decision']!='pending':continue
 if t['brand']=='Leviton' and ('not one named for this exact SKU' in t['source'].get('Notes','') or k in [74,75,76,77]):
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: تصویر سری/خانواده یا کابل بریده و نوشته‌های فنی دارد؛ شکل، نوشته و اتصالات دقیق SKU از مدارک موجود قابل تأیید نیست. رتبه فنی و اتصال حدس زده نشد.')
 elif k in [102,105,106,107,110,111,112,113,114,115,139] or k>=152:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: تصویر ترکیبی/چند نما/کیت، نوار یا کابل ناقص، یا عکس مشترک برای طول و ساختار متفاوت دیده شد. برای ساخت نمای تک‌محصول کامل و تعیین اجزای اتصال، طول و نوشته‌ها، عکس یا نقشه دقیق SKU لازم است؛ اجزای پنهان و مونتاژ حدس زده نشد.')

 else:
  t.update(decision='screened_no_obvious_mismatch',visual_review='batch_group_visual_and_metadata_screened_technical_QC_pending',review_note='عکس گروه و داده‌های موجود غربال شدند و ناسازگاری آشکارِ قابل اصلاح دیگری با مرجع معتبر در این مرحله مشخص نشد. اصلاح طول/رنگ/اثر اضافه فقط برای SKUهای دارای شاهد مشخص، جدا ثبت شد. این غربال، تأیید کیفیت ریزجزئیات، CCT، پرتو، اندازه، نوشته‌ها یا اجزای اضطراری و اتصالات نیست؛ QC دقیق همان SKU هنوز لازم است.')
json.dump(x,open(W/'review.json','w'),ensure_ascii=False,indent=2);print(dict(collections.Counter(t['decision'] for t in a)))
