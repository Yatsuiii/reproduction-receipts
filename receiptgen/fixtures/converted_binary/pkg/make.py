from pathlib import Path
Path("out").mkdir(exist_ok=True)
Path("out/x.bin").write_bytes(b"WRITER-v4.3\n0.5\n0.25\n")
