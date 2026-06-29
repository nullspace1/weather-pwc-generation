import os
from pathlib import Path
import subprocess

import uvicorn
import webview

from backend.app import ROOT
import threading

def _get_port() -> int:
    """Get a free port to run the FastAPI server."""
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]
    

   
def main(is_dev: bool = False):
    
    if is_dev:
        print("Running in development mode. Make sure the frontend development server is running on port 5173.")
        subprocess.Popen(["npm" , "run", "dev"], cwd=ROOT.parent / "frontend", shell=True)
    
    port = _get_port() if not is_dev else 8000

    server_thread = threading.Thread(target=lambda: uvicorn.run("backend.app:app", host="localhost", port=port, log_level="info"))
    server_thread.start()

    webview.create_window("Weather App", f"http://localhost:{port if not is_dev else 5173}", width=1200, height=800)
    webview.start()
    
if __name__ == "__main__":
    ## add dev argument to run the frontend development server
    import sys
    is_dev = len(sys.argv) > 1 and sys.argv[1] == "dev"
    main(is_dev)
    
