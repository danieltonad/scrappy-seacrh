import random, itertools, threading
from mnemonic import Mnemonic

with open("key.txt", "r", errors='ignore') as file:
    keys = file.read().splitlines()
    
def generate_permutations(input_list):
    return itertools.permutations(input_list)

def is_valid_phrase(phrase: str, language='english') -> bool:
    mnemo = Mnemonic(language)
    return mnemo.check(phrase)

def unordered_equal(a: list, b: str):
    return set(a) == set(b)

def random_pick_phrase(_len: int = 12):
    random_items = random.sample(keys, _len)
    print(random_items)

        
for i in generate_permutations(['post', 'true', 'pigeon', 'fortune', 'wonder', 'rice', 'decade', 'gallery', 'mobile', 'interest', 'curious', 'grow']):
    print(i)