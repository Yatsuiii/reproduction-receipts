from pathlib import Path
Path("out").mkdir(exist_ok=True)
Path("out/t.txt").write_text("ATT estimate: 0.5\n")
