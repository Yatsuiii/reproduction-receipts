from pathlib import Path
Path("results/inter.csv").write_text("x\n%s\n" % (1/2))
