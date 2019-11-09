#-*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib as mat
import json,requests,os,math,sys
from PIL import Image,ImageFont,ImageDraw


def pretty_date(time=False):
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diffa = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diffa = now - time
    elif not time:
        diffa = now - now
    second_diff = diffa.seconds
    day_diff = diffa.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "刚刚"
        if second_diff < 60:
            return str(second_diff) + "秒前"
        if second_diff < 120:
            return "一分钟前"
        if second_diff < 3600:
            return str(round(second_diff / 60)) + "分钟前"
        if second_diff < 7200:
            return "一小时前"
        if second_diff < 86400:
            return str(round(second_diff / 3600)) + "小时前"
    if day_diff == 1:
        return "昨天"
    if day_diff < 7:
        return str(day_diff) + "天前"
    if day_diff < 31:
        return str(day_diff / 7) + "周前"
    if day_diff < 365:
        return str(day_diff / 30) + "月前"
    return str(day_diff / 365) + "年前"

if len(sys.argv)<2:
    mid = '39638388'
else:
	mid = sys.argv[1]

font = {'family':' MF FangHei(Noncommercial)'}
fh = mat.font_manager.FontProperties(fname='mffh.ttf')
setFont = ImageFont.truetype('mffh.ttf', 90)
fillColor = "#000000"
plt.rc('font',**font)
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['font.sans-serif'] = [' MF FangHei(Noncommercial)']
plt.rcParams['font.serif'] = [' MF FangHei(Noncommercial)']
info = json.loads(requests.get("https://bilidata.1mc.site/api/web/data/get_source?type=1&id="+mid).text)
r = requests.get("https://bilidata.1mc.site/api/web/data/readby?sid="+info["id"]+"&time=43200")
fans = requests.get("https://api.bilibili.com/x/relation/stat?vmid="+mid)
d = json.loads(r.text)
f = json.loads(fans.text)
x_data = []
y_data = []
ins = f['data']['follower']-int(d[0][1]['fans'])
if ins == 0:
  ins_txt = '持平'
if ins > 0:
  ins_txt = '+'+str(ins)
if ins < 0:
  ins_txt = str(ins)
for data in d:
  x_data.append(pretty_date(int(data[0])))
  y_data.append(data[1]["fans"])
yint = range(min(y_data), math.ceil(max(y_data))+1)
plt.xticks(fontproperties=fh,fontsize=12)
plt.yticks(yint)
plt.figure(figsize=(10.8, 4))
plt.subplots_adjust(left=0.08,right=0.98,wspace=0.25,hspace=0.25,bottom=0.1,top=1)
plt.plot(x_data,y_data)
ax = plt.gca()
for label in ax.get_xticklabels()[::2]:
  label.set_visible(False)
plt.savefig("temp.png")
imp = Image.open('tpl_fansreport.png')
imq = Image.open('temp.png')
r, g, b, alpha = imq.split()
alpha = alpha.point(lambda i: i>0 and 178)
imp.paste(imq,(0, 1055),mask=alpha)
draw = ImageDraw.Draw(imp)
draw.text(((520-(len(str(f['data']['follower']))*25)), 530), str(f['data']['follower']), font=setFont, fill=fillColor)
draw.text(((510-(len(ins_txt)*25)), 770), ins_txt, font=setFont, fill=fillColor)
imp=imp.convert('RGB')
imp.save('outfans.jpg')
