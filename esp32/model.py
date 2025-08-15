def _is_leaf(i, L, R): return L[i]==-1 and R[i]==-1
def _argmax(a):
    bi, bv = 0, a[0]
    for i in range(1,len(a)):
        if a[i]>bv: bi,bv=i,a[i]
    return bi
def predict_tree(t, x):
    f, th, L, R, val = t["feature"], t["threshold"], t["left"], t["right"], t["value"]
    classes = t.get("classes",[0,1]); i=0
    while True:
        if _is_leaf(i,L,R) or f[i]<0: return classes[_argmax(val[i])]
        i = L[i] if x[f[i]] <= th[i] else R[i]
def predict_forest(forest, x):
    votes={}
    for t in forest:
        c=predict_tree(t,x); votes[c]=votes.get(c,0)+1
    return max(votes, key=votes.get)
