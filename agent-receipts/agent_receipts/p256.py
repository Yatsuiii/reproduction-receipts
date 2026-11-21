"""ECDSA P-256 with SHA-256, pure Python. Used to check a transparency log's signatures offline (Rekor signs with P-256).

Verification is the part that matters and runs on public data. Signing exists only for the local log stand-in in the tests;
it uses random nonces from `secrets` and is not constant-time, so do not use it to protect anything."""
from __future__ import annotations

import base64
import hashlib
import secrets

P = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
A = P - 3
B = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
N = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
G = (0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
     0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
_SPKI_PREFIX = bytes.fromhex("3059301306072a8648ce3d020106082a8648ce3d030107034200")


def _add(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    (x1, y1), (x2, y2) = p1, p2
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    if p1 == p2:
        lam = (3 * x1 * x1 + A) * pow(2 * y1, P - 2, P) % P
    else:
        lam = (y2 - y1) * pow(x2 - x1, P - 2, P) % P
    x3 = (lam * lam - x1 - x2) % P
    return (x3, (lam * (x1 - x3) - y1) % P)


def _mul(k, pt):
    out = None
    while k:
        if k & 1:
            out = _add(out, pt)
        pt = _add(pt, pt)
        k >>= 1
    return out


def _on_curve(pt) -> bool:
    x, y = pt
    return (y * y - (x * x * x + A * x + B)) % P == 0


def der_from_pem(pem: bytes) -> bytes:
    lines = [ln.strip() for ln in pem.decode("ascii").strip().splitlines()]
    return base64.b64decode("".join(ln for ln in lines if ln and not ln.startswith("-----")))


def pem_from_der(der: bytes) -> bytes:
    b64 = base64.b64encode(der).decode()
    body = "\n".join(b64[i:i + 64] for i in range(0, len(b64), 64))
    return f"-----BEGIN PUBLIC KEY-----\n{body}\n-----END PUBLIC KEY-----\n".encode()


def point_from_der(der: bytes):
    if not der.startswith(_SPKI_PREFIX) or len(der) != len(_SPKI_PREFIX) + 65 or der[len(_SPKI_PREFIX)] != 4:
        raise ValueError("not an uncompressed P-256 SubjectPublicKeyInfo")
    raw = der[len(_SPKI_PREFIX) + 1:]
    pt = (int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big"))
    if not _on_curve(pt):
        raise ValueError("point is not on P-256")
    return pt


def _der_int(n: int) -> bytes:
    b = n.to_bytes((n.bit_length() + 8) // 8 or 1, "big")
    return b"\x02" + bytes([len(b)]) + b


def _parse_der_sig(sig: bytes):
    if len(sig) < 8 or sig[0] != 0x30 or sig[1] != len(sig) - 2:
        raise ValueError("bad DER signature")
    i, out = 2, []
    for _ in range(2):
        if sig[i] != 0x02:
            raise ValueError("bad DER integer")
        ln = sig[i + 1]
        out.append(int.from_bytes(sig[i + 2:i + 2 + ln], "big"))
        i += 2 + ln
    if i != len(sig):
        raise ValueError("trailing bytes in DER signature")
    return out


def verify(pub_pem: bytes, msg: bytes, der_sig: bytes) -> bool:
    try:
        Q = point_from_der(der_from_pem(pub_pem))
        r, s = _parse_der_sig(der_sig)
    except (ValueError, IndexError):
        return False
    if not (1 <= r < N and 1 <= s < N):
        return False
    e = int.from_bytes(hashlib.sha256(msg).digest(), "big")
    w = pow(s, N - 2, N)
    pt = _add(_mul(e * w % N, G), _mul(r * w % N, Q))
    return pt is not None and pt[0] % N == r


def generate():
    d = secrets.randbelow(N - 1) + 1
    x, y = _mul(d, G)
    return d, pem_from_der(_SPKI_PREFIX + b"\x04" + x.to_bytes(32, "big") + y.to_bytes(32, "big"))


def sign(d: int, msg: bytes) -> bytes:
    e = int.from_bytes(hashlib.sha256(msg).digest(), "big")
    while True:
        k = secrets.randbelow(N - 1) + 1
        r = _mul(k, G)[0] % N
        s = pow(k, N - 2, N) * (e + r * d) % N
        if r and s:
            body = _der_int(r) + _der_int(s)
            return b"\x30" + bytes([len(body)]) + body
