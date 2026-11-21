"""Ed25519 (RFC 8032), pure Python, so the package has no dependencies.

Uses the `cryptography` package instead when it is installed: same keys, same signatures, faster, and constant-time. The
pure-Python path is NOT constant-time. It is fine for verifying receipts anywhere and for signing on a machine where timing
side channels are not in the threat model; prefer `cryptography` for signing in production. Checked against the RFC 8032
test vectors in tests/test_ed25519.py, and against `cryptography` when both are present.
"""
from __future__ import annotations

import hashlib
import os

try:  # optional fast path; AGENT_RECEIPTS_PURE=1 forces the pure-Python path (used in CI to test both)
    if os.environ.get("AGENT_RECEIPTS_PURE"):
        raise ImportError("pure path forced")
    from cryptography.exceptions import InvalidSignature as _InvalidSignature
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey as _Priv
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey as _Pub
    from cryptography.hazmat.primitives import serialization as _ser
    HAVE_CRYPTOGRAPHY = True
except Exception:  # pragma: no cover - depends on environment
    HAVE_CRYPTOGRAPHY = False

_p = 2 ** 255 - 19
_L = 2 ** 252 + 27742317777372353535851937790883648493
_d = -121665 * pow(121666, _p - 2, _p) % _p
_I = pow(2, (_p - 1) // 4, _p)


def _H(m: bytes) -> bytes:
    return hashlib.sha512(m).digest()


def _xrecover(y: int, sign: int):
    xx = (y * y - 1) * pow(_d * y * y + 1, _p - 2, _p) % _p
    x = pow(xx, (_p + 3) // 8, _p)
    if (x * x - xx) % _p:
        x = x * _I % _p
    if (x * x - xx) % _p:
        return None
    if x == 0 and sign:
        return None
    if x & 1 != sign:
        x = _p - x
    return x


_By = 4 * pow(5, _p - 2, _p) % _p
_Bx = _xrecover(_By, 0)
_B = (_Bx, _By, 1, _Bx * _By % _p)   # extended coordinates (X, Y, Z, T)
_ZERO = (0, 1, 1, 0)


def _add(P, Q):
    x1, y1, z1, t1 = P
    x2, y2, z2, t2 = Q
    a = (y1 - x1) * (y2 - x2) % _p
    b = (y1 + x1) * (y2 + x2) % _p
    c = 2 * t1 * t2 * _d % _p
    dd = 2 * z1 * z2 % _p
    e, f, g, h = b - a, dd - c, dd + c, b + a
    return (e * f % _p, g * h % _p, f * g % _p, e * h % _p)


def _mul(s: int, P):
    Q = _ZERO
    while s:
        if s & 1:
            Q = _add(Q, P)
        P = _add(P, P)
        s >>= 1
    return Q


def _encode(P) -> bytes:
    x, y, z, _ = P
    zi = pow(z, _p - 2, _p)
    x, y = x * zi % _p, y * zi % _p
    return (y | ((x & 1) << 255)).to_bytes(32, "little")


def _decode(b: bytes):
    if len(b) != 32:
        return None
    n = int.from_bytes(b, "little")
    y, sign = n & ((1 << 255) - 1), n >> 255
    if y >= _p:
        return None
    x = _xrecover(y, sign)
    if x is None:
        return None
    return (x, y, 1, x * y % _p)


def _eq(P, Q) -> bool:
    return (P[0] * Q[2] - Q[0] * P[2]) % _p == 0 and (P[1] * Q[2] - Q[1] * P[2]) % _p == 0


def _expand(seed: bytes):
    h = _H(seed)
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    return a, h[32:]


def public_key(seed: bytes, *, pure: bool = False) -> bytes:
    if len(seed) != 32:
        raise ValueError("Ed25519 seed must be 32 bytes")
    if HAVE_CRYPTOGRAPHY and not pure:
        return _Priv.from_private_bytes(seed).public_key().public_bytes(_ser.Encoding.Raw, _ser.PublicFormat.Raw)
    a, _ = _expand(seed)
    return _encode(_mul(a, _B))


def sign(seed: bytes, msg: bytes, *, pure: bool = False) -> bytes:
    if HAVE_CRYPTOGRAPHY and not pure:
        return _Priv.from_private_bytes(seed).sign(msg)
    a, prefix = _expand(seed)
    A = _encode(_mul(a, _B))
    r = int.from_bytes(_H(prefix + msg), "little") % _L
    R = _encode(_mul(r, _B))
    k = int.from_bytes(_H(R + A + msg), "little") % _L
    S = (r + k * a) % _L
    return R + S.to_bytes(32, "little")


def verify(pub: bytes, msg: bytes, sig: bytes, *, pure: bool = False) -> bool:
    if len(sig) != 64 or len(pub) != 32:
        return False
    if HAVE_CRYPTOGRAPHY and not pure:
        try:
            _Pub.from_public_bytes(pub).verify(sig, msg)
            return True
        except (_InvalidSignature, ValueError):
            return False
    A = _decode(pub)
    R = _decode(sig[:32])
    if A is None or R is None:
        return False
    S = int.from_bytes(sig[32:], "little")
    if S >= _L:
        return False
    k = int.from_bytes(_H(sig[:32] + pub + msg), "little") % _L
    return _eq(_mul(S, _B), _add(R, _mul(k, A)))


# ---- Ed25519ph (RFC 8032 section 5.1, phflag=1, empty context). Pure Python only: `cryptography` does not offer it.
# Sigstore's Rekor accepts Ed25519 keys in hashedrekord entries only with Ed25519ph over a SHA-512 prehash.

_DOM2_PH = b"SigEd25519 no Ed25519 collisions" + bytes([1, 0])


def sign_ph(seed: bytes, msg: bytes) -> bytes:
    ph = hashlib.sha512(msg).digest()
    a, prefix = _expand(seed)
    A = _encode(_mul(a, _B))
    r = int.from_bytes(_H(_DOM2_PH + prefix + ph), "little") % _L
    R = _encode(_mul(r, _B))
    k = int.from_bytes(_H(_DOM2_PH + R + A + ph), "little") % _L
    S = (r + k * a) % _L
    return R + S.to_bytes(32, "little")


def verify_ph(pub: bytes, msg: bytes, sig: bytes) -> bool:
    if len(sig) != 64 or len(pub) != 32:
        return False
    ph = hashlib.sha512(msg).digest()
    A, R = _decode(pub), _decode(sig[:32])
    if A is None or R is None:
        return False
    S = int.from_bytes(sig[32:], "little")
    if S >= _L:
        return False
    k = int.from_bytes(_H(_DOM2_PH + sig[:32] + pub + ph), "little") % _L
    return _eq(_mul(S, _B), _add(R, _mul(k, A)))
