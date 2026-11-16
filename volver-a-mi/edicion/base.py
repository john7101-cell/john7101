import subprocess, os
# (clip, in, out, start_on_timeline)
EDL = [
 ("02",0.0,2.2), ("01",0.0,1.3), ("02",5.0,7.5), ("01",1.4,4.6),
 ("01",4.6,8.0), ("03",1.35,3.75),
 ("04",0.6,5.8),
 ("04",5.8,8.0), ("03",6.8,8.0), ("05",2.0,4.0),
 ("05",4.0,8.0), ("06",0.0,1.2), ("06",1.3,2.1),
 ("06",2.1,6.5),
 ("06",6.5,8.0), ("07",0.0,2.0), ("05",0.0,2.0), ("03",3.75,5.4), ("07",2.0,2.9),
 ("07",2.9,8.0), ("08",0.0,1.7),
 ("08",2.2,5.0), ("09",0.0,1.2), ("09",1.25,2.75), ("09",2.8,4.0), ("09",4.05,5.45), ("08",5.0,8.0), ("09",5.5,7.5),
 ("10",3.0,6.1),
 ("11",0.0,8.0), ("11",0.0,0.0),  # placeholder removed below
 ("12",3.3,8.0),
 ("13",2.6,8.0), ("14",0.0,1.35),
 ("14",1.4,8.0),
]
EDL=[e for e in EDL if e[2]>e[1]]
GRADE="eq=contrast=1.06:saturation=0.92:gamma=0.98,colorbalance=rs=0.03:bs=-0.03:rh=0.02,vignette=PI/5,noise=alls=7:allf=t+u"
tot=0; lst=[]
for k,(c,a,b) in enumerate(EDL):
    out=f"/root/edit/seg/s{k:02d}.mp4"; d=b-a
    if c=="11":
        # horizontal clip: blurred fill + sharp centre, slow push
        vf=(f"split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.12[bg];"
            f"[b]scale=1180:-2:flags=lanczos,unsharp=5:5:0.5,crop=1080:ih[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-80,{GRADE},fps=30,format=yuv420p")
    else:
        vf=f"scale=1080:1920:flags=lanczos,unsharp=5:5:0.6:5:5:0.0,{GRADE},fps=30,format=yuv420p"
    subprocess.run(["ffmpeg","-loglevel","error","-y","-ss",str(a),"-t",str(d),"-i",f"/root/edit/src/c{c}.mp4",
        "-filter_complex",vf,"-af","aresample=48000,volume=0.18","-ac","2","-c:v","libx264","-preset","veryfast","-crf","17","-c:a","aac","-b:a","160k",out],check=True)
    lst.append(f"file '{out}'"); print(f"{k:02d} c{c} {a}-{b} @ {tot:.2f}"); tot+=d
open("/root/edit/seg/list.txt","w").write("\n".join(lst))
subprocess.run(["ffmpeg","-loglevel","error","-y","-f","concat","-safe","0","-i","/root/edit/seg/list.txt","-c","copy","/root/edit/base.mp4"],check=True)
print("total",tot)
