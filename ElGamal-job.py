

"""Brute force attack (Exhaustive search)"""
def find_secret_key(prime_modulus, generator, public_key):
    """
    Brute force all combinations for the private key in range:
    (0 <= private_key <= prime_modulus - 2). Using modular exponentiation
    and this formula: generator^private_key mod prime_modulus = public_key
    :return: private_key
    """
    for private_key in range(prime_modulus - 1):
        if pow(generator, private_key, prime_modulus) == public_key:
            return private_key

def decrypt_message(prime_modulus, ephemeral_randomness, public_key, cipher_text2):
    """
    Compute the shared secret and brute force the message by looping through
    all possible messages returning the message where (m * shared secret)
    modulus the large prime number is equal to the second intercepted cipher_text
    :return: message
    """
    shared_secret = pow(public_key, ephemeral_randomness, prime_modulus)
    for m in range(prime_modulus):
        if (m * shared_secret) % prime_modulus == cipher_text2:
            return m

def verify_result(prime_modulus, secret_key, generator, public_key, message, ephemeral_randomness, cipher_text2):
    # the secret key satisfies the public key equation
    assert pow(generator, secret_key, prime_modulus) == public_key

    # the message is in the valid range
    assert 1 <= message <= prime_modulus - 1

    # simulating the encryption produces the same cipher_text
    assert (message * pow(public_key, ephemeral_randomness, prime_modulus)) % prime_modulus == cipher_text2

    print("Verification successful")

"""Byzantine network: Ciphertext Malleability attack"""
def modify_ciphertext(prime_modulus, cipher_text1, cipher_text2, message, message_target):
    """:return: (c1, c2') that decrypts to message_target, using no secret values."""
    factor = (message_target * pow(message, -1, prime_modulus)) % prime_modulus
    return cipher_text1, (factor * cipher_text2) % prime_modulus

def main():
    # Initiate constants:
    _prime_modulus = 29837
    _generator = 42
    _public_key = 22690
    _cipher_text1 = 23447
    _cipher_text2 = 8372

    # Brute force the secret key and encryption randomness
    _private_key = find_secret_key(_prime_modulus, _generator, _public_key)
    _ephemeral_randomness = find_secret_key(_prime_modulus, _generator, _cipher_text1)

    # Decrypt the message using the recovered variables above
    _message = decrypt_message(_prime_modulus, _ephemeral_randomness, _public_key, _cipher_text2)

    verify_result(
        _prime_modulus,
        _private_key,
        _generator,
        _public_key,
        _message,
        _ephemeral_randomness,
        _cipher_text2
    )

    print(f"Private key: {_private_key}\nPlaintext: {_message}")


    _message_target = 20000
    (_, _cipher_text2_new) = modify_ciphertext(_prime_modulus, _cipher_text1, _cipher_text2, _message, _message_target)


if __name__ == '__main__':
    main()