# main.py
import os
from elliptic import EllipticCurve
from gost_sign import generate_keys, sign_message, verify_signature
from streebog import streebog256

# Параметры схемы (тестовые, из примера к ГОСТ Р 34.10-2012)
p = 97
a = 9
b = 3
q = 47
P = (-8 % p, 1)  # (-8, 1) по модулю 97 -> (89, 1)
curve = EllipticCurve(p, a, b)

def write_private_key(filename, d):
    with open(filename, 'w') as f:
        f.write(str(d))

def read_private_key(filename):
    with open(filename, 'r') as f:
        return int(f.readline().strip())

def write_public_key(filename, Q):
    with open(filename, 'w') as f:
        f.write(f"{Q[0]}\n{Q[1]}")

def read_public_key(filename):
    with open(filename, 'r') as f:
        x = int(f.readline().strip())
        y = int(f.readline().strip())
        return (x, y)

def write_signature(filename, r, s):
    with open(filename, 'w') as f:
        f.write(f"{r}\n{s}")

def read_signature(filename):
    with open(filename, 'r') as f:
        r = int(f.readline().strip())
        s = int(f.readline().strip())
        return r, s

def main():
    while True:
        print("\n" + "="*50)
        print("ГОСТ Р 34.10-2012 – Электронная подпись")
        print("1. Сгенерировать ключевую пару")
        print("2. Подписать файл")
        print("3. Проверить подпись")
        print("4. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            d, Q = generate_keys(curve, q, P)
            write_private_key("private.key", d)
            write_public_key("public.key", Q)
            print(f"Ключи сохранены:\n  private.key: d = {d}\n  public.key: Q = {Q}")
        elif choice == '2':
            msg_file = input("Путь к файлу для подписи: ")
            if not os.path.exists(msg_file):
                print("Файл не найден")
                continue
            key_file = input("Путь к файлу с закрытым ключом (private.key): ")
            if not os.path.exists(key_file):
                print("Файл ключа не найден")
                continue
            with open(msg_file, 'rb') as f:
                data = f.read()
            msg_hash = streebog256(data)   # наша собственная хэш-функция
            d = read_private_key(key_file)
            r, s = sign_message(curve, q, P, d, msg_hash)
            sig_file = input("Имя файла для сохранения подписи: ")
            write_signature(sig_file, r, s)
            print(f"Подпись (r={r}, s={s}) сохранена в {sig_file}")
        elif choice == '3':
            msg_file = input("Путь к файлу сообщения: ")
            sig_file = input("Путь к файлу подписи: ")
            pub_file = input("Путь к файлу с открытым ключом (public.key): ")
            if not (os.path.exists(msg_file) and os.path.exists(sig_file) and os.path.exists(pub_file)):
                print("Один из файлов не найден")
                continue
            with open(msg_file, 'rb') as f:
                data = f.read()
            msg_hash = streebog256(data)
            r, s = read_signature(sig_file)
            Q = read_public_key(pub_file)
            valid = verify_signature(curve, q, P, Q, msg_hash, r, s)
            print("Результат проверки:", "ПОДПИСЬ ВЕРНА" if valid else "ПОДПИСЬ НЕВЕРНА")
        elif choice == '4':
            break
        else:
            print("Неверный ввод")

if __name__ == "__main__":
    main()
