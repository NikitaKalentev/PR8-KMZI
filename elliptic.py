# elliptic.py
from modular import modinv

class EllipticCurve:
    def __init__(self, p: int, a: int, b: int):
        self.p = p
        self.a = a
        self.b = b

    def add(self, P, Q):
        """
        Сложение двух точек на кривой.
        P, Q – кортежи (x, y) или None (бесконечно удалённая точка).
        """
        if P is None:
            return Q
        if Q is None:
            return P
        x1, y1 = P
        x2, y2 = Q
        # P = -Q
        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None
        # Удвоение
        if x1 == x2 and y1 == y2:
            lam = (3 * x1 * x1 + self.a) * modinv(2 * y1, self.p) % self.p
        else:
            lam = (y2 - y1) * modinv((x2 - x1) % self.p, self.p) % self.p
        x3 = (lam * lam - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p
        return (x3, y3)

    def multiply(self, k: int, P):
        """Умножение точки P на скаляр k (алгоритм double-and-add)."""
        result = None
        addend = P
        while k:
            if k & 1:
                result = self.add(result, addend)
            addend = self.add(addend, addend)
            k >>= 1
        return result
