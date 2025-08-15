class MinMaxScaler:
    def __init__(self, fmin, fmax): self.fmin, self.fmax = fmin, fmax
    def transform(self, xs):
        out=[]
        for i,x in enumerate(xs):
            mn, mx = self.fmin[i], self.fmax[i]
            if mx==mn: out.append(0.0)
            else:
                v=(x-mn)/(mx-mn)
                if v<0: v=0.0
                if v>1: v=1.0
                out.append(v)
        return out
class MeanBuffer:
    def __init__(self, size=8):
        self.buf=[0.0]*size; self.idx=0; self.count=0; self.size=size
    def add(self, v):
        self.buf[self.idx]=v; self.idx=(self.idx+1)%self.size
        if self.count<self.size: self.count+=1
    def mean(self):
        s=0.0
        for i in range(self.count): s+=self.buf[i]
        return s/self.count if self.count>0 else 0.0
