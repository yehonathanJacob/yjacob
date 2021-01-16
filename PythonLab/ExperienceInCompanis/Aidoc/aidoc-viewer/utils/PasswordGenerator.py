import random

'''
Simple password generator
'''
class PasswordGenerator:
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    passlen = 16

    @classmethod
    def generate(cls):
        return "".join(random.sample(cls.s, cls.passlen))


if __name__ == "__main__":
    print(PasswordGenerator.generate())
    print(PasswordGenerator.generate())
    print(PasswordGenerator.generate())
    print(PasswordGenerator.generate())
