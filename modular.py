# modular.py
def egcd(a, b):
    """Расширенный алгоритм Евклида: возвращает (gcd, x, y): a*x + b*y = gcd."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def modinv(a, n):
    """Возвращает x, такой что a*x ≡ 1 (mod n). n > 0, a и n взаимно просты."""
    g, x, _ = egcd(a, n)
    if g != 1:
        raise ValueError("Обратный элемент не существует")
    return x % n
