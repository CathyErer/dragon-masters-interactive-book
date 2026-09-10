"""Deterministic original instrumental sketches; Python standard library only."""
import argparse,math,struct,wave
from pathlib import Path
RATE=22050
MOODS={'mystery':([57,60,64,67],.75,.10),'motion':([60,64,67,72],.375,.12),'relief':([60,64,67,71],1.5,.10)}
def build(out,seconds=12):
    out.mkdir(parents=True,exist_ok=True)
    for name,(notes,beat,gain) in MOODS.items():
        samples=[]
        for i in range(round(seconds*RATE)):
            t=i/RATE;step=int(t/beat);age=t%beat;frequency=440*2**((notes[step%len(notes)]-69)/12)
            # Plucked overtone and quiet bass, no borrowed recordings/melodies.
            env=(1-math.exp(-age*100))*math.exp(-age*3.5)
            tone=(math.sin(2*math.pi*frequency*age)+.22*math.sin(4*math.pi*frequency*age))*env
            bass=.25*math.sin(2*math.pi*(440*2**((notes[0]-24-69)/12))*t)
            edge=min(1,t/.06,(seconds-t)/.06)
            samples.append(struct.pack('<h',int(max(-1,min(1,(tone+bass)*gain*edge))*32767)))
        with wave.open(str(out/(name+'.wav')),'wb') as f:f.setparams((1,2,RATE,0,'NONE','not compressed'));f.writeframes(b''.join(samples))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();build(a.output)
