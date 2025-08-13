BITS = 256
MOD_MASK = (1 << BITS) - 1
START = (1 << BITS)  # == 2^256


# -------- 1) Odd-step reverse counter --------
class OddStepReverse:
    def __init__(self, start, step):
        assert step % 2 == 1, "step must be odd for full coverage"
        self.x = start & MOD_MASK
        self.step = step & MOD_MASK

    def prev(self):
        self.x = (self.x - self.step) & MOD_MASK
        return self.x

    def jump(self, count):
        """Jump `count` steps back in O(1)."""
        self.x = (self.x - self.step * count) & MOD_MASK
        return self.x


# -------- 2) LCG reverse --------
def modinv(a, mod):
    return pow(a, -1, mod)

class LCGReverse:
    def __init__(self, start, a, c):
        assert a % 4 == 1, "a must be 1 mod 4"
        assert c % 2 == 1, "c must be odd"
        self.x = start & MOD_MASK
        self.a = a & MOD_MASK
        self.c = c & MOD_MASK
        self.m = 1 << BITS
        self.a_inv = modinv(a, self.m)

    def prev(self):
        self.x = ((self.x - self.c) * self.a_inv) & MOD_MASK
        return self.x

    def jump(self, count):
        """Jump `count` steps back in O(log count) for 2^BITS modulus."""
        a = self.a_inv  # stepping backwards
        c = (-self.c * self.a_inv) & MOD_MASK
        m = 1 << BITS

        mul = 1
        add = 0
        k = count
        while k > 0:
            if k & 1:
                mul = (mul * a) % m
                add = (add * a + c) % m
            c = (c * (a + 1)) % m
            a = (a * a) % m
            k >>= 1

        self.x = (self.x * mul + add) % m
        return self.x



# -------- 3) PRP reverse counter --------
def feistel_encrypt(x, rounds=3):
    half = BITS // 2
    mask = (1 << half) - 1
    L = (x >> half) & mask
    R = x & mask
    for r in range(rounds):
        L, R = R, (L ^ ((R * (0x9E3779B97F4A7C15 + r)) & mask))
    return (L << half) | R

class PRPCounterReverse:
    def __init__(self, start):
        self.counter = start & MOD_MASK

    def prev(self):
        self.counter = (self.counter - 1) & MOD_MASK
        return feistel_encrypt(self.counter)

    def jump(self, count):
        """Jump `count` steps back instantly."""
        self.counter = (self.counter - count) & MOD_MASK
        return feistel_encrypt(self.counter)


# -------- DEMO --------
if __name__ == "__main__":
    print("OddStepReverse jump test:")
    odd_rev = OddStepReverse(START, 3)
    print(hex(odd_rev.jump()))  # jump 10 steps back
    print(hex(odd_rev.prev()))  # previous step
    print(hex(odd_rev.prev()))  # previous step


    # print("\nLCGReverse jump test:")
    # lcg_rev = LCGReverse(START, 5, 1)
    # print(hex(lcg_rev.jump(10)))  # jump 10 steps back

    # print("\nPRPCounterReverse jump test:")
    # prp_rev = PRPCounterReverse(START)
    # print(hex(prp_rev.jump(10)))  # jump 10 steps back
