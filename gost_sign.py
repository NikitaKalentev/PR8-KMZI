# gost_sign.py
import random
from elliptic import EllipticCurve
from modular import modinv
from streebog import streebog256

def generate_keys(curve: EllipticCurve, q: int, P):
    """Возвращает (d, Q) – секретный и открытый ключи."""
    d = random.randrange(1, q)
    Q = curve.multiply(d, P)
    return d, Q

def sign_message(curve: EllipticCurve, q: int, P, d: int, message_hash: bytes):
    """Возвращает (r, s) – подпись для хэша сообщения."""
    e = int.from_bytes(message_hash, 'big') % q
    if e == 0:
        e = 1
    while True:
        k = random.randrange(1, q)
        C = curve.multiply(k, P)
        r = C[0] % q
        if r == 0:
            continue
        s = (r * d + k * e) % q
        if s == 0:
            continue
        return r, s

def verify_signature(curve: EllipticCurve, q: int, P, Q, message_hash: bytes, r: int, s: int) -> bool:
    """Проверяет подпись. Возвращает True, если подпись верна."""
    if not (0 < r < q and 0 < s < q):
        return False
    e = int.from_bytes(message_hash, 'big') % q
    if e == 0:
        e = 1
    v = modinv(e, q)
    z1 = (s * v) % q
    z2 = (-r * v) % q
    C = curve.add(curve.multiply(z1, P), curve.multiply(z2, Q))
    if C is None:
        return False
    R = C[0] % q
    return R == r
