"""Generate the original illustrated micro-lesson (Pillow and imageio-ffmpeg)."""
from pathlib import Path
import os, math
from PIL import Image,ImageDraw,ImageFont
import imageio_ffmpeg as ff
P=Path(__file__).parent/'media'; P.mkdir(exist_ok=True)
W,H=960,540
font=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts/msyh.ttc'
def f(n):return ImageFont.truetype(str(font),n)
scenes=[
 ('使徒信经','罗马的洗礼传统','先讲清楚福音的故事','创造 → 十架与复活 → 永生','#3fbbac'),
 ('尼西亚信经','尼西亚 325 · 君士坦丁堡 381','辨认我们所敬拜的是谁','子是造物主；圣灵同受敬拜','#f5bf76'),
 ('亚他那修信经','拉丁西方的教会教学','守住两对不可混淆的界线','一神三位；一位中保、真实二性','#b6a5f4'),
 ('三份信经，同一福音','复述练习','故事 → 敬拜 → 辨析','回到约翰福音 1 章与希伯来书 2 章','#74bfea')]
def frame(index,n):
 title,where,line,extra,color=scenes[index]
 im=Image.new('RGB',(W,H),'#112d3c'); d=ImageDraw.Draw(im)
 d.rounded_rectangle((32,32,928,505),28,fill='#18394b',outline='#315268',width=2)
 d.text((70,66),f'GT STUDY   /   0{index+1}',font=f(22),fill=color)
 d.text((68,137),title,font=f(50),fill='#ffffff')
 d.text((70,220),where,font=f(23),fill='#d2e0e8')
 d.text((70,321),line,font=f(32),fill='#ffffff')
 d.text((70,385),extra,font=f(25),fill=color)
 y=216+int(8*math.sin(n/10))
 for r in (76,94,113):d.ellipse((772-r,y-r,772+r,y+r),outline='#315268',width=2)
 for j in range(3):
  x=772+math.sin(j*2.094+n/30)*68;z=y+math.cos(j*2.094+n/30)*68
  d.ellipse((x-8,z-8,x+8,z+8),fill=color)
 # Symbols are teaching aids: baptismal bowl, council hall, open book, and cross.
 if index==0:
  d.arc((724,y-22,820,y+45),0,180,fill=color,width=5)
  d.line((724,y+11,820,y+11),fill=color,width=4)
  d.ellipse((768,y-28,776,y-16),fill=color)
 elif index==1:
  d.line([(723,y-10),(772,y-42),(821,y-10),(723,y-10)],fill=color,width=4)
  for x in (738,772,806):d.line((x,y-10,x,y+31),fill=color,width=5)
  d.line((725,y+32,819,y+32),fill=color,width=4)
 elif index==2:
  d.line([(772,y+33),(728,y+16),(728,y-28),(772,y-13),(816,y-28),(816,y+16),(772,y+33),(772,y-13)],fill=color,width=4)
 else:
  d.line((772,y-41,772,y+39),fill=color,width=6)
  d.line((742,y-11,802,y-11),fill=color,width=6)
 for i in range(4):d.rounded_rectangle((70+206*i,466,249+206*i,473),3,fill=color if i<=index else '#315268')
 return im
frame(0,0).save(P/'creed-scenes.jpg',quality=88)
writer=ff.write_frames(str(P/'creed-scenes.mp4'),(W,H),fps=12,codec='libx264',quality=7,macro_block_size=2,output_params=['-movflags','+faststart'])
writer.send(None)
for i in range(4):
 for n in range(96):writer.send(frame(i,n).tobytes())
writer.close()
vtt='WEBVTT\n\n'+ '\n\n'.join(f'00:00:{i*8:02d}.000 --> 00:00:{(i+1)*8:02d}.000\n{x[0]}：{x[2]}。{x[3]}。' for i,x in enumerate(scenes))+'\n'
(P/'creed-scenes.vtt').write_text(vtt,encoding='utf8',newline='\n')
