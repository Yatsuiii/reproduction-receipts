from pathlib import Path
Path("out").mkdir(exist_ok=True)
Path("out/table.tex").write_text("Effect & 1.240 & (0.311) \\\\\nN & 445 & \\\\\n")
