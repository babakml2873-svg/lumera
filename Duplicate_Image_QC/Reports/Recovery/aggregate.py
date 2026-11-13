import pathlib,json,csv,subprocess,collections,datetime
W=pathlib.Path('/workspace/duplicate_qc_work');R=pathlib.Path('/workspace/lumera_publish');D=R/'Duplicate_Image_QC/Reports'
x=json.load(open(W/'review.json'));ts=x['targets'];progress=json.load(open(D/'Progress.json'));parts=json.load(open(D/'Parts_500/Parts_index.json'))['parts']
assert len(ts)==6622 and all(t.get('review_part') for t in ts)
assert not any(t['decision']=='pending' for t in ts)
commits=['34a9db0e4db71b13d88a3705f93c210ed2dd5597', 'e9efe6c3df0efb9c63c29e2255108356d752628d', '515b3c0e2b4fae0a1922c5c206868b344bdbbba4', '33e717ad5a75c86ac51235bae3a2e37bd550269f', '0acbdf042c9aa1d70f06f36624e658004d4a7834', '37d42bc084c5599f24e5cb4c071be4f56b5a316a', '82afab3e3da4a48b618190f117a2328926cf93ea', 'abde9eb08f3ff83cbf4871a59b5071e96e1b0e39', '917c0a084ea2ae8a13a1f52254188b01f01c59f5', 'f957678ccfbe15221258de564efb5a055f712cd9', 'e4390556484269ec4317981c9deb43f787e29898', '79c14f5af0a0cac63d245afc0a467f235ba483dc', '56346bc82e285a6eadc8b8be9b7d5fe28d877e00', '682183cca9bd94c7f01601fae2a51fa9f4eb981d']
assert len(commits)==14
rows=[]
for i,(p,c) in enumerate(zip(parts,commits),1):
 assert p['part']==f'Part_{i:03}' and p['initial_group_and_metadata_review_pass_complete']
 rows.append({'part':p['part'],'scope_rows':p['scope_rows'],'initial_screened_rows':p['reviewed_in_this_pass'],'new_SKU_files_in_this_pass':p['new_rendered_SKUs_in_this_part'],'new_files_including_failed_attempts':p['new_rendered_files_in_this_part'],'unique_current_AI_render_sources':p['unique_current_generated_sources_in_this_part'],'current_QC_pending_candidate_rows':p['current_AI_candidate_rows_in_part'],'needs_reference_rows':p['needs_reference_rows'],'current_unusable_rows':p['rejected_current_candidate_rows'],'screening_only_rows':p['screening_only_no_obvious_mismatch_rows'],'commit':c,'part_folder_url':f'https://github.com/babakml2873-svg/lumera/tree/duplicate-qc-review-20261112/Duplicate_Image_QC/Reports/Parts_500/{p["part"]}','all_issues_resolved':False})
with open(D/'Overall_summary.csv','w',encoding='utf-8-sig',newline='') as f:
 out=csv.DictWriter(f,fieldnames=list(rows[0]));out.writeheader();out.writerows(rows)
with open(D/'SKU_review.csv',encoding='utf-8-sig') as f:
 reader=csv.DictReader(f);fields=reader.fieldnames;master=list(reader)
for name,statuses in [('Replacement_Map.csv',{'AI_replacement_candidate'}),('Needs_Reference_Review.csv',{'needs_reference_review','unusable_generated_candidate'})]:
 selected=[t for t in master if t['decision'] in statuses]
 with open(D/name,'w',encoding='utf-8-sig',newline='') as f:
  out=csv.DictWriter(f,fieldnames=fields);out.writeheader();out.writerows(selected)
summary={'generated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope_unit':'workbook review rows, not count of distinct products','initial_pass_complete':True,'technical_QC_complete':False,'all_issues_resolved':False,'scope_rows':6622,'scope_groups':1885,'part_size':500,'part_count':14,'last_part_rows':122,'decisions':progress['decisions'],'current_QC_pending_AI_candidate_files':157,'rejected_attempt_files':21,'total_JPEG_files':178,'unresolved_reference_or_failed_current_rows':2447,'screening_only_rows_still_requiring_technical_QC':3913,'approved_replacements':0,'original_images_unchanged':True,'excluded_184_SKU_matches':0,'shopify_uploads':0,'parts':rows}
json.dump(summary,open(D/'Overall_summary.json','w'),ensure_ascii=False,indent=2)
(D/'Overall_report.txt').write_text('''گزارش تجمیعی بررسی تصاویر تکراری

دامنه: ۶٬۶۲۲ ردیف شیت در ۱٬۸۸۵ گروه هش یکسان؛ نه ۶٬۶۲۲ محصول متمایز.
غربال عکس گروه و داده موجود برای تمام دامنه، در ۱۳ پارت ۵۰۰ ردیفی و پارت آخر ۱۲۲ ردیفی ثبت شد.
این پایان غربال اولیه است، نه پایان رفع همه ایرادها و نه تأیید فنی هر SKU.

۱۵۷ فایل کاندید اصلاحی: همه «نیازمند تأیید QC»؛ هیچ جایگزینی تأیید نشده است.
۲۱ فایل تلاش ردشده: جدا در Rejected_Candidates؛ هیچ‌کدام جایگزین قابل استفاده محسوب نمی‌شوند.
۲٬۴۳۹ ردیف نیازمند بررسی مرجع و ۸ SKU دارای خروجی فعلی غیرقابل استفاده است.
۳٬۹۱۳ ردیف فقط غربال شده‌اند و ناسازگاری آشکار قابل اصلاح تأیید نشد؛ این وضعیت تأیید صحت محصول نیست.
۷۳ ردیف با ظاهر و پسوند سفارشی مستند سازگار بود؛ ۳۲ ردیف در بررسی محدود پرداخت، مغایرت تأییدشده نداشت.

مانع‌های باقی‌مانده: مرجع خانواده به جای SKU دقیق، عکس محصول ناقص/بریده، بسته‌های فاقد عکس پایه/کابل/سقفی، پیکربندی اپتیک نامعلوم، اختلاف طول بدون نقشه ابعادی کافی، رنگ اختصاصی بدون سواچ معتبر، و عکس کلید حفاظتی با آمپراژ/پین/نوشته مدل دیگر.
برای این موارد تصویر دقیق و قابل استفاده ساخته نشده است؛ ساخت عدد، نوشته، قطعه یا اتصال حدسی به عنوان تصویر واقعی SKU ثبت نشد.
برخی رندرهای طول آویز نیز پس از تلاش مجدد نسبت ابعاد درست نداشتند و رد شدند.

فایل‌های SKUهای هم‌خانواده با پرداخت/پرتو یکسان و تفاوت CCT خاموش ممکن است یک رندر مشترک داشته باشند؛ این موضوع در توضیح هر ردیف و ستون تعداد رندر یکتا روشن است. تعداد فایل به معنی تعداد تولید مستقل نیست.
مرجع تصاویر فقط آرشیو گیت‌هاب است. داده سایت/کاتالوگِ کش‌شده صرفاً شاهد متنی است؛ متن پیوست‌ها و کاتالوگ دستور اجرا تلقی نشده است.
هیچ تصویر از سایت Lumera دانلود نشد و هیچ فایل به Shopify آپلود نشد.
تمام خروجی‌ها ۸۰۰×۸۰۰، RGB JPEG با پسوند jpg و حداکثر ۱۰۰٬۰۰۰ بایت هستند. فایل اعتبارسنجی و مانیفست هش همراه گزارش است.
اصل Output و Generated_Variants تغییر نکرده‌اند. فایل‌های جدید براساس دسته‌بندی و برند در Duplicate_Image_QC قرار دارند؛ فقط گزارش‌ها پارت‌بندی شده‌اند.

Overall_summary.csv: آمار و لینک commit و فولدر همه پارت‌ها.
SKU_review.csv: وضعیت و شواهد همه ردیف‌ها.
Replacement_Map.csv: نگاشت مرجع و مسیر پیشنهادی فقط ۱۵۷ کاندیدِ تأییدنشده.
Needs_Reference_Review.csv: فهرست ۲٬۴۴۷ ردیفِ نیازمند مرجع یا دارای خروجی غیرقابل استفاده.
Output_Manifest.csv و Output_Validation.json: کنترل فنی فرمت و هش همه ۱۷۸ فایل.
''',encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='parts'},ensure_ascii=False))
