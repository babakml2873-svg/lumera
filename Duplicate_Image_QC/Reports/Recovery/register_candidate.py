import json,pathlib,re,csv,glob,hashlib,sys
from PIL import Image
W=pathlib.Path('/workspace/duplicate_qc_work');d=json.load(open(W/'review.json'));sku=sys.argv[1];src=pathlib.Path(sys.argv[2]);reason=sys.argv[3]
matches=[t for t in d['targets'] if t['sku']==sku and (len(sys.argv)<5 or t['excel_row']==int(sys.argv[4]))]
assert len(matches)==1, 'Ambiguous SKU: supply the exact Excel row as the final argument'
t=matches[0]
def canon(x):return str(x).strip().lstrip("'").upper()
ex={canon(r['sku']) for r in csv.DictReader(open(glob.glob('/workspace/attachments/*/*.csv')[0],encoding='utf-8-sig'))};assert canon(sku) not in ex
safe=lambda s:re.sub(r'[\s/\\:?#&]+','-',s.strip()).strip('-')
segs=[safe(s) for s in re.split(r'\s*(?:/|>)\s*',t['category']) if s.strip()];brand=t['original_path'].split('/')[2]
p=pathlib.Path('Duplicate_Image_QC').joinpath(*segs,brand,safe(sku)+'-V.jpg');out=pathlib.Path('/workspace/lumera_publish')/p;out.parent.mkdir(parents=True,exist_ok=True)
im=Image.open(src).convert('RGB');im.thumbnail((800,800),Image.Resampling.LANCZOS);canvas=Image.new('RGB',(800,800),'white');canvas.paste(im,((800-im.width)//2,(800-im.height)//2))
for quality in range(94,39,-1):
 canvas.save(out,'JPEG',quality=quality,optimize=True,subsampling=0)
 if out.stat().st_size<=100000:break
assert out.stat().st_size<=100000
assert Image.open(out).size==(800,800)
t.update(visual_review='full_reference_and_candidate_reviewed',decision='AI_replacement_candidate',generation_status='generated',qc_status='نیازمند تأیید QC',output_path=str(p),review_note=reason+'؛ رنگ نهایی و جزئیات فنی باید با SKU دقیق تأیید شوند.',output_dimensions='800x800',output_bytes=out.stat().st_size,reference_sku=sku,reference_url=t['original_url'],generated_source=str(src),output_sha256=hashlib.sha256(out.read_bytes()).hexdigest())
json.dump(d,open(W/'review.json','w'),ensure_ascii=False,indent=2);print(p,out.stat().st_size)
