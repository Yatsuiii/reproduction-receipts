"""Stub runtime for the failure-injection tests. No weights are read beyond the hash check, no model is loaded.

OFFLINE_STUB_MODE selects the behaviour:
  ok         deterministic scores from a keyword rule
  connect    tries socket.connect to 203.0.113.7:443 on the first item, swallows the error, carries on
  dns        tries socket.getaddrinfo("telemetry.example.com") on the first item, swallows the error, carries on
  flip:ID    like ok, but the given item's decision is inverted
  drift:X    like ok, but every YES logit is shifted by X"""
import hashlib
import os
import socket


class Runtime:
    def __init__(self, weights_dir: str):
        self.mode = os.environ.get("OFFLINE_STUB_MODE", "ok")
        self.calls = 0

    def info(self) -> dict:
        return {"runtime": "stub", "mode": self.mode}

    def score(self, system: str, user: str):
        self.calls += 1
        if self.calls == 1 and self.mode == "connect":
            try:
                socket.create_connection(("203.0.113.7", 443), timeout=1)
            except OSError:
                pass
        if self.calls == 1 and self.mode == "dns":
            try:
                socket.getaddrinfo("telemetry.example.com", 443)
            except OSError:
                pass
        text = user.split("Text: ", 1)[1].split("\n", 1)[0]
        ly = 1.0 if any(c.isdigit() for c in text) or "@" in text else 0.0
        ln = 0.5
        if self.mode.startswith("drift:"):
            ly += float(self.mode.split(":", 1)[1])
        if self.mode.startswith("flip:") and f"p{self.calls:02d}" == self.mode.split(":", 1)[1]:
            ly, ln = ln, ly
        return ly, ln, hashlib.sha256((system + user).encode()).hexdigest(), len(user.split())
