import random, itertools, threading
from mnemonic import Mnemonic
from database import check_seed_exist

with open("key.txt", "r", errors='ignore') as file:
    keys = file.read().splitlines()
    
def generate_permutations(input_list):
    return itertools.permutations(input_list)

def is_valid_phrase(phrase: str, language='english') -> bool:
    mnemo = Mnemonic(language)
    return mnemo.check(phrase)

def random_pick_phrase(_len: int = 12):
    random_items = random.sample(keys, _len)
    return random_items if is_valid_phrase(" ".join(random_items)) else random_pick_phrase(_len)

async def generate_seed():
    seed = random_pick_phrase()
    if is_valid_phrase(seed) and not await check_seed_exist(seed):
        return seed
    