import argparse, json
import pandas as pd, numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def build_features(raw, window=8):
    vals = raw.values.astype(float)
    feat=[]; buf=[]
    for v in vals:
        buf.append(v)
        if len(buf)>window: buf.pop(0)
        feat.append(float(np.mean(buf)))
    return np.array(feat).reshape(-1,1)

def export_tree(clf, classes, Xn):
    sk=clf.tree_
    return {
        "n_features": int(Xn.shape[1]),
        "classes": [int(c) for c in classes],
        "feature": [int(f) for f in sk.feature],
        "threshold": [float(t) for t in sk.threshold],
        "left": [int(l) for l in sk.children_left],
        "right":[int(r) for r in sk.children_right],
        "value":[[int(v) for v in sk.value[i][0]] for i in range(sk.node_count)]
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out", default="model_bundle.json")
    ap.add_argument("--max_depth", type=int, default=4)
    ap.add_argument("--window", type=int, default=8)
    a=ap.parse_args()

    df=pd.read_csv(a.csv)
    if not {"raw","label"}.issubset(df.columns):
        raise SystemExit("CSV must contain columns: raw,label (+timestamp_ms optional)")

    X=build_features(df["raw"], window=a.window)
    y=df["label"].values.astype(int)
    fmin=[float(np.min(X[:,0]))]; fmax=[float(np.max(X[:,0]))]
    denom=(fmax[0]-fmin[0]) or 1.0
    Xn=(X - fmin[0]) / denom

    Xtr,Xte,ytr,yte=train_test_split(Xn,y,test_size=0.25,random_state=0,stratify=y)
    clf=DecisionTreeClassifier(max_depth=a.max_depth, random_state=0).fit(Xtr,ytr)
    print(classification_report(yte, clf.predict(Xte)))

    bundle={"tree": export_tree(clf, np.unique(y), Xn), "feat_min": fmin, "feat_max": fmax}
    with open(a.out,"w") as f: json.dump(bundle,f,indent=2)
    print("Saved", a.out)

if __name__=="__main__": main()
