"""Build the panel-anatomy example board with KiCad 10's Python API (pcbnew).
2 x 2 panel of 70 x 45 mm boards, 10 mm rails, V-score lines on layer User.1 ("V-Score"),
board and global fiducials using KiCad's own Fiducial:Fiducial_1mm_Mask2mm footprint,
and 3/16 in tooling holes on the rails.
Set KICAD10_FOOTPRINT_DIR if KiCad's footprint libraries are not in the default place."""
import os, pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
FP_DIR = os.environ.get("KICAD10_FOOTPRINT_DIR", "/usr/share/kicad/footprints")
LIB = os.path.join(FP_DIR, "Fiducial.pretty")
MM = pcbnew.FromMM
BW, BH, RAIL = 70, 45, 10
PW, PH = 2 * BW, 2 * BH + 2 * RAIL

b = pcbnew.BOARD()
b.SetLayerName(pcbnew.User_1, "V-Score")
ds = b.GetDesignSettings()
ds.SetCopperLayerCount(2)


def seg(x1, y1, x2, y2, layer, w=0.1):
    s = pcbnew.PCB_SHAPE(b)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(pcbnew.VECTOR2I(MM(x1), MM(y1)))
    s.SetEnd(pcbnew.VECTOR2I(MM(x2), MM(y2)))
    s.SetLayer(layer)
    s.SetWidth(MM(w))
    b.Add(s)


def text(s, x, y, layer, size=1.5):
    t = pcbnew.PCB_TEXT(b)
    t.SetText(s)
    t.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
    t.SetLayer(layer)
    t.SetTextSize(pcbnew.VECTOR2I(MM(size), MM(size)))
    t.SetTextThickness(MM(size * 0.15))
    b.Add(t)


# panel outline (Edge.Cuts)
for x1, y1, x2, y2 in ((0, 0, PW, 0), (PW, 0, PW, PH), (PW, PH, 0, PH), (0, PH, 0, 0)):
    seg(x1, y1, x2, y2, pcbnew.Edge_Cuts, 0.1)
# V-score lines, edge to edge
for y in (RAIL, RAIL + BH, PH - RAIL):
    seg(0, y, PW, y, pcbnew.User_1, 0.2)
seg(BW, 0, BW, PH, pcbnew.User_1, 0.2)
text("V-SCORE", PW + 6, RAIL, pcbnew.User_1, 1.2)

fid = pcbnew.FootprintLoad(LIB, "Fiducial_1mm_Mask2mm")
n = [0]


def place(x, y, prefix="FID"):
    n[0] += 1
    f = pcbnew.FOOTPRINT(fid)
    f.SetFPID(pcbnew.LIB_ID("Fiducial", "Fiducial_1mm_Mask2mm"))
    f.SetReference(f"{prefix}{n[0]}")
    f.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
    b.Add(f)


for x, y in ((PW - 15, 5), (15, PH - 5), (PW - 15, PH - 5)):          # global fiducials on the rails
    place(x, y)
for r in range(2):                                           # two board fiducials per board
    for c in range(2):
        x0, y0 = c * BW, RAIL + r * BH
        place(x0 + 5, y0 + 5)
        place(x0 + BW - 5, y0 + BH - 5)
        text(f"BOARD {'AB'[c]}{r + 1}", x0 + BW / 2, y0 + BH / 2, pcbnew.F_SilkS, 2.0)

# 3/16 in non-plated tooling holes in the rail corners
for i, (x, y) in enumerate(((5, 5), (PW - 5, 5), (5, PH - 5), (PW - 5, PH - 5)), 1):
    f = pcbnew.FOOTPRINT(b)
    f.SetReference(f"TH{i}")
    f.Reference().SetVisible(False)
    f.Value().SetVisible(False)
    p = pcbnew.PAD(f)
    p.SetAttribute(pcbnew.PAD_ATTRIB_NPTH)
    p.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
    d = MM(4.7625)
    p.SetSize(pcbnew.VECTOR2I(d, d))
    p.SetDrillSize(pcbnew.VECTOR2I(d, d))
    ls = pcbnew.LSET.AllCuMask()
    ls.AddLayer(pcbnew.F_Mask)
    ls.AddLayer(pcbnew.B_Mask)
    p.SetLayerSet(ls)
    f.Add(p)
    f.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
    b.Add(f)

out = os.path.join(HERE, "panel-anatomy.kicad_pcb")
pcbnew.SaveBoard(out, b)
print("saved", out)
