import random
import math
from hashlib import sha256
import os

def is_prime(n, k=40):
    if n <= 1 or n == 4: return False
    if n <= 3: return True

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_large_prime(bits):
    while True:
        num = random.getrandbits(bits)
        num |= (1 << bits - 1) | 1
        if is_prime(num):
            return num

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    return x % m

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = extended_gcd(b % a, a)
    return (g, x - (b // a) * y, y)

def generate_keypair(bits=1024):
    p = generate_large_prime(bits // 2)
    q = generate_large_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    d = modinv(e, phi)
    return ((e, n), (d, n))

def pkcs1_pad(message, block_size):
    padding_len = block_size - len(message) - 3
    if padding_len < 8:
        raise ValueError("Message too long")

    padding = b''
    while len(padding) < padding_len:
        byte = os.urandom(1)
        if byte != b'\x00':
            padding += byte

    return b'\x00\x02' + padding + b'\x00' + message

def pkcs1_unpad(padded_message):
    if padded_message[0:2] != b'\x00\x02':
        raise ValueError("Invalid padding")
    padded_message = padded_message[2:]
    padding_end = padded_message.find(b'\x00')
    if padding_end == -1:
        raise ValueError("Invalid padding")
    return padded_message[padding_end + 1:]

def encrypt(message: bytes, pub_key):
    e, n = pub_key
    block_size = (n.bit_length() + 7) // 8
    padded = pkcs1_pad(message, block_size)
    m = int.from_bytes(padded, byteorder='big')
    c = pow(m, e, n)
    return c

def decrypt(ciphertext: int, priv_key):
    d, n = priv_key
    m = pow(ciphertext, d, n)
    m_bytes = m.to_bytes((n.bit_length() + 7) // 8, byteorder='big')
    return pkcs1_unpad(m_bytes)

if __name__ == "__main__":
    print("Generating RSA keypair...")
    public, private = generate_keypair(1024)

    msg = b"Complex RSA implementation"
    print(f"\nOriginal Message:\n{msg.decode()}")

    cipher = encrypt(msg, public)
    print(f"\nEncrypted Cipher:\n{cipher}")

    plain = decrypt(cipher, private)
    print(f"\nDecrypted Message:\n{plain.decode()}")
