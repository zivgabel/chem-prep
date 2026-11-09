# -*- coding: utf-8 -*-
"""Generate the periodic-table map and Aufbau diagram SVGs for the intro chapter."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
SYM = {(1,1):"H",(1,18):"He",(2,1):"Li",(2,2):"Be",(2,13):"B",(2,14):"C",(2,15):"N",(2,16):"O",(2,17):"F",(2,18):"Ne",
 (3,1):"Na",(3,2):"Mg",(3,13):"Al",(3,14):"Si",(3,15):"P",(3,16):"S",(3,17):"Cl",(3,18):"Ar",
 (4,1):"K",(4,2):"Ca",(4,26-18):"Fe",(4,11):"Cu",(4,31-18):"Ga",(4,14):"Ge",(4,15):"As",(4,16):"Se",(4,17):"Br",(4,18):"Kr",
 (5,1):"Rb",(5,14):"Sn",(5,15):"Sb",(5,16):"Te",(5,17):"I",(5,18):"Xe",(6,1):"Cs",(6,2):"Ba",(6,11):"Au",(6,14):"Pb",(6,16):"Po",(6,17):"At",(6,18):"Rn",(7,1):"Fr",(7,2):"Ra"}
METALLOID = {(2,13),(3,14),(4,14),(4,15),(5,15),(5,16),(6,17)}
NONMETAL = {(1,1),(2,14),(2,15),(2,16),(2,17),(3,15),(3,16),(3,17),(4,16),(4,17),(5,17)}
def exists(p,g):
    if p==1: return g in (1,18)
    if p in (2,3): return g<=2 or g>=13
    return True
def cls(p,g):
    if g==18: return "pt-ng"
    if (p,g) in NONMETAL: return "pt-nm"
    if (p,g) in METALLOID: return "pt-md"
    return "pt-m"
W,H,X0,Y0 = 33,30,64,52
o = ['<svg viewBox="0 0 700 360" role="img" aria-label="מפה של הטבלה המחזורית: מחזורים, קבוצות, מתכות ואל-מתכות" class="pt">']
for g in range(1,19):
    o.append(f'<text x="{X0+(g-1)*W+W/2-1.5:.1f}" y="{Y0-8}" text-anchor="middle" class="sm">{g}</text>')
for p in range(1,8):
    o.append(f'<text x="{X0-12}" y="{Y0+(p-1)*H+H/2+4:.1f}" text-anchor="middle" class="sm">{p}</text>')
    for g in range(1,19):
        if not exists(p,g): continue
        x,y = X0+(g-1)*W, Y0+(p-1)*H
        o.append(f'<rect class="{cls(p,g)}" x="{x}" y="{y}" width="{W-3}" height="{H-3}" rx="3"/>')
        if (p,g) in SYM:
            o.append(f'<text x="{x+(W-3)/2:.1f}" y="{y+H/2+2:.1f}" text-anchor="middle" class="pt-t">{SYM[(p,g)]}</text>')
# labels
o.append(f'<text x="{X0+9*W-1.5}" y="{Y0-28}" text-anchor="middle" class="b" direction="rtl">קבוצה (טור) – תכונות כימיות דומות</text>')
o.append(f'<text x="22" y="{Y0+3.5*H}" text-anchor="middle" class="b" direction="rtl" transform="rotate(-90 22 {Y0+3.5*H})">מחזור (שורה)</text>')
yb = Y0+7*H+18
for a,b,t in [(1,2,"גוש s"),(3,12,"גוש d – מתכות מעבר"),(13,18,"גוש p")]:
    x1,x2 = X0+(a-1)*W, X0+b*W-3
    o.append(f'<path class="ln-d" d="M{x1},{yb-8} V{yb-4} H{x2} V{yb-8}"/>')
    o.append(f'<text x="{(x1+x2)/2:.1f}" y="{yb+12}" text-anchor="middle" class="sm" direction="rtl">{t}</text>')
ly = yb+40
for i,(c,t) in enumerate([("pt-m","מתכות"),("pt-md","מטלואידים"),("pt-nm","אל-מתכות"),("pt-ng","גזים אצילים")]):
    x = 600 - i*150
    o.append(f'<rect class="{c}" x="{x}" y="{ly-13}" width="16" height="16" rx="3"/><text x="{x-8}" y="{ly}" text-anchor="start" direction="rtl">{t}</text>')
o.append('</svg>')
io.open(os.path.join(HERE,"pt.svg"),"w",encoding="utf-8").write("\n".join(o))

# Aufbau diagonal diagram
L = "spdf"
maxl = {1:0,2:1,3:2,4:3,5:3,6:2,7:1}
cx = lambda l: 70+l*78
cy = lambda n: 44+(n-1)*38
a = ['<svg viewBox="0 0 400 320" role="img" aria-label="סדר מילוי תת-הרמות לפי כלל האלכסונים" class="auf">',
     '<defs><marker id="i0-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path class="fa" d="M0,0 L10,5 L0,10 z"/></marker></defs>']
order = []
for k in range(1,9):
    cells = [(n,k-n) for n in range(1,8) if 0 <= k-n <= maxl[n]]
    cells.sort(key=lambda c: c[0])  # small n (top-right) first
    if not cells: continue
    order += [f"{n}{L[l]}" for n,l in cells]
    (n1,l1),(n2,l2) = cells[0], cells[-1]
    x1,y1 = cx(l1)+30, cy(n1)-16
    x2,y2 = cx(l2)-30, cy(n2)+16
    a.append(f'<line class="ln-ac" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-end="url(#i0-arr)" opacity=".75"/>')
for n in range(1,8):
    for l in range(maxl[n]+1):
        a.append(f'<rect class="bx" x="{cx(l)-22}" y="{cy(n)-13}" width="44" height="26" rx="6"/><text x="{cx(l)}" y="{cy(n)+5}" text-anchor="middle" class="b">{n}{L[l]}</text>')
a.append('</svg>')
io.open(os.path.join(HERE,"aufbau.svg"),"w",encoding="utf-8").write("\n".join(a))
print(" ".join(order))
