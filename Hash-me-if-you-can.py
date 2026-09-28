import os
from hashlib import sha256


def custom_hash(m, b):
    """b should be either: 16, 24 or 32"""
    if not b in {16, 24, 32}:
        raise ValueError("Invalid value for b expected 16, 24 or 32")

    return sha256(m).hexdigest()[:b//4]

def collision_search(b):

    hash_to_message_dict = {}

    while True:
        random_message = os.urandom(8)
        hashed_message = custom_hash(random_message, b)

        if hashed_message in hash_to_message_dict:
            collided_message = hash_to_message_dict[hashed_message]

            # Make sure that the collided messages actually are different
            if random_message != hashed_message:
                return collided_message, random_message, hashed_message

        else:
            hash_to_message_dict[hashed_message] = random_message


def main():
    for b in (16, 24, 32):
        m1, m2, h = collision_search(b)
        print(f"Collision found for b = {b}")
        print(f"Message 1: {m1.hex()}, Message 2: {m2.hex()}, Shared hash: {h}")


if __name__ == '__main__':
    main()