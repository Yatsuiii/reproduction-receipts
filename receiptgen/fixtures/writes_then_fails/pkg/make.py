from pathlib import Path
Path("out").mkdir(exist_ok=True)
Path("out/t.csv").write_text("x\n1\n")
raise SystemExit(2)
