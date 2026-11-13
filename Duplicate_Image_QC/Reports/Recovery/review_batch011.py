import json,pathlib,collections
W=pathlib.Path('/workspace/duplicate_qc_work');x=json.load(open(W/'review.json'));a=x['targets'][5000:5500];gids=json.load(open(W/'batch011_groups.json'));assert len(gids)==114 and len(a)==500
for t in a:
 k=gids.index(t['group_id']);t.update(review_part='Part_011',batch_review_level='group_visual_screen_plus_catalog_metadata_not_full_technical_QC',batch_review_basis={'group_screen_index':k,'same_sha_members_verified':True,'catalog_matches':len(t.get('catalog_evidence',[])),'source_metadata_not_independent_technical_validation':True})
 if t['decision']!='pending':continue

 if True:
  t.update(decision='screened_no_obvious_mismatch',visual_review='batch_group_visual_and_metadata_screened_technical_QC_pending',review_note='عکس گروه و داده‌های موجود غربال شدند و ناسازگاری آشکارِ قابل اصلاح دیگری با مرجع معتبر در این مرحله مشخص نشد. در این پارت ایراد ظاهری قابل اصلاحِ دیگری با شاهد مشخص تأیید نشد؛ عکس مشترک CCT/درایور/اضطراری به تنهایی اثبات ایراد نیست. نبود داده دقیق اپتیک و اجزای اضطراری، محدودیت این غربال است. این غربال، تأیید کیفیت ریزجزئیات، CCT، پرتو، اندازه، نوشته‌ها یا اجزای اضطراری و اتصالات نیست؛ QC دقیق همان SKU هنوز لازم است.')
json.dump(x,open(W/'review.json','w'),ensure_ascii=False,indent=2);print(dict(collections.Counter(t['decision'] for t in a)))
