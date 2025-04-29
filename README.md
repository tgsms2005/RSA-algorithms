# RSA-algorithms
The code implements the RSA cryptographic algorithm in Python without using any external cryptography libraries. RSA is an asymmetric encryption system that uses a pair of keys — a public key for encryption and a private key for decryption. This script not only covers encryption and decryption but also the complex internals like prime number generation, padding (PKCS#1 v1.5), and modular arithmetic operations.

RSA security depends on the difficulty of factoring large prime numbers. The code starts by defining a function is_prime() which uses the Miller-Rabin primality test, a probabilistic algorithm for checking whether a number is prime. The function generate_large_prime() repeatedly generates large odd numbers of the required bit length and tests them using Miller-Rabin until a prime is found. This ensures that the RSA keys are built upon two large, secure primes.

The generate_keypair() function generates the RSA public and private keys. It begins by generating two large primes p and q, then calculates n = p * q, and the totient phi = (p - 1)(q - 1). The public exponent e is usually set to 65537 for efficiency and security. The corresponding private exponent d is calculated using the modular inverse, which relies on the extended_gcd() function — a recursive implementation of the extended Euclidean algorithm. Finally, the public key (e, n) and private key (d, n) are returned.

Before encrypting, RSA requires padding to prevent security vulnerabilities. The pkcs1_pad() function applies PKCS#1 v1.5 padding, where random non-zero bytes are added between a fixed header (0x00 0x02) and the message. This ensures that the message length is appropriate for encryption. During decryption, the pkcs1_unpad() function checks the padding and extracts the original message from the decrypted padded block, raising errors if padding is invalid.

Encryption is handled by the encrypt() function, which pads the message, converts it to an integer, and performs modular exponentiation ciphertext = m^e mod n using Python’s built-in pow() function. Decryption is similarly implemented in the decrypt() function, where the ciphertext is exponentiated with the private exponent d and then unpadded to recover the original plaintext. All conversions between bytes and integers are handled using int.from_bytes() and int.to_bytes().

In the __main__ block, the code generates a 1024-bit RSA keypair, encrypts a simple message using the public key, and decrypts it with the private key. The result is printed at each step to show the original message, ciphertext, and recovered message. This part ties all components together into a working example of the RSA algorithm with realistic padding and security practices.


