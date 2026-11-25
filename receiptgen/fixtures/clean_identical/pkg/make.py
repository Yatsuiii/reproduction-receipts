from pathlib import Path
Path("out").mkdir(exist_ok=True)
Path("out/table.csv").write_text("x,y\n1,0.5\n2,0.25\n")
