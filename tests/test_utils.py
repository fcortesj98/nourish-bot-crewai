import base64

import pytest

from nourishbot.settings import EXAMPLES_DIR, Settings
from nourishbot.utils.images import guess_mime_type, image_to_data_uri, load_image_bytes, save_pil_image_to_temp
from nourishbot.utils.text import parse_comma_separated
from nourishbot.workflows import WorkflowType


def test_parse_comma_separated_cleans_items():
    assert parse_comma_separated(" Tomato, ,BASIL ,olive oil,") == ["tomato", "basil", "olive oil"]


def test_load_image_bytes_missing_file():
    with pytest.raises(FileNotFoundError):
        load_image_bytes("does/not/exist.jpg")


def test_image_to_data_uri_roundtrip():
    path = str(EXAMPLES_DIR / "food-1.jpg")
    uri = image_to_data_uri(path)
    assert uri.startswith("data:image/jpeg;base64,")
    assert base64.b64decode(uri.split(",", 1)[1]) == load_image_bytes(path)


def test_guess_mime_type():
    assert guess_mime_type("a.png") == "image/png"
    assert guess_mime_type("https://x.com/a.jpg?size=2") == "image/jpeg"
    assert guess_mime_type("no_extension") == "image/jpeg"


def test_save_pil_image_handles_rgba(tmp_path):
    from PIL import Image

    path = save_pil_image_to_temp(Image.new("RGBA", (8, 8), (255, 0, 0, 128)))
    with Image.open(path) as img:
        assert img.format == "JPEG"


def test_workflow_type_parse():
    assert WorkflowType.parse(" Recipe ") is WorkflowType.RECIPE
    assert WorkflowType.parse(WorkflowType.ANALYSIS) is WorkflowType.ANALYSIS
    with pytest.raises(ValueError):
        WorkflowType.parse("dessert")


def test_settings_env_overrides(monkeypatch):
    monkeypatch.setenv("WATSONX_PROJECT_ID", "my-project")
    monkeypatch.setenv("NOURISHBOT_PORT", "7860")
    monkeypatch.setenv("WATSONX_API_KEY", "")  # empty means unset
    s = Settings.from_env()
    assert s.watsonx_project_id == "my-project"
    assert s.server_port == 7860
    assert s.watsonx_api_key is None
