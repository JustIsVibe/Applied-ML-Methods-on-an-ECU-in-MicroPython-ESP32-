import time
from machine import Pin, ADC
ADC_PIN=34; SAMPLE_MS=50; EXIT_HOLD_MS=1200
adc=ADC(Pin(ADC_PIN))
try: adc.atten(ADC.ATTN_11DB)
except: pass
btn=Pin(0,Pin.IN,Pin.PULL_UP); label=-1; last_btn=1; last_toggle=0; press=None
print("timestamp_ms,raw,label"); t0=time.ticks_ms()
try:
    while True:
        now=time.ticks_ms(); b=btn.value()
        if b==0 and last_btn==1: press=now
        if b==1 and last_btn==0 and press is not None:
            dur=time.ticks_diff(now,press)
            if dur<EXIT_HOLD_MS and time.ticks_diff(now,last_toggle)>250:
                last_toggle=now; label = 0 if label==-1 else (1 if label==0 else 0)
                print("# label toggled to", label)
            press=None
        if b==0 and press is not None and time.ticks_diff(now,press)>=EXIT_HOLD_MS:
            print("# exit"); break
        last_btn=b
        raw=adc.read(); ts=time.ticks_diff(time.ticks_ms(),t0)
        print("{},{},{}".format(ts, raw, label))
        time.sleep_ms(SAMPLE_MS)
except KeyboardInterrupt:
    print("# interrupted")
