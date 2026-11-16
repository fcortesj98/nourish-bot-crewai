"""NourishBot web app entry point.

Run with ``python app.py`` and open http://127.0.0.1:5000 (port 5000 matches
the IBM Skills Network Cloud IDE "Web Application" button). ``demo`` is kept
at module level so Hugging Face Spaces can discover it.
"""

import logging

from nourishbot.settings import EXAMPLES_DIR, get_settings
from nourishbot.ui import build_demo

logging.basicConfig(level=logging.INFO)

demo = build_demo()

if __name__ == "__main__":
    settings = get_settings()
    demo.launch(
        server_name=settings.server_host,
        server_port=settings.server_port,
        allowed_paths=[str(EXAMPLES_DIR)],
    )
