import json,pathlib,hashlib,csv,glob,subprocess,datetime,re
from PIL import Image
W=pathlib.Path('/workspace/duplicate_qc_work');R=pathlib.Path('/workspace/lumera_publish');D=R/'Duplicate_Image_QC'
x=json.load(open(W/'review.json'));canon=lambda s:str(s).strip().lstrip("'").upper()
ex={canon(r['sku']) for r in csv.DictReader(open(glob.glob('/workspace/attachments/*/*.csv')[0],encoding='utf-8-sig'))}
assert len(ex)==184
safe=lambda s:re.sub(r'[\s/\\:?#&]+','-',s.strip()).strip('-')
mapped={};manifest=[]
for t in x['targets']:
 if t.get('output_path'):mapped[t['output_path']]=(t,t)
 for a in t.get('rejected_attempts',[]):mapped[a['output_path']]=(t,a)
files=list(D.rglob('*.jpg'));assert len(files)==len(mapped)
for p in files:
 rel=str(p.relative_to(R));t,a=mapped[rel];assert canon(t['sku']) not in ex
 assert p.name==safe(t['sku'])+'-V.jpg'
 h=hashlib.sha256(p.read_bytes()).hexdigest();assert h==a['output_sha256']
 with Image.open(p) as im:assert im.size==(800,800) and im.format=='JPEG' and im.mode=='RGB'
 assert p.stat().st_size<=100000 and p.stat().st_size==a['output_bytes']
 assert t['qc_status']=='نیازمند تأیید QC'
 rejected='/Reports/Rejected_Candidates/' in rel
 assert rejected or t['decision']=='AI_replacement_candidate'
 manifest.append({'sku':t['sku'],'path':rel,'sha256':h,'dimensions':'800x800','bytes':p.stat().st_size,'QC':t['qc_status'],'usability':'rejected_do_not_use' if rejected else 'candidate_requires_QC'})
for path,base in [(R,'99dd49fc9eb8541261df129f4641c20a8e5dd1cd')]:
 changed=subprocess.check_output(['git','-C',str(path),'diff','--name-only',base],text=True).splitlines()
 assert all(p.startswith('Duplicate_Image_QC/') for p in changed),changed
source_changed=subprocess.check_output(['git','-C','/workspace/lumera','diff','--name-only','22d81bfc2b60b79cea477ebd0c7b4f90d8faec42','--','Output'],text=True).splitlines()
assert not source_changed
with open(D/'Reports/Output_Manifest.csv','w',encoding='utf-8-sig',newline='') as f:
 c=csv.DictWriter(f,fieldnames=list(manifest[0]));c.writeheader();c.writerows(sorted(manifest,key=lambda r:r['path']))
a={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files_checked':len(files),'current_candidate_files':sum(r['usability']=='candidate_requires_QC' for r in manifest),'rejected_files_including_previous_attempts':sum(r['usability']=='rejected_do_not_use' for r in manifest),'dimensions_format_mode_and_size_pass':True,'max_bytes':max(r['bytes'] for r in manifest),'excluded_184_SKU_output_matches':0,'filename_and_SHA_manifest_pass':True,'original_Output_unchanged':True,'previous_Generated_Variants_unchanged':True,'all_AI_candidates_require_QC':True,'technical_QC_approved':0,'scope_complete':False}
json.dump(a,open(D/'Reports/Output_Validation.json','w'),ensure_ascii=False,indent=2);print(json.dumps(a))
