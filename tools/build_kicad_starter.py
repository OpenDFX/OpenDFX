"""Build the OpenDFX starter project for KiCad 10 (M12): kicad/opendfx-starter/.

Run: python3 tools/build_kicad_starter.py

Needs KiCad 10 (its Python module, pcbnew). Run it again after any change to tools/kicad_rules.yaml,
then run tools/build_kicad_rules.py, which copies the rules file into the project.

The project is an empty two-layer board with:
  - the OpenDFX rules file (opendfx-starter.kicad_dru), written by tools/build_kicad_rules.py;
  - the solder mask web set in Board Setup, which the rules file can't set (PCB-DFA-032);
  - Board Setup minimums set to the OpenDFX minimum values, so KiCad's own checks agree with the rules file.
KiCad's own net class defaults (0.2 mm clearance, 0.25 mm tracks, 0.6 mm vias with 0.3 mm holes) already
sit above the OpenDFX recommended values, so they are left as they are.
"""
from pathlib import Path

import pcbnew
import yaml
from pcbnew import FromMM as mm

ROOT = Path(__file__).resolve().parent.parent
FOLDER = ROOT / "kicad" / "opendfx-starter"
PCB = FOLDER / "opendfx-starter.kicad_pcb"


def main():
    checks = {c["key"]: c for c in yaml.safe_load((ROOT / "tools" / "kicad_rules.yaml").read_text())["checks"]}

    def low(key):
        return mm(float(checks[key]["minimum"]))

    FOLDER.mkdir(parents=True, exist_ok=True)
    board = pcbnew.NewBoard(str(PCB))
    ds = board.GetDesignSettings()
    ds.m_SolderMaskMinWidth = mm(float(checks["mask-web"]["recommended"]))
    ds.m_MinClearance = low("copper-spacing")
    ds.m_TrackMinWidth = low("trace-width")
    ds.m_HoleClearance = low("hole-clearance")
    ds.m_MinThroughDrill = low("drill-size")
    ds.m_ViasMinAnnularWidth = low("annular-ring")
    ds.m_ViasMinSize = low("drill-size") + 2 * low("annular-ring")
    ds.m_CopperEdgeClearance = low("copper-edge")
    ds.m_MinSilkTextHeight = low("legend-height")
    ds.m_MinSilkTextThickness = low("legend-line")
    ds.m_SilkClearance = low("legend-clearance")
    pcbnew.SaveBoard(str(PCB), board)
    print(f"Wrote {PCB.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
