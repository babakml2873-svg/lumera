import json,pathlib,collections,re
W=pathlib.Path('/workspace/duplicate_qc_work');x=json.load(open(W/'review.json'));a=x['targets'][:500];gids=json.load(open(W/'batch001_groups.json'))
# These 203 group images were inspected in 11 comparison sheets in this session.
assert len(gids)==203 and len(a)==500
issues={}
for k in range(80,91):issues[k]='تصویر خانوادگی کلید حفاظتی/لامپ دارای نوشته یا مشخصات ظاهری است، اما مشخصات و برچسب دقیق این SKU از مرجع قابل تأیید نیست. برای کلیدها، شماره‌های نمایانِ مرجع برای همه اعضای گروه یکسان‌اند؛ از بازنویسی برچسب فنی یا شماره آمپر بدون سند دقیق خودداری شد.'
issues[94]='مرجع صرفاً ترسیم خطی لامپ است. ساختار و مواد واقعی قطعات داخلی لامپ در این فایل مشخص نیست؛ از تبدیل نقاشی عمومی به عکسِ جزئیات حدسی خودداری شد.'
for k in [114,117,145,146,147,185]:issues[k]='مرجع تنها قطعه‌ای بریده از نوار/ریل را نشان می‌دهد؛ انتهاها، طول کامل و آرایش دقیق مجموعه در این تصویر حاضر نیست. نمایش محصول کامل بدون مرجع کل محصول نیازمند حدس تعداد اجزا و اتصالات است.'
issues[157]='مرجع، تصویر ترکیبیِ دو ترانس با اندازه و برچسب متفاوت است؛ از مرجع کم‌وضوح مشخص نیست کدام مجموعه سیم/بدنه به SKU دقیق تعلق دارد. تولید تک‌محصول با برچسب یا اتصالات حدسی قابل اتکا نیست.'
for k in range(168,176):issues[k]='تصویر مشترک منبع تغذیه/درایور، برچسب فنی و سیم‌ها/ترمینال‌ها را نشان می‌دهد؛ گروه SKUهای توان/ولتاژ/آمپر متفاوت دارد. برچسب کامل و فرم دقیق اتصالِ همین SKU از کاتالوگ موجود مشخص نیست و نباید اختراع یا از SKU دیگر منتقل شود.'
issues[183]='تصویر عمومی صفحه نصب را با ناحیه سفیدِ فاقد جزئیات قاب/اپتیک نشان می‌دهد. مرجع بدون صفحه نصبِ F27BB/F30BB برای واریانت‌های F27/F30 هم‌پرتو استفاده شد؛ برای سایر مدل‌های همین گروه، سازگاری هندسه و پرتو از این مرجع ثابت نشده است. ناحیه سفید به‌عنوان یک قطعه قابل رنگ‌کردن فرض نشد.'
issues[199]='دو عنوان دقیق گروه، پرتو ۶۰ و ۳۸ درجه را برای یک تصویر یکسان نشان می‌دهند. جنس و هندسه اپتیک دقیق هر SKU از نمای مشترک قابل تأیید نیست؛ تغییر حدسی لنز انجام نشد.'
for t in a:
 k=gids.index(t['group_id']);t['review_part']='Part_001';t['batch_review_level']='group_visual_screen_plus_catalog_metadata_not_full_technical_QC'
 t['batch_review_basis']={'group_screen_index':k,'same_sha_members_verified':True,'catalog_matches':len(t.get('catalog_evidence',[])),'source_notes_reviewed_as_data':True}
 if t['decision']!='pending':continue
 if k in issues:
  t.update(decision='needs_reference_review',visual_review='batch_group_visual_and_metadata_review_reference_insufficient',review_note='نیازمند بررسی مرجع: '+issues[k]+' این وضعیت به‌معنی اثبات خطای تمام اعضای گروه نیست؛ مرجع دقیق برای اصلاح قابل اتکا کافی نیست.')
 elif t['brand'] in ['Alora','Alora Mood'] and 'same fixture with an electrical/CCT ordering suffix' in t['source']['Notes']:
  t.update(decision='shared_image_consistent_with_documented_ordering_suffix',visual_review='group_finish_screen_and_ordering_suffix_evidence_reviewed',review_note='داده منبع، کد نام‌گذاریِ دارای پسوند برق/CCT را همان چراغ معرفی می‌کند؛ رنگ و شکل کلی در تصویر گیت با عنوان موجود سازگار است. تفاوت ظاهریِ نیازمند تولید مجدد در این بررسی مشخص نشد. مشخصات برق، رنگ دقیق، تعداد قطعات ریز و نوشته‌ها تأیید فنی کامل نشده‌اند.')
 else:
  t.update(decision='screened_no_obvious_mismatch',visual_review='batch_group_visual_and_metadata_screened_technical_QC_pending',review_note='تصویر مشترک گروه، رنگ/چیدمان کلی و عنوان‌های موجود بررسی شدند و ایراد آشکارِ قابل اصلاح با مرجع معتبر در این مرحله تأیید نشد. شباهت عکس به‌تنهایی خطا نیست. این نتیجه غربال گروهی و تطبیق داده‌هاست؛ تأیید کاملِ SKU، کیفیت ریزجزئیات، ابعاد، پرتو، تعداد قطعات یا نوشته‌ها نیست. اختلاف توان، ولتاژ، طول یا CCTِ ثبت‌شده باید در QC دقیق همان SKU بررسی شود.')
json.dump(x,open(W/'review.json','w'),ensure_ascii=False,indent=2)
print(json.dumps(dict(collections.Counter(t['decision'] for t in a)),ensure_ascii=False))
