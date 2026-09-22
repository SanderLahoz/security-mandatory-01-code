
def find_secret_key(prime, generator, public_key):
    for private_key in range(prime - 1): # 0 <= x <= p - 2
        if pow(generator, private_key, prime) == public_key:
            return private_key


"""This decryption method is wrong should be looked at, before moving on"""
def decrypt_message(prime, encrypted_randomness, public_key, encrypted_message):
    for m in range(1, prime): # 1 <= m <= p - 1
        if pow(m * public_key, encrypted_randomness, prime) == encrypted_message:
            return m

def main():
    # Initiate constants:
    p, g, PK, c1, c2 = 29837, 42, 22690, 23447, 8372
    x, r = find_secret_key(p, g, PK), find_secret_key(p, g, c1)
    message = decrypt_message(p, r, PK, c2)
    print(f"Private key: {x}\nPlaintext: {message}")

if __name__ == '__main__':
    main()