from pathlib import Path
import runpy

if __name__ == "__main__":
    root_main = Path(__file__).resolve().parent.parent / "main.py"
    runpy.run_path(str(root_main), run_name="__main__")
