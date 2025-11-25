from __future__ import annotations

import functools
import sys
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest
from playwright.sync_api import APIRequestContext, Playwright

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.visualization import build_dashboard  # noqa: E402


@pytest.fixture(scope="session")
def project_root() -> Path:
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def dashboard_html(project_root: Path) -> Path:
    output = project_root / "dist" / "driver_gap_dashboard.html"
    build_dashboard(output_html=output, open_browser=False)
    return output


@pytest.fixture(scope="session")
def static_server(project_root: Path, dashboard_html: Path):
    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(project_root))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        yield base_url
    finally:
        server.shutdown()
        thread.join()


@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> APIRequestContext:
    request_context = playwright.request.new_context()
    try:
        yield request_context
    finally:
        request_context.dispose()
