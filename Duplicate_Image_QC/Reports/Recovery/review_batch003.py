import json,pathlib,collections
W=pathlib.Path('/workspace/duplicate_qc_work');x=json.load(open(W/'review.json'));a=x['targets'][1000:1500];gids=json.load(open(W/'batch003_groups.json'));assert len(gids)==51 and len(a)==500
for t in a:
 k=gids.index(t['group_id']);t.update(review_part='Part_003',batch_review_level='group_visual_screen_plus_catalog_metadata_not_full_technical_QC',batch_review_basis={'group_screen_index':k,'same_sha_members_verified':True,'catalog_matches':len(t.get('catalog_evidence',[])),'source_metadata_not_independent_technical_validation':True})
 if t['decision']!='pending':continue
 t.update(decision='screened_no_obvious_mismatch',visual_review='batch_group_visual_and_metadata_screened_technical_QC_pending',review_note='تصویر مشترک گروه و مشخصات موجود غربال شدند؛ رنگ و شکل کلی ایراد آشکارِ قابل اصلاح با مرجع معتبر نشان نداد. برای طول‌های ساقه که در عنوان صریح بودند، تلاش جدا ثبت شد. شباهت عکس به‌تنهایی خطا نیست؛ CCT، توان، پرتو، رنگ دقیق، لنز و تعداد اجزای ریز هر SKU هنوز باید در QC دقیق تطبیق شوند. این غربال گروهی، پذیرش استفاده یا تأیید فنی کامل نیست.')
json.dump(x,open(W/'review.json','w'),ensure_ascii=False,indent=2);print(dict(collections.Counter(t['decision'] for t in a)))
