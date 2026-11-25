from pathlib import Path
Path("out/table.csv").write_text(Path("results/inter.csv").read_text())
