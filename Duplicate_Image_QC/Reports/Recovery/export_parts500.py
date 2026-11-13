import pathlib,json,csv,collections,math,subprocess
W=pathlib.Path('/workspace/duplicate_qc_work');R=pathlib.Path('/workspace/lumera_publish');D=R/'Duplicate_Image_QC/Reports/Parts_500'
subprocess.run(['python',str(W/'checkpoint.py')],check=True)
x=json.load(open(W/'review.json'));ts=x['targets'];D.mkdir(exist_ok=True)
with open(R/'Duplicate_Image_QC/Reports/SKU_review.csv',encoding='utf-8-sig') as f:
 reader=csv.DictReader(f);fields=reader.fieldnames;master={int(r['excel_row']):r for r in reader}
index=[]
for k in range(math.ceil(len(ts)/500)):
 part=f'Part_{k+1:03}';a=ts[k*500:(k+1)*500];reviewed=[t for t in a if t.get('review_part')==part]
 s={'part':part,'item_unit':'workbook SKU review row; not 500 generated images or 500 distinct products','scope_rows':len(a),'first_scope_position':k*500+1,'last_scope_position':k*500+len(a),'reviewed_in_this_pass':len(reviewed),'initial_group_and_metadata_review_pass_complete':len(reviewed)==len(a),'all_issues_resolved':False,'detailed_technical_QC_complete':False,'decisions':dict(collections.Counter(t['decision'] for t in a)),'new_rendered_SKUs_in_this_part':sum(t.get('generation_batch')=='Review_500_'+f'{k+1:03}' for t in a),'new_rendered_files_in_this_part':sum(t.get('generation_batch')=='Review_500_'+f'{k+1:03}' for t in a)+sum(at.get('generation_batch')=='Review_500_'+f'{k+1:03}' for t in a for at in t.get('rejected_attempts',[])),'current_AI_candidate_rows_in_part':sum(t['decision']=='AI_replacement_candidate' for t in a),'needs_reference_rows':sum(t['decision']=='needs_reference_review' for t in a),'rejected_current_candidate_rows':sum(t['decision']=='unusable_generated_candidate' for t in a),'screening_only_no_obvious_mismatch_rows':sum(t['decision']=='screened_no_obvious_mismatch' for t in a),'unreviewed_in_this_500_pass':len(a)-len(reviewed)}
 index.append(s)
 if not reviewed:continue
 p=D/part;p.mkdir(exist_ok=True)
 json.dump(s,open(p/(part+'_summary.json'),'w'),ensure_ascii=False,indent=2)
 with open(p/(part+'_report.csv'),'w',encoding='utf-8-sig',newline='') as f:
  out=csv.DictWriter(f,fieldnames=fields);out.writeheader();out.writerows(master[t['excel_row']] for t in a)
json.dump({'scope_rows':len(ts),'part_size_rows':500,'total_parts':len(index),'initial_pass_rows':sum(i['reviewed_in_this_pass'] for i in index),'all_issues_resolved':False,'parts':index},open(D/'Parts_index.json','w'),ensure_ascii=False,indent=2)
print(json.dumps([s for s in index if s['reviewed_in_this_pass']],ensure_ascii=False))
