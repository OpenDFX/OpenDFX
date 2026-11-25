"""Prove that every rule in kicad/opendfx.kicad_dru fires, and only where it should (M12).

Run: python3 kicad/tests/test_rules.py

Needs KiCad 10 (its Python module, pcbnew, and kicad-cli).
It draws a test board, kicad/tests/opendfx-test.kicad_pcb, with one deliberate mistake for each rule
and a matching feature that is just good enough to pass. Half of the cases sit inside a rule area named
"OpenDFX minimum", where the minimum values apply. It then runs KiCad's design rule check and compares
what KiCad reports with what each case expects.

Every case is tagged with a net name, a reference designator or a piece of text, so each report can be
traced to its case. Open the board in KiCad to see the cases; each has a label on the drawing layer.

The test project relaxes KiCad's own limits (net class clearance 0.1 mm, Board Setup minimums at zero),
as a designer working to a fab's limits might, so only the OpenDFX rules are being tested.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pcbnew
from pcbnew import VECTOR2I
from pcbnew import FromMM as mm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
RULES = ROOT / "kicad" / "opendfx.kicad_dru"
NAME = "opendfx-test"

W, H = 140, 110            # board size, mm
AREA = (80, 5, W, H - 5)   # the "OpenDFX minimum" rule area, reaching the right-hand edge

board = pcbnew.BOARD()
expected = set()           # (tag, words that must appear in the rule name)
passing = set()            # tags that must not appear in any OpenDFX report
nets = {}


def V(x, y):
    return VECTOR2I(mm(x), mm(y))


def expect(tag, words=None):
    if words:
        expected.add((tag, words))
    else:
        passing.add(tag)


def net(name):
    if name not in nets:
        n = pcbnew.NETINFO_ITEM(board, name)
        board.Add(n)
        nets[name] = n
    return nets[name]


def label(x, y, text):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(text)
    t.SetLayer(pcbnew.Cmts_User)
    t.SetTextSize(VECTOR2I(mm(0.6), mm(0.6)))
    t.SetTextThickness(mm(0.1))
    t.SetPosition(V(x, y - 1.5))
    board.Add(t)


def line(layer, x1, y1, x2, y2, width=0.1):
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(V(x1, y1))
    s.SetEnd(V(x2, y2))
    s.SetLayer(layer)
    s.SetWidth(mm(width))
    board.Add(s)


def track(x1, y1, x2, y2, width, name, layer=pcbnew.F_Cu):
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(V(x1, y1))
    t.SetEnd(V(x2, y2))
    t.SetWidth(mm(width))
    t.SetLayer(layer)
    t.SetNet(net(name))
    board.Add(t)


def via(x, y, diameter, drill, name):
    v = pcbnew.PCB_VIA(board)
    v.SetPosition(V(x, y))
    v.SetWidth(mm(diameter))
    v.SetDrill(mm(drill))
    v.SetNet(net(name))
    board.Add(v)


def footprint(ref, x, y):
    f = pcbnew.FOOTPRINT(board)
    f.SetReference(ref)
    f.SetValue(ref)
    f.SetPosition(V(x, y))
    f.Reference().SetVisible(False)
    f.Value().SetVisible(False)
    board.Add(f)
    return f


def pad(f, x, y, kind, size, hole=None, name=None, shape=pcbnew.PAD_SHAPE_CIRCLE, layers=None, testpoint=False):
    p = pcbnew.PAD(f)
    p.SetNumber(str(len(f.Pads()) + 1))
    sx, sy = size if isinstance(size, tuple) else (size, size)
    p.SetShape(shape)
    p.SetSize(VECTOR2I(mm(sx), mm(sy)))
    if kind == "smd":
        p.SetAttribute(pcbnew.PAD_ATTRIB_SMD)
        p.SetLayerSet(layers or p.SMDMask())
    else:
        hx, hy = hole if isinstance(hole, tuple) else (hole, hole)
        p.SetDrillShape(pcbnew.PAD_DRILL_SHAPE_OBLONG if hx != hy else pcbnew.PAD_DRILL_SHAPE_CIRCLE)
        p.SetDrillSize(VECTOR2I(mm(hx), mm(hy)))
        if kind == "pth":
            p.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
            p.SetLayerSet(p.PTHMask())
        else:
            p.SetAttribute(pcbnew.PAD_ATTRIB_NPTH)
            p.SetLayerSet(p.UnplatedHoleMask())
    if testpoint:
        p.SetProperty(pcbnew.PAD_PROP_TESTPOINT)
    if name:
        p.SetNet(net(name))
    f.Add(p)
    p.SetPosition(V(x, y))
    return p


def text(x, y, content, height, thickness):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(content)
    t.SetLayer(pcbnew.F_SilkS)
    t.SetTextSize(VECTOR2I(mm(height), mm(height)))
    t.SetTextThickness(mm(thickness))
    t.SetPosition(V(x, y))
    board.Add(t)


def draw():
    for x1, y1, x2, y2 in [(0, 0, W, 0), (W, 0, W, H), (W, H, 0, H), (0, H, 0, 0)]:
        line(pcbnew.Edge_Cuts, x1, y1, x2, y2)
    z = pcbnew.ZONE(board)
    z.SetIsRuleArea(True)
    z.SetZoneName("OpenDFX minimum")
    z.SetLayerSet(pcbnew.LSET.AllLayersMask())
    for allow in ("SetDoNotAllowTracks", "SetDoNotAllowVias", "SetDoNotAllowPads", "SetDoNotAllowZoneFills", "SetDoNotAllowFootprints"):
        getattr(z, allow)(False)
    outline = z.Outline()
    outline.NewOutline()
    x1, y1, x2, y2 = AREA
    for x, y in [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]:
        outline.Append(mm(x), mm(y))
    board.Add(z)

    # Columns: x = 10 to 70 outside the area, 90 to 125 inside it. Rows every 6 mm.
    # PCB-DFM-020 trace width
    label(10, 8, "trace width 0.12 (fail), 0.15 (pass)")
    track(10, 8, 20, 8, 0.12, "TW_A"); expect("TW_A", "traces at least 0.15 mm wide")
    track(25, 8, 35, 8, 0.15, "TW_B"); expect("TW_B")
    label(90, 8, "inside: 0.12 (pass), 0.08 (fail)")
    track(90, 8, 100, 8, 0.12, "TW_C"); expect("TW_C")
    track(105, 8, 115, 8, 0.08, "TW_D"); expect("TW_D", "traces at least 0.1 mm wide, inside")

    # PCB-DFM-020 copper spacing
    label(10, 14, "spacing 0.12 (fail), 0.15 (pass)")
    track(10, 14, 20, 14, 0.2, "SP_A1"); track(10, 14.32, 20, 14.32, 0.2, "SP_A2")
    expect("SP_A1", "copper at least 0.15 mm from copper"); expect("SP_A2", "copper at least 0.15 mm from copper")
    track(25, 14, 35, 14, 0.2, "SP_B1"); track(25, 14.35, 35, 14.35, 0.2, "SP_B2"); expect("SP_B1"); expect("SP_B2")
    label(90, 14, "inside: 0.12 (pass), 0.08 (fail)")
    track(90, 14, 100, 14, 0.2, "SP_C1"); track(90, 14.32, 100, 14.32, 0.2, "SP_C2"); expect("SP_C1"); expect("SP_C2")
    track(105, 14, 115, 14, 0.2, "SP_D1"); track(105, 14.28, 115, 14.28, 0.2, "SP_D2")
    expect("SP_D1", "0.1 mm from copper on another net, inside"); expect("SP_D2", "0.1 mm from copper on another net, inside")

    # PCB-DFM-022 copper to a drilled hole (non-plated 1 mm holes, so no via copper gets in the way)
    label(10, 20, "copper to hole 0.22 (fail), 0.25 (pass)")
    pad(footprint("H1", 12, 20), 12, 20, "npth", 1.0, 1.0); track(12.72 + 0.1, 17, 12.72 + 0.1, 23, 0.2, "HC_A")
    expect("HC_A", "0.25 mm from the edge of a drilled hole")
    pad(footprint("H2", 27, 20), 27, 20, "npth", 1.0, 1.0); track(27.75 + 0.1, 17, 27.75 + 0.1, 23, 0.2, "HC_B"); expect("HC_B")
    label(90, 20, "inside: 0.22 (pass), 0.15 (fail)")
    pad(footprint("H3", 92, 20), 92, 20, "npth", 1.0, 1.0); track(92.72 + 0.1, 17, 92.72 + 0.1, 23, 0.2, "HC_C"); expect("HC_C")
    pad(footprint("H4", 107, 20), 107, 20, "npth", 1.0, 1.0); track(107.65 + 0.1, 17, 107.65 + 0.1, 23, 0.2, "HC_D")
    expect("HC_D", "0.2 mm from the edge of a drilled hole, inside")

    # PCB-DFM-024 drill size, and PCB-DFM-026 annular ring
    label(10, 28, "via drill 0.22 (fail), KiCad default via 0.6/0.3 (pass), via ring 0.125 (fail)")
    via(12, 28, 0.6, 0.22, "DR_A"); expect("DR_A", "drilled holes at least 0.25 mm")
    via(20, 28, 0.6, 0.3, "DR_B"); expect("DR_B")
    via(28, 28, 0.55, 0.3, "AR_A"); expect("AR_A", "annular ring of at least 0.15 mm")
    label(40, 28, "pad drill 0.22 (fail), pad ring 0.1 (fail)")
    pad(footprint("DRP", 42, 28), 42, 28, "pth", 0.6, 0.22, "DR_P"); expect("DR_P", "drilled holes at least 0.25 mm")
    pad(footprint("ARP", 50, 28), 50, 28, "pth", 1.0, 0.8, "AR_P"); expect("AR_P", "annular ring of at least 0.15 mm")
    label(90, 28, "inside: drill 0.22 (pass), 0.18 (fail); ring 0.125 (pass), 0.1 (fail)")
    via(92, 28, 0.6, 0.22, "DR_C"); expect("DR_C")
    via(100, 28, 0.5, 0.18, "DR_D"); expect("DR_D", "drilled holes at least 0.2 mm in diameter, inside")
    via(108, 28, 0.55, 0.3, "AR_C"); expect("AR_C")
    via(116, 28, 0.5, 0.3, "AR_D"); expect("AR_D", "annular ring of at least 0.125 mm, inside")

    # PCB-DFM-002 copper to the board edge: left edge outside the area, right edge inside it
    label(3, 36, "copper to edge 0.4 (fail), 0.5 (pass)")
    track(0.4 + 0.1, 34, 0.4 + 0.1, 40, 0.2, "ED_A"); expect("ED_A", "copper at least 0.5 mm from the board edge")
    track(0.5 + 0.1, 44, 0.5 + 0.1, 50, 0.2, "ED_B"); expect("ED_B")
    label(120, 36, "inside: 0.3 (pass), 0.2 (fail)")
    track(W - 0.4, 34, W - 0.4, 40, 0.2, "ED_C"); expect("ED_C")
    track(W - 0.3, 44, W - 0.3, 50, 0.2, "ED_D"); expect("ED_D", "copper at least 0.25 mm from the board edge, inside")

    # PCB-DFM-007 copper on a non-plated hole; PCB-DFM-042 slots
    label(10, 56, "copper pad on non-plated hole (fail), slot 0.8 (fail), slot 1.0 (pass)")
    pad(footprint("NPC", 12, 56), 12, 56, "npth", 2.0, 1.0); expect("NPC", "no copper pad on a non-plated hole")
    pad(footprint("SLA", 22, 56), 22, 56, "npth", (2.0, 0.8), (2.0, 0.8), shape=pcbnew.PAD_SHAPE_OVAL)
    expect("SLA", "non-plated slots at least 1 mm wide")
    pad(footprint("SLB", 32, 56), 32, 56, "npth", (2.0, 1.0), (2.0, 1.0), shape=pcbnew.PAD_SHAPE_OVAL); expect("SLB")
    label(40, 62, "plated slot 0.8 (fail)")
    pad(footprint("SPA", 42, 62), 42, 62, "pth", (2.6, 1.4), (2.0, 0.8), "SL_PA", shape=pcbnew.PAD_SHAPE_OVAL)
    expect("SL_PA", "plated slots at least 1 mm wide")
    label(90, 56, "inside: plated slot 0.8 (pass), 0.4 (fail)")
    pad(footprint("SPC", 92, 56), 92, 56, "pth", (2.6, 1.4), (2.0, 0.8), "SL_PC", shape=pcbnew.PAD_SHAPE_OVAL); expect("SL_PC")
    pad(footprint("SPD", 102, 56), 102, 56, "pth", (1.6, 1.0), (1.0, 0.4), "SL_PD", shape=pcbnew.PAD_SHAPE_OVAL)
    expect("SL_PD", "plated slots at least 0.5 mm wide, inside")

    # PCB-DFM-039 legend text
    label(10, 68, "legend 0.9 tall (fail), 1.0 tall with 0.15 lines (pass), 0.12 lines (fail)")
    text(12, 68, "LH_A", 0.9, 0.15); expect("LH_A", "legend text at least 1 mm tall")
    text(22, 68, "LH_B", 1.0, 0.15); expect("LH_B")
    text(32, 68, "LL_A", 1.0, 0.12); expect("LL_A", "lines at least 0.15 mm wide")
    label(40, 68, "visible reference designators: KiCad's standard 1.0/0.15 (pass), 0.8 tall (fail)")
    f = footprint("RDOK", 42, 68); f.Reference().SetVisible(True); f.Reference().SetLayer(pcbnew.F_SilkS)
    f.Reference().SetTextSize(VECTOR2I(mm(1.0), mm(1.0))); f.Reference().SetTextThickness(mm(0.15)); expect("RDOK")
    f = footprint("RDSM", 52, 68); f.Reference().SetVisible(True); f.Reference().SetLayer(pcbnew.F_SilkS)
    f.Reference().SetTextSize(VECTOR2I(mm(0.8), mm(0.8))); f.Reference().SetTextThickness(mm(0.15))
    expect("RDSM", "legend text at least 1 mm tall")
    label(90, 68, "inside: 0.9 tall (pass), 0.7 tall (fail)")
    text(92, 68, "LH_C", 0.9, 0.15); expect("LH_C")
    text(102, 68, "LH_D", 0.7, 0.15); expect("LH_D", "legend text at least 0.8 mm tall, inside")

    # PCB-DFM-040 legend to exposed copper; legend over a masked trace is fine
    label(10, 74, "legend 0.05 from a pad (fail), 0.15 (pass), over a masked trace (pass)")
    pad(footprint("LC_A", 12, 74), 12, 74, "smd", (1.0, 1.0), name="LC_A", shape=pcbnew.PAD_SHAPE_RECTANGLE)
    line(pcbnew.F_SilkS, 12.5 + 0.05 + 0.075, 72, 12.5 + 0.05 + 0.075, 76, 0.15); expect("LC_A", "legend at least 0.1 mm from exposed copper")
    pad(footprint("LC_B", 22, 74), 22, 74, "smd", (1.0, 1.0), name="LC_B", shape=pcbnew.PAD_SHAPE_RECTANGLE)
    line(pcbnew.F_SilkS, 22.5 + 0.15 + 0.075, 72, 22.5 + 0.15 + 0.075, 76, 0.15); expect("LC_B")
    track(30, 74, 36, 74, 0.25, "LC_C"); line(pcbnew.F_SilkS, 33, 72, 33, 76, 0.15); expect("LC_C")

    # PCB-DFT-008 test point pads, size and spacing
    label(10, 82, "test pad 0.8 (fail); two 1.0 pads 2.0 apart (fail), 2.54 apart (pass)")
    pad(footprint("TPA", 12, 82), 12, 82, "smd", 0.8, name="TP_A", testpoint=True); expect("TP_A", "test point pads at least 1.0 mm")
    f = footprint("TPB", 22, 82)
    pad(f, 22, 82, "smd", 1.0, name="TP_B1", testpoint=True); pad(f, 24, 82, "smd", 1.0, name="TP_B2", testpoint=True)
    expect("TP_B1", "test points at least 2.54 mm apart"); expect("TP_B2", "test points at least 2.54 mm apart")
    f = footprint("TPC", 32, 82)
    pad(f, 32, 82, "smd", 1.0, name="TP_C1", testpoint=True); pad(f, 34.54, 82, "smd", 1.0, name="TP_C2", testpoint=True)
    expect("TP_C1"); expect("TP_C2")
    label(90, 82, "inside: pad 0.85 (fail); 0.9 pads 1.9 apart (pass), 1.7 apart (fail)")
    pad(footprint("TPD", 92, 82), 92, 82, "smd", 0.85, name="TP_D", testpoint=True)
    expect("TP_D", "test point pads at least 0.9 mm in diameter, inside")
    f = footprint("TPE", 100, 82)
    pad(f, 100, 82, "smd", 0.9, name="TP_E1", testpoint=True); pad(f, 101.9, 82, "smd", 0.9, name="TP_E2", testpoint=True)
    expect("TP_E1"); expect("TP_E2")
    f = footprint("TPF", 110, 82)
    pad(f, 110, 82, "smd", 0.9, name="TP_F1", testpoint=True); pad(f, 111.7, 82, "smd", 0.9, name="TP_F2", testpoint=True)
    expect("TP_F1", "test points at least 1.9 mm apart"); expect("TP_F2", "test points at least 1.9 mm apart")

    # PCB-DFT-009 test points to the board edge: bottom edge outside the area, right edge inside it
    label(40, H - 6, "test pad 4 mm from edge (fail), 5 mm (pass)")
    pad(footprint("TPG", 42, H - 4), 42, H - 4, "smd", 1.0, name="TP_G", testpoint=True)
    expect("TP_G", "test points at least 5 mm from the board edge")
    pad(footprint("TPH", 52, H - 5.5), 52, H - 5.5, "smd", 1.0, name="TP_H", testpoint=True); expect("TP_H")
    label(125, 90, "inside: 3.5 (pass), 2.5 (fail)")
    pad(footprint("TPI", W - 4, 90), W - 4, 90, "smd", 1.0, name="TP_I", testpoint=True); expect("TP_I")
    pad(footprint("TPJ", W - 3, 96), W - 3, 96, "smd", 1.0, name="TP_J", testpoint=True)
    expect("TP_J", "test points at least 3 mm from the board edge, inside")

    # PCB-DFA-043 bottom surface-mount pads near through-hole pads (a warning)
    bottom = pcbnew.LSET()
    for layer in (pcbnew.B_Cu, pcbnew.B_Mask, pcbnew.B_Paste):
        bottom.AddLayer(layer)
    label(10, 92, "bottom pad 2.5 from a through-hole pad (warn), 3.2 (pass)")
    f = footprint("WS_A", 12, 92)
    pad(f, 12, 92, "pth", 1.6, 1.0, "WS_A1"); pad(f, 12 + 0.8 + 2.5 + 0.5, 92, "smd", 1.0, name="WS_A2", layers=bottom)
    expect("WS_A1", "bottom surface-mount pads at least 3 mm"); expect("WS_A2", "bottom surface-mount pads at least 3 mm")
    f = footprint("WS_B", 30, 92)
    pad(f, 30, 92, "pth", 1.6, 1.0, "WS_B1"); pad(f, 30 + 0.8 + 3.2 + 0.5, 92, "smd", 1.0, name="WS_B2", layers=bottom)
    expect("WS_B2")
    label(90, 92, "inside: 2.5 (pass), 1.5 (warn)")
    f = footprint("WS_C", 92, 92)
    pad(f, 92, 92, "pth", 1.6, 1.0, "WS_C1"); pad(f, 92 + 0.8 + 2.5 + 0.5, 92, "smd", 1.0, name="WS_C2", layers=bottom)
    expect("WS_C2")
    f = footprint("WS_D", 105, 92)
    pad(f, 105, 92, "pth", 1.6, 1.0, "WS_D1"); pad(f, 105 + 0.8 + 1.5 + 0.5, 92, "smd", 1.0, name="WS_D2", layers=bottom)
    for tag in ("WS_D1", "WS_D2"):
        expect(tag, "bottom surface-mount pads at least 2 mm from through-hole pads (wave or selective soldering), inside")
    expect("WS_B1"); expect("WS_C1")


def thermal_case():
    """PCB-DFA-044: a pour set to join pads solidly must still use thermal reliefs on a through-hole pad."""
    label(60, 33, "pour set to solid: through-hole pad gets a thermal relief, surface-mount pad stays solid")
    bottom = pcbnew.LSET()
    for layer in (pcbnew.B_Cu, pcbnew.B_Mask, pcbnew.B_Paste):
        bottom.AddLayer(layer)
    f = footprint("TR", 64, 41)
    pad(f, 64, 41, "pth", 1.6, 1.0, "TR")
    pad(f, 70, 41, "smd", (1.6, 1.6), name="TR", shape=pcbnew.PAD_SHAPE_RECTANGLE, layers=bottom)
    z = pcbnew.ZONE(board)
    z.SetLayer(pcbnew.B_Cu)
    z.SetNet(net("TR"))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
    outline = z.Outline()
    outline.NewOutline()
    for x, y in [(60, 35), (75, 35), (75, 48), (60, 48)]:
        outline.Append(mm(x), mm(y))
    board.Add(z)
    expect("TR")


def check_thermal(folder):
    """Refill the pours with the rules loaded, then look at the copper just outside each pad in eight directions.
    A thermal relief leaves a gap in some of them (KiCad puts the spokes at 45 degrees on round pads);
    a solid connection fills them all."""
    import math
    pcb = folder / f"{NAME}.kicad_pcb"
    subprocess.run(["kicad-cli", "pcb", "drc", "--refill-zones", "--save-board", "-o", str(folder / "fill.rpt"), str(pcb)],
                   check=False, capture_output=True)
    filled = pcbnew.LoadBoard(str(pcb))
    zone = next(z for z in filled.Zones() if z.GetNetname() == "TR")
    poly = zone.GetFilledPolysList(pcbnew.B_Cu)

    def ring(cx, cy, r):
        return [poly.Contains(V(cx + r * math.cos(a * math.pi / 4), cy + r * math.sin(a * math.pi / 4))) for a in range(8)]

    tht_gap = not all(ring(64, 41, 0.8 + 0.15))
    smd_solid = all(ring(70, 41, 0.8 * 1.4142 + 0.1))
    problems = []
    if not tht_gap:
        problems.append("THERMAL the through-hole pad is joined solidly to the pour; expected a thermal relief")
    if not smd_solid:
        problems.append("THERMAL the surface-mount pad lost its solid connection; the rule should only touch through-hole pads")
    return problems


def project():
    """A project as a designer working to a fab's limits might set it up: KiCad's own limits relaxed."""
    rules = {k: 0.0 for k in ("min_clearance", "min_track_width", "min_via_annular_width", "min_via_diameter",
                              "min_through_hole_diameter", "min_hole_clearance", "min_hole_to_hole",
                              "min_copper_edge_clearance", "min_silk_clearance", "min_text_height",
                              "min_text_thickness", "min_microvia_diameter", "min_microvia_drill")}
    return {
        "meta": {"filename": f"{NAME}.kicad_pro", "version": 3},
        "board": {"design_settings": {"rules": rules}},
        "net_settings": {"meta": {"version": 4}, "classes": [
            {"name": "Default", "clearance": 0.1, "track_width": 0.15, "via_diameter": 0.6, "via_drill": 0.3, "priority": 2147483647}]},
    }


RULE_RE = re.compile(r"rule '([^']*)'")


def run(folder):
    pcb = folder / f"{NAME}.kicad_pcb"
    pcbnew.SaveBoard(str(pcb), board)
    (folder / f"{NAME}.kicad_pro").write_text(json.dumps(project(), indent=2))
    shutil.copy(RULES, folder / f"{NAME}.kicad_dru")
    report = folder / "drc.json"
    subprocess.run(["kicad-cli", "pcb", "drc", "--format", "json", "--severity-all", "-o", str(report), str(pcb)],
                   check=False, capture_output=True)
    found, untagged, severities = set(), [], {}
    for v in json.loads(report.read_text())["violations"]:
        m = RULE_RE.search(v["description"])
        if not m or not m.group(1).startswith("PCB-"):
            continue  # one of KiCad's own checks, not an OpenDFX rule
        tags = set()
        for item in v["items"]:
            d = item["description"]
            # Prefer the net name, then the text, then the footprint's reference designator.
            for pattern in (r"\[([A-Z][A-Z_0-9]+)\]", r"'([A-Z]{2}_[A-Z])'", r"of ([A-Z][A-Z_]+)\b"):
                m2 = re.search(pattern, d)
                if m2:
                    tags.add(m2.group(1))
                    break
        if not tags:
            untagged.append(v["description"])
        for t in tags:
            found.add((t, m.group(1)))
            severities[(t, m.group(1))] = v["severity"]
    return found, untagged, severities


def main():
    draw()
    thermal_case()
    with tempfile.TemporaryDirectory() as tmp:
        found, untagged, severities = run(Path(tmp))
        thermal_problems = check_thermal(Path(tmp))
        for suffix in (".kicad_pcb", ".kicad_pro"):  # keep a copy to open in KiCad
            shutil.copy(Path(tmp) / f"{NAME}{suffix}", HERE / f"{NAME}{suffix}")
    shutil.copy(RULES, HERE / f"{NAME}.kicad_dru")
    failures = []
    for tag, words in sorted(expected):
        hits = [rule for t, rule in found if t == tag and words in rule]
        if not hits:
            failures.append(f"MISSED  {tag}: expected a report containing '{words}'")
    expected_tags = {t for t, _ in expected}
    for tag, rule in sorted(found):
        if tag in passing:
            failures.append(f"EXTRA   {tag} should pass, but got: {rule}")
        elif tag in expected_tags and not any(t == tag and w in rule for t, w in expected):
            failures.append(f"WRONG   {tag} got an unexpected rule: {rule}")
        elif tag not in expected_tags:
            failures.append(f"UNKNOWN {tag}: {rule}")
    for (tag, rule), sev in severities.items():
        if "wave or selective" in rule and sev != "warning":
            failures.append(f"SEVERITY {tag}: expected a warning, got {sev}")
    failures += thermal_problems
    for d in untagged:
        failures.append(f"UNTAGGED {d}")
    rules_tested = {w for _, w in expected}
    print(f"{len(expected)} expected reports, {len(passing)} passing features, {len(rules_tested)} distinct rule messages.")
    if failures:
        print("\n".join(failures))
        sys.exit(1)
    print("All OpenDFX rules fired where expected, and nowhere else.")


if __name__ == "__main__":
    main()
