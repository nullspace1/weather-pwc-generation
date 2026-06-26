import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import uvicorn
import webview

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend" / "weather"
API_URL = "http://localhost:8000/docs"
UI_URL = "http://localhost:8001"


def _wait_for_url(
    url: str,
    timeout: float = 60.0,
    process: subprocess.Popen | None = None,
) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process is not None and process.poll() is not None:
            return False
        try:
            with urllib.request.urlopen(url, timeout=1):
                return True
        except (urllib.error.URLError, TimeoutError, OSError):
            time.sleep(0.25)
    return False


def _run_backend() -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT)
    os.environ.update(env)
    config = uvicorn.Config(
        "backend.main.app:app",
        log_level="info",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )
    server = uvicorn.Server(config)
    server.run()


def _terminate(process: subprocess.Popen | None) -> None:
    if process is None or process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


def _launch() -> None:
    backend_process = subprocess.Popen(
        [sys.executable, __file__, "--backend"],
        cwd=ROOT,
    )
    frontend_process = subprocess.Popen(
        "npm run dev",
        cwd=FRONTEND_DIR,
        shell=True,
    )

    try:
        if not _wait_for_url(API_URL):
            raise RuntimeError(f"Backend did not become ready at {API_URL}")
        if not _wait_for_url(UI_URL, process=frontend_process):
            if frontend_process.poll() is not None:
                raise RuntimeError(
                    f"Frontend process exited with code {frontend_process.returncode}"
                )
            raise RuntimeError(f"Frontend did not become ready at {UI_URL}")

        webview.create_window("Weather App", UI_URL, width=1200, height=800)
        webview.start()
    finally:
        _terminate(frontend_process)
        _terminate(backend_process)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--backend":
        _run_backend()
    else:
        _launch()
