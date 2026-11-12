import json,csv,re,pathlib,collections,hashlib,urllib.parse
W=pathlib.Path('/workspace/duplicate_qc_work');R=pathlib.Path('/workspace/lumera');D=pathlib.Path('/workspace/lumera_publish/Duplicate_Image_QC/Reports')
x=json.load(open(W/'review.json'));q=json.load(open('/workspace/variant_work/qc.json'))
canon=lambda s:str(s or '').strip().lstrip("'").upper()
norm=lambda s:re.sub('[^a-z0-9]','',str(s or '').lower())
key=lambda b,s:(norm(b),canon(s))
product_by_sku=collections.defaultdict(set)
for r in q:
 if r.get('SKU') and r.get('لینک محصول'):product_by_sku[key(r.get('برند'),r['SKU'])].add(str(r['لینک محصول']).rstrip('/'))
wanted={str(t['product_url']).rstrip('/') for t in x['targets']}
known={m['path']:g['SHA-256'] for g in x['groups'] for m in g['members']}
refs=collections.defaultdict(dict)
for r in csv.DictReader(open(R/'Output/Reports/image_report.csv',encoding='utf-8-sig')):
 if not r['Filename']:continue
 urls=product_by_sku.get(key(r['Brand'],r['SKU']),set()) & wanted
 if not urls:continue
 p='Output/'+r['List']+'/'+r['Brand'].replace(' ','_')+'/'+r['Filename'];f=R/p
 if not f.is_file():continue
 h=known.get(p)
 if not h:h=hashlib.sha256(f.read_bytes()).hexdigest();known[p]=h
 for u in urls:
  # Keep each unique actual file, retaining SHA so duplicate bytes are visible.
  refs[u][p]={'sku':r['SKU'],'path':p,'sha256':h,'image_type':r['Image_Type'],'confidence':r['Match_Confidence'],'notes':r['Notes']}
out=[]
for t in x['targets']:
 a=list(refs[str(t['product_url']).rstrip('/')].values());different=[r for r in a if r['sha256']!=t['original_sha256']]
 t['same_product_reference_files']=len(a);t['same_product_alternative_hashes']=len({r['sha256'] for r in different})
 for r in different:
  out.append(dict(target_sku=t['sku'],brand=t['brand'],product_url=t['product_url'],candidate_reference_sku=r['sku'],image_type=r['image_type'],confidence=r['confidence'],path=r['path'],sha256=r['sha256'],github_url='https://raw.githubusercontent.com/babakml2873-svg/lumera/22d81bfc2b60b79cea477ebd0c7b4f90d8faec42/'+urllib.parse.quote(r['path']),source_notes=r['notes'],status='index_only_not_visually_or_technically_validated'))
fields=['target_sku','brand','product_url','candidate_reference_sku','image_type','confidence','path','sha256','github_url','source_notes','status']
with open(D/'Alternative_References.csv','w',encoding='utf-8-sig',newline='') as f:
 c=csv.DictWriter(f,fieldnames=fields);c.writeheader();c.writerows(out)
json.dump(x,open(W/'review.json','w'),ensure_ascii=False,indent=2)
print(json.dumps({'indexed_alternative_file_links':len(out),'targets_with_other_same_product_image_hashes':sum(t['same_product_alternative_hashes']>0 for t in x['targets']),'targets_with_no_other_same_product_image_hashes':sum(t['same_product_alternative_hashes']==0 for t in x['targets'])}))
