from pathlib import Path
Path("out").mkdir(exist_ok=True)
Path("data/input.csv").write_text("v\n9\n")
Path("out/t.csv").write_text("9\n")
