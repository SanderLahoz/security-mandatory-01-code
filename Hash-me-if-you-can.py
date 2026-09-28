from hashlib import sha256


def custom_hash(m, b):
    """b should be either: 16, 24 or 32"""
    if not b in {16, 24, 32}:
        raise "Invalid value for b expected 16, 24 or 32"

    print(sha256(m).hexdigest()[:b//4])

def collision_search(m1, m2, b):
    if m1 == m2:
        raise "message 1 and message 2 should be distinct"

    return custom_hash(m1, b) == custom_hash(m2, b)


def main():
    test = b"hej"
    custom_hash(test, 32)



if __name__ == '__main__':
    main()