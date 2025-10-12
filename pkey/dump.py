from typing import Callable, Optional
import secrets


def heaps_permutations(seq):
    """
    Yield all permutations of seq using Heap's algorithm.
    Works in-place, uses O(n) memory.
    """
    seq = list(seq)
    n = len(seq)
    c = [0] * n
    yield ''.join(seq)

    i = 0
    while i < n:
        if c[i] < i:
            # swap depends on even/odd i
            if i % 2 == 0:
                seq[0], seq[i] = seq[i], seq[0]
            else:
                seq[c[i]], seq[i] = seq[i], seq[c[i]]
            yield ''.join(seq)
            c[i] += 1
            i = 0
        else:
            c[i] = 0
            i += 1


def _default_entropy(nbytes: int) -> bytes:
    return secrets.token_bytes(nbytes)

def generate_secure_bigint(
    bit_length: int = 256,
    *,
    allow_zero: bool = True,
    entropy_fn: Optional[Callable[[int], bytes]] = None
) -> int:

    if entropy_fn is None:
        entropy_fn = _default_entropy

    nbytes = (bit_length + 7) // 8  # number of full bytes needed
    top_bits = nbytes * 8 - bit_length  # number of unused high bits in the top byte

    # Rejection loop only used for allow_zero == False. For allow_zero==True there is
    # no bias because we are generating exactly bit_length bits and mapping to 0..2**bit_length-1.
    while True:
        raw = entropy_fn(nbytes)  # cryptographic randomness

        # mask away extra top bits so we produce exactly `bit_length` bits
        if top_bits:
            mask = (1 << (8 - top_bits)) - 1
            raw = bytes([raw[0] & mask]) + raw[1:]

        value = int.from_bytes(raw, "big")

        if 0 <= value < (1 << bit_length):
            if not allow_zero and value == 0:
                # very rare; re-sample
                continue
            return value
        continue



# Example quick test / usage
if __name__ == "__main__":
    
    # Example usage
    for state in heaps_permutations("862718293348820473429344482784628181556388621521298319395315527974912"):
        print(state)