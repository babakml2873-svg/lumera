import json,pathlib,collections
W=pathlib.Path('/workspace/duplicate_qc_work');x=json.load(open(W/'review.json'));a=x['targets'][6500:6622];gids=json.load(open(W/'batch014_groups.json'));assert len(gids)==34 and len(a)==122
for t in a:
 k=gids.index(t['group_id']);t.update(review_part='Part_014',batch_review_level='group_visual_screen_plus_catalog_metadata_not_full_technical_QC',batch_review_basis={'group_screen_index':k,'same_sha_members_verified':True,'catalog_matches':len(t.get('catalog_evidence',[])),'source_metadata_not_independent_technical_validation':True})
 if t['decision']!='pending':continue
 if k in [0,1,3,4,6,9,11,13,15,16,18,19,20,22,23,24,31,32,33] or k>=26 and k<=30:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: تصویر چند مدل/چند طول/سایز یا مشخصات و رنگ مشترک است؛ نسبت ابعاد، تعداد سوراخ، رزوه، چیدمان یا محدوده پرداخت دقیق SKU از مرجع موجود تأیید نمی‌شود. عکس کامل همان سایز/پیکربندی و مدرک مشخصات لازم است؛ اجزا یا عدد و برند جدید حدس زده نشد.')

 else:
  t.update(decision='screened_no_obvious_mismatch',visual_review='batch_group_visual_and_metadata_screened_technical_QC_pending',review_note='عکس گروه و داده‌های موجود غربال شدند و ناسازگاری آشکارِ قابل اصلاح دیگری با مرجع معتبر در این مرحله مشخص نشد. اصلاح طول/رنگ/اثر اضافه فقط برای SKUهای دارای شاهد مشخص، جدا ثبت شد. این غربال، تأیید کیفیت ریزجزئیات، CCT، پرتو، اندازه، نوشته‌ها یا اجزای اضطراری و اتصالات نیست؛ QC دقیق همان SKU هنوز لازم است.')
json.dump(x,open(W/'review.json','w'),ensure_ascii=False,indent=2);print(dict(collections.Counter(t['decision'] for t in a)))
