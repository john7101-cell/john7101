import json,subprocess,os,sys
S=os.path.dirname(os.path.abspath(__file__)); U="/root/.claude/uploads/d60bbb93-9d71-5269-bf89-48eddddfd067/"
src={k:U+f for f in os.listdir(U) for k in [f[:8]]}
tr=json.load(open(S+"/audio/tr.json"))
XF=0.35
segs=[ # id, in, out, chip
 ("acac8a52",0.50,15.95,None),
 ("9a820ff3",0.00,17.00,"Apego emocional"),
 ("31162a4f",1.62,11.80,"Creencias y heridas"),
 ("a38847f4",0.00,11.30,"Límites e identidad"),
 ("95c690a6",0.00,15.60,None),
]
END=4.5
os.makedirs(S+"/seg",exist_ok=True)
def run(c): subprocess.run(c,check=True)
grade="eq=contrast=1.05:saturation=1.08:brightness=0.01,colorbalance=rs=0.03:bs=-0.03:rm=0.02:bm=-0.02,unsharp=5:5:0.5"
for i,(k,a,b,_) in enumerate(segs):
    v="delogo=x=18:y=20:w=84:h=36," if k=="acac8a52" else ""
    vf=f"{v}scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,setsar=1,{grade},fps=30,format=yuv420p"
    af="highpass=f=80,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-16:TP=-1.5:LRA=9,aresample=48000,aformat=channel_layouts=stereo"
    if not os.path.exists(f"{S}/seg/{i}.mkv"): run(["ffmpeg","-v","error","-y","-ss",str(a),"-to",str(b),"-i",src[k],"-vf",vf,"-af",af,"-c:v","libx264","-crf","16","-preset","medium","-c:a","pcm_s16le",f"{S}/seg/{i}.mkv"])
# end card from last frame
last=f"{S}/seg/{len(segs)-1}.mkv"
run(["ffmpeg","-v","error","-y","-sseof","-0.1","-i",last,"-frames:v","1",f"{S}/seg/last.png"])
run(["ffmpeg","-v","error","-y","-loop","1","-t",str(END),"-i",f"{S}/seg/last.png","-f","lavfi","-t",str(END),"-i","anullsrc=r=48000:cl=stereo",
     "-vf","gblur=sigma=40,eq=brightness=-0.12:saturation=0.7,drawbox=c=0x2a1f1c@0.45:t=fill,fps=30,format=yuv420p","-c:v","libx264","-crf","16","-c:a","pcm_s16le","-shortest",f"{S}/seg/end.mkv"])
durs=[b-a for _,a,b,_ in segs]+[END]
files=[f"{S}/seg/{i}.mkv" for i in range(len(segs))]+[f"{S}/seg/end.mkv"]
starts=[0]
for d in durs[:-1]: starts.append(starts[-1]+d-XF)
total=starts[-1]+durs[-1]
# xfade chain
inp=sum([["-i",f] for f in files],[])
fc=[];vl="[0:v]";al="[0:a]"
for i in range(1,len(files)):
    off=starts[i]
    fc.append(f"{vl}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[v{i}]")
    fc.append(f"{al}[{i}:a]acrossfade=d={XF}:c1=tri:c2=tri[a{i}]")
    vl=f"[v{i}]";al=f"[a{i}]"
# ASS
def ts(t):
    t=max(0,t);h=int(t//3600);m=int(t%3600//60);s=t%60
    return f"{h}:{m:02d}:{s:05.2f}"
ACC="&H6DB8E8&"  # warm gold (BGR)
ev=[]
for i,(k,a,b,chip) in enumerate(segs):
    T=starts[i]-a
    words=[(w[0],w[1],w[2].strip()) for s in tr[k] for w in s["words"] if w[0]>=a-0.05 and w[1]<=b+0.1]
    # group into chunks of <=4 words, split at punctuation / pauses
    groups=[];g=[]
    for j,w in enumerate(words):
        g.append(w)
        nxt=words[j+1] if j+1<len(words) else None
        if len(g)>=4 or w[2][-1] in ".,?" or (nxt and nxt[0]-w[1]>0.35) or not nxt:
            groups.append(g);g=[]
    for gi,g in enumerate(groups):
        for j,w in enumerate(g):
            nxtg=groups[gi+1][0][0] if gi+1<len(groups) else 1e9
            st=w[0]+T; en=(g[j+1][0] if j+1<len(g) else min(g[-1][1]+0.25,nxtg))+T
            txt=" ".join((("{\\c"+ACC+"}"+x[2].upper()+"{\\c&HFFFFFF&}") if x is w else x[2].upper()) for x in g)
            pop="{\\fscx104\\fscy104\\t(0,90,\\fscx100\\fscy100)}" if j==0 else ""
            ev.append(f"Dialogue: 1,{ts(st)},{ts(en)},Sub,,0,0,0,,{pop}{txt}")
    if chip:
        s0=starts[i]+0.4
        ev.append(f"Dialogue: 2,{ts(s0)},{ts(s0+4.2)},Chip,,0,0,0,,{{\\fad(300,400)\\move(540,330,540,310,0,400)}}{chip.upper()}")
        ev.append(f"Dialogue: 2,{ts(s0)},{ts(s0+4.2)},ChipLine,,0,0,0,,{{\\fad(300,400)\\pos(540,372)\\p1}}m 0 0 l 120 0 120 4 0 4{{\\p0}}")
# title in hook when she says "En volver a mí" (src 12.54)
t0=starts[0]+12.45-segs[0][1]; t1=starts[1]
ev.append(f"Dialogue: 3,{ts(t0)},{ts(t1)},Title,,0,0,0,,{{\\fad(450,450)\\blur1\\move(540,330,540,300,0,600)}}Volver a mí")
ev.append(f"Dialogue: 3,{ts(t0+0.3)},{ts(t1)},Kicker,,0,0,0,,{{\\fad(450,450)\\pos(540,180)}}T A L L E R")
# small persistent brand mark after title
ev.append(f"Dialogue: 0,{ts(t1)},{ts(starts[-1])},Brand,,0,0,0,,{{\\fad(600,300)}}VOLVER A MÍ  ·  TALLER")
# end card
e=starts[-1]
ev.append(f"Dialogue: 3,{ts(e+0.3)},{ts(total)},Kicker,,0,0,0,,{{\\fad(500,0)\\pos(540,700)}}T A L L E R")
ev.append(f"Dialogue: 3,{ts(e+0.4)},{ts(total)},TitleBig,,0,0,0,,{{\\fad(600,0)\\move(540,900,540,870,0,700)}}Volver a mí")
ev.append(f"Dialogue: 3,{ts(e+0.9)},{ts(total)},Quote,,0,0,0,,{{\\fad(600,0)\\pos(540,990)}}Volver a ti es volverte a elegir")
ev.append(f"Dialogue: 3,{ts(e+1.5)},{ts(total)},CTA,,0,0,0,,{{\\fad(500,0)\\fscx92\\fscy92\\t(0,300,\\fscx100\\fscy100)\\pos(540,1180)}}INSCRIPCIONES ABIERTAS")
ass=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Lato Black,66,&H00FFFFFF,&H00FFFFFF,&H40000000,&H90000000,0,0,0,0,100,100,1,0,1,3,4,2,90,90,520,1
Style: Chip,Lato Bold,40,&H00FFFFFF,&H00FFFFFF,&H00000000,&H60000000,0,0,0,0,100,100,6,0,1,0,3,5,40,40,0,1
Style: ChipLine,Lato Bold,40,{ACC.replace('&H','&H00')},&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,5,0,0,0,1
Style: Title,EB Garamond 12,140,&H00FFFFFF,&H00FFFFFF,&H00000000,&H70000000,0,1,0,0,100,100,0,0,1,0,5,5,40,40,0,1
Style: TitleBig,EB Garamond 12,170,&H00FFFFFF,&H00FFFFFF,&H00000000,&H70000000,0,1,0,0,100,100,0,0,1,0,4,5,40,40,0,1
Style: Kicker,Lato Bold,40,{ACC.replace('&H','&H00')},&H00FFFFFF,&H00000000,&H60000000,0,0,0,0,100,100,4,0,1,0,3,5,40,40,0,1
Style: Quote,EB Garamond 12,62,&H00F0F0F0,&H00FFFFFF,&H00000000,&H60000000,0,1,0,0,100,100,0,0,1,0,3,5,60,60,0,1
Style: CTA,Lato Black,50,&H002A1F1C,&H00FFFFFF,{ACC.replace('&H','&H00')},&H00000000,0,0,0,0,100,100,5,0,3,26,0,5,60,60,0,1
Style: Brand,Lato Bold,28,&H50FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,5,0,1,0,2,8,40,40,150,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""+"\n".join(ev)+"\n"
open(S+"/subs.ass","w").write(ass)
# vignette + subs, music ducked under voice
fc.append(f"{vl}vignette=PI/5,ass={S}/subs.ass,format=yuv420p[vo]")
fc.append(f"[{len(files)}:a]atrim=0:{total:.3f},volume=0.55,afade=t=out:st={total-2.5:.3f}:d=2.5[m]")
fc.append(f"{al}asplit=2[vx][sc]")
fc.append(f"[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md]")
fc.append(f"[vx][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[ao]")
out=sys.argv[1]
run(["ffmpeg","-v","error","-y",*inp,"-i",S+"/music/bed.wav","-filter_complex",";".join(fc),"-map","[vo]","-map","[ao]",
     "-c:v","libx264","-crf","18","-preset","slow","-profile:v","high","-pix_fmt","yuv420p","-movflags","+faststart","-c:a","aac","-b:a","192k",out])
print("total",total,"starts",starts)
