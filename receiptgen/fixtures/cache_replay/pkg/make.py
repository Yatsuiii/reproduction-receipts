from pathlib import Path
Path("out").mkdir(exist_ok=True)
p=Path("out/scores.csv")
if p.exists():
    print("cached")
else:
    p.write_text("0.91\n")
