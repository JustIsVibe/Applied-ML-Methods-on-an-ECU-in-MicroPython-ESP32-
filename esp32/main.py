import time
from machine import Pin
from sensors import AdcSensor
from features import MinMaxScaler, MeanBuffer
from model import predict_tree
from config import MODEL
LED=Pin(2,Pin.OUT); STOP=Pin(0,Pin.IN,Pin.PULL_UP)
sensor=AdcSensor(pin=34); scaler=MinMaxScaler(MODEL["feat_min"],MODEL["feat_max"])
buf=MeanBuffer(size=8); TREE=MODEL["tree"]
SAMPLE_MS=50; SMOOTH_N=5; EXIT_HOLD_MS=1200; STATS_KEEP=300
class Smo:
    def __init__(self,n=5): self.n=n; self.q=[]
    def add(self,p): self.q.append(p); 
    def maj(self):
        while len(self.q)>self.n: self.q.pop(0)
        if not self.q: return None
        c={}
        for v in self.q: c[v]=c.get(v,0)+1
        best,bc=None,-1
        for k,v in c.items():
            if v>bc: best,bc=k,v
        return best
def p95(vals):
    if not vals: return 0
    s=sorted(vals); return s[int(0.95*(len(s)-1))]
print("Starting inference loop...")
t0=time.ticks_ms(); press=None; smo=Smo(SMOOTH_N); times=[]; cnt=0
try:
    while True:
        t=time.ticks_us()
        b=STOP.value(); now=time.ticks_ms()
        if b==0 and press is None: press=now
        if b==1 and press is not None: press=None
        if b==0 and press is not None and time.ticks_diff(now,press)>=EXIT_HOLD_MS: print("# exit"); break
        raw=sensor.read_raw(); buf.add(raw); feat=buf.mean()
        x=scaler.transform([feat]); pred=predict_tree(TREE,x)
        smo.add(pred); ps=smo.maj()
        LED.value(1 if ps==1 else 0)
        dt=time.ticks_diff(time.ticks_us(),t)
        if len(times)<STATS_KEEP: times.append(dt)
        else: times[cnt%STATS_KEEP]=dt; cnt+=1
        print("ts_ms:", time.ticks_diff(time.ticks_ms(),t0), "raw:", raw, "feat:", int(feat), "x_norm:", x, "pred:", pred, "pred_smooth:", ps, "infer_us:", dt)
        time.sleep_ms(SAMPLE_MS)
except KeyboardInterrupt:
    print("# interrupted")
avg=int(sum(times)/len(times)) if times else 0; p95us=int(p95(times))
print("=== STATS ==="); print("samples:", len(times), "avg_us:", avg, "p95_us:", p95us); print("SAMPLE_MS:", SAMPLE_MS, "SMOOTH_N:", SMOOTH_N)
