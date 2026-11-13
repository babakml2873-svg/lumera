import json,pathlib,collections
W=pathlib.Path('/workspace/duplicate_qc_work');x=json.load(open(W/'review.json'));a=x['targets'][6000:6500];gids=json.load(open(W/'batch013_groups.json'));assert len(gids)==122 and len(a)==500
for t in a:
 k=gids.index(t['group_id']);t.update(review_part='Part_013',batch_review_level='group_visual_screen_plus_catalog_metadata_not_full_technical_QC',batch_review_basis={'group_screen_index':k,'same_sha_members_verified':True,'catalog_matches':len(t.get('catalog_evidence',[])),'source_metadata_not_independent_technical_validation':True})
 if t['decision']!='pending':continue
 if t['brand']=='Utopia Lighting':
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: عکس نصب‌شده یا بریده‌شده/چندنما، طول کامل و انتهاها و اجزای آویز/سقفی همان SKU را نشان نمی‌دهد؛ برای برخی عکس‌ها رنگ ثبت‌شده با ظاهر عکس هم مبهم است. تغییر طول، جنس و پرداخت یا تکمیل محصول از یک بخش عمومی حدسی خواهد بود. عکس یا نقشه کامل لازم است.')
 elif k in [112,113] or t['sku'] in ['LVB-24-MCT-BN','LVB-24-MCT-PC','BOL-G8-100Q-MCTP-BK-WH','BOL-G8-100Q-MCTP-BR-WH']:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: تصویر مشترک/تقریباً هم‌نسبت برای طول‌های 24 و 42 یا 18 و 24 اینچ، یا پیکربندی دو رنگ استفاده شده است. نسبت ابعاد و محدوده دقیق رنگ از داده موجود تأیید نمی‌شود؛ تغییر رنگ تنها کافی نیست. نقشه ابعادی و نمای پیکربندی همان SKU لازم است.')
 elif k==118:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: پایه زیر محصول بریده شده و طول و اتصال کامل دقیق دیده نمی‌شود. تکمیل پایه از این کادر حدسی خواهد بود.')

 else:
  t.update(decision='screened_no_obvious_mismatch',visual_review='batch_group_visual_and_metadata_screened_technical_QC_pending',review_note='عکس گروه و داده‌های موجود غربال شدند و ناسازگاری آشکارِ قابل اصلاح دیگری با مرجع معتبر در این مرحله مشخص نشد. اصلاح طول/رنگ/اثر اضافه فقط برای SKUهای دارای شاهد مشخص، جدا ثبت شد. این غربال، تأیید کیفیت ریزجزئیات، CCT، پرتو، اندازه، نوشته‌ها یا اجزای اضطراری و اتصالات نیست؛ QC دقیق همان SKU هنوز لازم است.')
json.dump(x,open(W/'review.json','w'),ensure_ascii=False,indent=2);print(dict(collections.Counter(t['decision'] for t in a)))
