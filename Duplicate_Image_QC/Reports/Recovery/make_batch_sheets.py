import json,pathlib,math,sys
from PIL import Image,ImageOps,ImageDraw,ImageFont
W=pathlib.Path('/workspace/duplicate_qc_work');x=json.load(open(W/'review.json'));num=int(sys.argv[1]);a=x['targets'][(num-1)*500:num*500];gids=list(dict.fromkeys(t['group_id'] for t in a));font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
for b in range(math.ceil(len(gids)/20)):
 page=Image.new('RGB',(2000,2000),'#ddd');draw=ImageDraw.Draw(page)
 for j,gid in enumerate(gids[b*20:(b+1)*20]):
  ts=[t for t in a if t['group_id']==gid];t=ts[0];im=ImageOps.contain(Image.open('/workspace/lumera/'+t['original_path']).convert('RGB'),(390,355));xx=(j%5)*400;yy=(j//5)*500;page.paste(im,(xx+(400-im.width)//2,yy));txt=f'{b*20+j:03} {t["sku"]}\n{t["brand"]} rows={len(ts)}\n'+', '.join(sorted(set(f for t in ts for f in t['finish_keywords'])))[:50]
  draw.multiline_text((xx+5,yy+365),txt,fill='black',font=font)
 page.save(W/f'batch{num:03}_screen_{b:02}.jpg',quality=92)
json.dump(gids,open(W/f'batch{num:03}_groups.json','w'))
print(json.dumps({'part':num,'rows':len(a),'groups':len(gids),'sheets':math.ceil(len(gids)/20)}))
