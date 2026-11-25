from pathlib import Path
Path("out").mkdir(exist_ok=True)
Path("out/fresh.csv").write_text("2\n")
