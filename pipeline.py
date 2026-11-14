"""Two stages: refresh (source -> JSON cache) and build_deck (JSON cache -> PPTX). Synthetic source only."""
import json
import os
import random
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches

HERE = Path(__file__).parent
REGIONS = ["North", "South", "East", "West"]


def refresh(cache=HERE / "cache" / "report.json"):
    # Guard: never fall back to fake data silently; the dummy source must be asked for.
    if os.environ.get("REPORT_DUMMY") != "1":
        raise RuntimeError("no real source configured; set REPORT_DUMMY=1 to use synthetic data")
    rng = random.Random(1)
    data = {"title": "Daily Sales Report (synthetic)",
            "regions": [{"name": r, "actual": rng.randint(80, 140), "target": 100} for r in REGIONS]}
    cache.parent.mkdir(exist_ok=True)
    cache.write_text(json.dumps(data))
    return cache


def build_deck(cache=HERE / "cache" / "report.json", out=HERE / "output" / "report.pptx"):
    data = json.loads(cache.read_text())
    prs = Presentation()
    s = prs.slides.add_slide(prs.slide_layouts[0])
    s.shapes.title.text = data["title"]
    s.placeholders[1].text = "Generated from a JSON cache"

    s = prs.slides.add_slide(prs.slide_layouts[5])
    s.shapes.title.text = "Actual vs target by region"
    cd = CategoryChartData()
    cd.categories = [r["name"] for r in data["regions"]]
    cd.add_series("Actual", [r["actual"] for r in data["regions"]])
    cd.add_series("Target", [r["target"] for r in data["regions"]])
    s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.7), Inches(1.7), Inches(8.6), Inches(5), cd)
    out.parent.mkdir(exist_ok=True)
    prs.save(out)
    return out


if __name__ == "__main__":
    print(build_deck(refresh()))
