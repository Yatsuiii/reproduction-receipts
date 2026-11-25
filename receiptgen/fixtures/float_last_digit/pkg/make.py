from pathlib import Path
Path("out").mkdir(exist_ok=True)
Path("out/table.csv").write_text("a,b\n%r,%r\n" % (0.1+0.2, 1/3))
