import json,pathlib,collections
W=pathlib.Path('/workspace/duplicate_qc_work');x=json.load(open(W/'review.json'));a=x['targets'][4000:4500];gids=json.load(open(W/'batch009_groups.json'));assert len(gids)==113 and len(a)==500
for t in a:
 k=gids.index(t['group_id']);t.update(review_part='Part_009',batch_review_level='group_visual_screen_plus_catalog_metadata_not_full_technical_QC',batch_review_basis={'group_screen_index':k,'same_sha_members_verified':True,'catalog_matches':len(t.get('catalog_evidence',[])),'source_metadata_not_independent_technical_validation':True})
 if t['decision']!='pending':continue
 if k<13:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: تصویر چند جزء کیت و نوشته فنی است؛ اتصال دقیق و تعداد/نسخه اجزای همان SKU برای ساخت نمای مونتاژشده روشن نیست و قطعه/نوشته حدس زده نشد.')
 elif t['brand']=='Lutron' and (t['sku'].endswith(('-HT','-TP','-BI','-MN','-PD')) or k==34):
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: عکس سفید/عمومی یا سواچ جدا برای پرداخت اختصاصی Hot، Taupe، Biscuit، Midnight، Palladium یا سفیدهای متفاوت استفاده شده است. عنوان پرداخت موجود است اما نمونه رنگ معتبر و مرز پرداخت همان SKU در عکس روشن نیست؛ رنگ دقیق از نام یا کد حدس زده نشد.')
 elif t['brand']=='Morris' and 'not one named for this exact SKU' in t['source'].get('Notes',''):
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: داده منبع عکس خانواده برای SKU دیگری را اعلام می‌کند؛ قطر، تعداد رزوه و جزئیات اتصال دقیق این SKU روشن نیست. عکس مشابه به معنی تطبیق فنی نیست و ابعاد از شماره SKU حدس زده نشد.')

 else:
  t.update(decision='screened_no_obvious_mismatch',visual_review='batch_group_visual_and_metadata_screened_technical_QC_pending',review_note='عکس گروه و داده‌های موجود غربال شدند و ناسازگاری آشکارِ قابل اصلاح دیگری با مرجع معتبر در این مرحله مشخص نشد. اصلاح طول/رنگ/اثر اضافه فقط برای SKUهای دارای شاهد مشخص، جدا ثبت شد. این غربال، تأیید کیفیت ریزجزئیات، CCT، پرتو، اندازه، نوشته‌ها یا اجزای اضطراری و اتصالات نیست؛ QC دقیق همان SKU هنوز لازم است.')
json.dump(x,open(W/'review.json','w'),ensure_ascii=False,indent=2);print(dict(collections.Counter(t['decision'] for t in a)))
