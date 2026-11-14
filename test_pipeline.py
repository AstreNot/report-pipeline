import pytest
from pptx import Presentation

import pipeline


def test_refuses_to_run_without_explicit_dummy_flag(monkeypatch, tmp_path):
    monkeypatch.delenv("REPORT_DUMMY", raising=False)
    with pytest.raises(RuntimeError):
        pipeline.refresh(tmp_path / "c.json")


def test_deck_built_from_cache(monkeypatch, tmp_path):
    monkeypatch.setenv("REPORT_DUMMY", "1")
    cache = pipeline.refresh(tmp_path / "c.json")
    deck = Presentation(pipeline.build_deck(cache, tmp_path / "r.pptx"))
    assert len(deck.slides) == 2
    assert deck.slides[1].shapes[-1].has_chart
