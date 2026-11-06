import json, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from fontTools.ttLib import TTFont
S, ART, OUT, DATA = sys.argv[1:5]
F = S + "/fonts/"
R="/home/user/sawasdee-thai/"
nc=Image.open(R+"art/social/nong-chang-character.png").convert("RGB").crop((40,70,920,950))
MASC={"th":nc,"mix":nc,"fr":Image.open(R+"courses/fr/art/mascot-400.png").convert("RGB"),"es":Image.open(R+"courses/es/art/mascot.png").convert("RGB"),"it":Image.open(R+"courses/it/art/mascot-400.png").convert("RGB")}
def circ(img,r,ring=True):
    e=img.resize((2*r,2*r),Image.LANCZOS); m=Image.new("L",e.size,0); ImageDraw.Draw(m).ellipse((0,0,2*r-1,2*r-1),fill=255)
    out=Image.new("RGB",(2*r+12,2*r+12),(243,226,176)); om=Image.new("L",out.size,0); ImageDraw.Draw(om).ellipse((0,0,2*r+11,2*r+11),fill=255)
    out.paste(e,(6,6),m); return out,om
BG=(238,244,239); DARK=(18,60,51); TEAL=(18,125,106); ORANGE=(232,150,46); GREY=(78,106,98)
dots=[(18,125,106),(229,87,135),(232,150,46)]
FALL="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
cmaps={}
def cmap(path):
    if path not in cmaps: cmaps[path]=TTFont(path).getBestCmap()
    return cmaps[path]
def isthai(s): return any('฀'<=c<='๿' for c in s)
def font(kind,n):
    return (F+"Sarabun-SemiBold.ttf" if kind=="thai" else F+("Mitr-SemiBold.ttf" if kind=="bold" else "Mitr-Medium.ttf")), n
def runs(text,path):
    cm=cmap(path); out=[]
    for c in text:
        if 0x300<=ord(c)<=0x36f and out: out[-1][1]+=c; continue
        p = path if (ord(c) in cm or c in " \n") else FALL
        if out and out[-1][0]==p: out[-1][1]+=c
        else: out.append([p,c])
    return out
def width(d,text,kind,n):
    path,n=font(kind,n); return sum(d.textlength(t,font=ImageFont.truetype(p,n)) for p,t in runs(text,path))
def draw(d,xy,text,kind,n,fill,anchor="la"):
    path,n=font(kind,n); x,y=xy
    w=width(d,text,kind,n)
    if anchor=="mm": x-=w/2; anchor="lm"
    for p,t in runs(text,path):
        f=ImageFont.truetype(p,n); d.text((x,y),t,font=f,fill=fill,anchor=anchor); x+=d.textlength(t,font=f)
def base(title,lang="th",mascot=True):
    im=Image.new("RGB",(1080,1080),BG); d=ImageDraw.Draw(im)
    for y in (16,1064):
        for i,x in enumerate(range(18,1080,26)): d.ellipse((x-5,y-5,x+5,y+5),fill=dots[i%3])
    draw(d,(540,80),title,"med",40,TEAL,"mm")
    if mascot:
        r=150; c,cm=circ(MASC[lang],r); im.paste(c,(1080-2*r-46,1080-2*r-66),cm)
    d.text((60,1000),"nongchang.co.uk",font=ImageFont.truetype(F+"Mitr-Medium.ttf",34),fill=GREY,anchor="ls")
    return im,d
def kind(s,default="bold"): return "thai" if isthai(s) else default
for p in json.load(open(DATA)):
    sp=p.get("spec")
    if not sp: continue
    lang=p.get("lang","th")
    if p.get("special")=="mascots":
        im,d=base(sp["title"],lang,False)
        draw(d,(540,250),sp["big"],"bold",72 if len(sp["big"])<24 else 58,DARK,"mm")
        for i,(k,name) in enumerate([("th","Nong Chang"),("fr","Coco"),("es","Torito"),("it","Lupo")]):
            cx=290+500*(i%2); cy=470+300*(i//2); c,cm=circ(MASC[k],115); im.paste(c,(cx-121,cy-121),cm)
            draw(d,(cx,cy+150),name,"bold",40,TEAL,"mm")
        im.save(OUT+"/"+p["card"]+".png"); print("made",p["card"]); continue
    im,d=base(sp["title"],lang); y=270
    if "big" not in sp and "roman" not in sp and not sp.get("linesBig") and "pair" not in sp:
        y=200
        for L,Rr in sp.get("lines",[]):
            draw(d,(80,y),L,kind(L),62 if width(d,L,kind(L),62)<900 else 50,DARK); draw(d,(80,y+92),Rr,"med",38,ORANGE); y+=170
        im.save(OUT+"/"+p["card"]+".png"); print("made",p["card"]); continue
    if "pair" in sp:
        for i,(L,name,rom) in enumerate(sp["pair"]):
            cx=300 if i==0 else 780
            draw(d,(cx,330),L,"thai",300,DARK,"mm"); draw(d,(cx,560),name,"thai",80,TEAL,"mm"); draw(d,(cx,650),rom,"med",38,ORANGE,"mm")
    else:
        if "big" in sp:
            big=sp["big"]; n=190 if len(big)<=6 else (150 if len(big)<=10 else 110)
            if not isthai(big): n=min(n,130)
            while width(d,big,kind(big),n)>980: n-=6
            draw(d,(540,y),big,kind(big),n,DARK,"mm"); y+=170 if isthai(big) else 140
        if "roman" in sp: draw(d,(540,y),sp["roman"],"bold",60,ORANGE,"mm"); y+=90
        if sp.get("meaning"): draw(d,(540,y),sp["meaning"],"bold",58 if len(sp["meaning"])<22 else 48,TEAL,"mm"); y+=110
        big_lines=sp.get("linesBig")
        if big_lines: y=230
        for L,R in sp.get("lines",[]):
            L=L.replace("⭐","•")
            if big_lines:
                draw(d,(90,y),L,kind(L),120,DARK); draw(d,(430,y+40),R,"bold",60,ORANGE); y+=190
            else:
                lim=1000 if y+60<700 else 690
                a,b=54,40
                while 80+width(d,L,kind(L),a)+24+width(d,R,"med",b)>lim and b>32: a-=2; b-=1
                if 80+width(d,L,kind(L),a)+24+width(d,R,"med",b)<=lim:
                    draw(d,(80,y),L,kind(L),a,TEAL); x2=80+width(d,L,kind(L),a)+24
                    draw(d,(x2,y+6),R,"med",b,GREY); y+=80
                else:
                    draw(d,(80,y),L,kind(L),54,TEAL); draw(d,(80,y+66),R,"med",38,GREY); y+=126
    im.save(OUT+"/"+p["card"]+".png")
    print("made", p["card"])
