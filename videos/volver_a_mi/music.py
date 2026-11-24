import numpy as np, wave, sys
sr=48000; bpm=66; beat=60/bpm; bar=4*beat
# Progression in C: Cmaj9 - Am7 - Fmaj7 - G(add9/sus)
chords=[[48,55,64,67,74],[45,52,60,64,67],[41,48,57,64,69],[43,50,59,62,69]]
arp=[[72,76,79,74],[69,72,76,79],[69,72,77,76],[67,71,74,79]]
dur=float(sys.argv[2]); n=int(sr*dur); out=np.zeros((n,2))
f=lambda m:440*2**((m-69)/12)
t_all=np.arange(n)/sr
def pad(m,start,length,amp):
    i0=int(start*sr); L=min(int(length*sr),n-i0)
    if L<=0: return
    t=np.arange(L)/sr; env=np.minimum(1,t/1.2)*np.minimum(1,(length-t)/1.5)
    env=np.clip(env,0,1)
    for det,pan in((-0.12,0.3),(0.12,0.7)):
        fr=f(m)*2**(det/12/8)
        s=np.sin(2*np.pi*fr*t)+0.25*np.sin(4*np.pi*fr*t)+0.08*np.sin(6*np.pi*fr*t)
        s*=env*amp*(1+0.1*np.sin(2*np.pi*0.3*t))
        out[i0:i0+L,0]+=s*(1-pan); out[i0:i0+L,1]+=s*pan
def piano(m,start,amp,pan):
    i0=int(start*sr); L=min(int(3.5*sr),n-i0)
    if L<=0: return
    t=np.arange(L)/sr; fr=f(m)
    s=sum(a*np.sin(2*np.pi*fr*k*t)*np.exp(-t*(1.2+k*0.9)) for k,a in ((1,1),(2,.45),(3,.18),(4,.08)))
    s*=np.minimum(1,t/0.005)*amp
    out[i0:i0+L,0]+=s*(1-pan); out[i0:i0+L,1]+=s*pan
t=0;k=0
while t<dur:
    c=chords[k%4]
    for m in c: pad(m,t,bar+1.0,0.05)
    pad(c[0]-12,t,bar+1.0,0.07)
    if t>=bar*1:  # piano enters after first bar
        for j,m in enumerate(arp[k%4]):
            piano(m,t+j*beat,0.16 if j==0 else 0.11,0.35+0.3*(j%2))
    t+=bar;k+=1
out*=np.minimum(1,t_all/3)[:,None]*np.clip((dur-t_all)/4,0,1)[:,None]
out/=np.abs(out).max()*1.12
w=wave.open(sys.argv[1],'wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr)
w.writeframes((out*32767).astype(np.int16).tobytes());w.close()
