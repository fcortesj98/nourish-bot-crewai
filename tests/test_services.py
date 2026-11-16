"""Service-layer tests with the watsonx.ai call mocked out (no network needed)."""

from nourishbot.services import food_ai
from nourishbot.settings import EXAMPLES_DIR


def test_filter_without_restriction_skips_model(monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("model should not be called")

    monkeypatch.setattr(food_ai.wx, "chat", fail)
    assert food_ai.filter_by_dietary_restrictions(["egg", "rice"], None) == ["egg", "rice"]


def test_filter_with_restriction_parses_reply(monkeypatch):
    captured = {}

    def fake_chat(model_id, content, max_tokens):
        captured["prompt"] = content[0]["text"]
        return "Rice, Spinach"

    monkeypatch.setattr(food_ai.wx, "chat", fake_chat)
    result = food_ai.filter_by_dietary_restrictions(["egg", "rice", "spinach"], "vegan")
    assert result == ["rice", "spinach"]
    assert "egg, rice, spinach" in captured["prompt"] and "vegan" in captured["prompt"]


def test_vision_calls_send_image(monkeypatch):
    sent = {}

    def fake_chat(model_id, content, max_tokens):
        sent["content"] = content
        return "tomato, basil"

    monkeypatch.setattr(food_ai.wx, "chat", fake_chat)
    assert food_ai.extract_ingredients(str(EXAMPLES_DIR / "food-1.jpg")) == "tomato, basil"
    kinds = [part["type"] for part in sent["content"]]
    assert kinds == ["text", "image_url"]
