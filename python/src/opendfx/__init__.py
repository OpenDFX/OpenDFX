"""The recommendations of OpenDFX for Printed Circuit Boards, by Chris Denney (https://opendfx.org).

    import opendfx
    opendfx.get("PCB-DFA-006")          # one recommendation, as a dict
    opendfx.for_stage("placement")      # every recommendation for one design stage
    opendfx.search("fiducial")          # recommendations whose text contains a word
    opendfx.recommendations()           # all of them
    opendfx.data_path()                 # the data file, recommendations.json
    opendfx.rules_path()                # the KiCad 10 design-rules file, opendfx.kicad_dru

These are recommendations, not rules. Each one has a permanent ID, such as PCB-DFA-006,
and a permanent address, such as https://opendfx.org/PCB-DFA-006.
The data is licensed CC BY 4.0: credit "OpenDFX for Printed Circuit Boards by Chris Denney, https://opendfx.org".
The code and the KiCad rules file are licensed MIT.
"""
import json
from functools import lru_cache
from pathlib import Path

from ._version import __version__

__all__ = ["STAGES", "ATTRIBUTION", "recommendations", "get", "for_stage", "search", "data", "data_path", "rules_path", "__version__"]

HERE = Path(__file__).resolve().parent
STAGES = ("parts", "library", "placement", "routing", "outline", "release", "production")
ATTRIBUTION = "OpenDFX for Printed Circuit Boards by Chris Denney, https://opendfx.org"


def data_path():
    """The path of recommendations.json, the book's data file."""
    return HERE / "data" / "recommendations.json"


def rules_path():
    """The path of opendfx.kicad_dru, the KiCad 10 design-rules file."""
    return HERE / "data" / "opendfx.kicad_dru"


@lru_cache(maxsize=1)
def data():
    """The whole data file: the credit line, the citation, the license and the recommendations."""
    return json.loads(data_path().read_text(encoding="utf-8"))


def recommendations():
    """Every recommendation, in the book's order."""
    return list(data()["recommendations"])


def get(rec_id):
    """One recommendation by its ID, such as "PCB-DFA-006". Raises KeyError if there is none."""
    want = rec_id.strip().upper()
    for r in data()["recommendations"]:
        if r["id"] == want:
            return r
    raise KeyError(f"No recommendation {rec_id}")


def for_stage(stage):
    """Every recommendation for one design stage (see STAGES)."""
    if stage not in STAGES:
        raise ValueError(f"Unknown design stage {stage!r}. The stages are: {', '.join(STAGES)}")
    return [r for r in data()["recommendations"] if stage in r["design_stages"]]


def search(text):
    """Recommendations whose ID, title or text contains every word of `text`, ignoring case."""
    words = text.lower().split()
    keys = ("id", "title", "recommendation", "why", "typical_values", "what_goes_wrong", "applies_to")
    found = []
    for r in data()["recommendations"]:
        hay = " ".join(str(r.get(k) or "") for k in keys).lower()
        if all(w in hay for w in words):
            found.append(r)
    return found
