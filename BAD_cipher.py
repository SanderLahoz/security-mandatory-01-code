"""Public specification of the deliberately insecure cipher in Exercise 3.

Python 3.10+. Blocks and both keys are exactly 16 bytes. No padding or mode
of operation is used: each challenge is one independent block.
"""

import json

BLOCK_BYTES = 16
MASK = (1 << 128) - 1


def rotate_left_13(block: bytes) -> bytes:
    if len(block) != BLOCK_BYTES:
        raise ValueError("Expected exactly 16 bytes")
    value = int.from_bytes(block, "big")
    return (((value << 13) & MASK) | (value >> 115)).to_bytes(16, "big")


def xor(left: bytes, right: bytes) -> bytes:
    if len(left) != BLOCK_BYTES or len(right) != BLOCK_BYTES:
        raise ValueError("Expected exactly 16 bytes per operand")
    return bytes(a ^ b for a, b in zip(left, right))


def encrypt(plaintext: bytes, key1: bytes, key2: bytes) -> bytes:
    return xor(rotate_left_13(xor(plaintext, key1)), key2)


def rotate_right_13(block: bytes) -> bytes:
    if len(block) != BLOCK_BYTES:
        raise ValueError("Expected exactly 16 bytes")
    value = int.from_bytes(block, "big")
    return ((value >> 13) | ((value << 115) & MASK)).to_bytes(16, "big")

def decrypt(ciphertext: bytes, key1: bytes, key2: bytes) -> bytes:
    return xor(rotate_right_13(xor(ciphertext, key2)), key1)


if __name__ == "__main__":
    # Public test vector. These are NOT the challenge keys.
    p = bytes(16)
    k1 = bytes.fromhex("00000000000000000000000000000001")
    k2 = bytes(16)
    expected = "00000000000000000000000000002000"
    assert encrypt(p, k1, k2).hex() == expected
    print("Public test vector passed:", expected)

    # Load JSON challenge
    with open("cipher_challenge.json", "r") as f:
        data = json.load(f)

    known_p = bytes.fromhex(data["known_plaintext_hex"])
    known_c = bytes.fromhex(data["known_ciphertext_hex"])

    # Mathematical Shortcut: Assume Key1 is 0, solve for Key2 (the Master Key)
    derived_k1 = bytes(16)
    derived_k2 = xor(known_c, rotate_left_13(known_p))

    # Process challenges
    for challenge in data["challenges"]:
        c_bytes = bytes.fromhex(challenge["ciphertext_hex"])
        p_bytes = decrypt(c_bytes, derived_k1, derived_k2)

        print(f"ID: {challenge['id']}")
        print(f"  Hex:   {p_bytes.hex()}")
        print(f"  ASCII: '{p_bytes.decode('ascii')}'")
