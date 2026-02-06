from whales_crawl import play_in, random
import sqlite3

DB_PATH = r"D:\9ja\general.db"


def pull_data_from_db(table: str) -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    conn.close()
    return rows


def pull_big_int_from_seed(_seed: str) -> int:
    random.seed(_seed)
    return random.getrandbits(256)


def main():
    data =  pull_data_from_db("pussios")
    total = len(data)
    for i, row in enumerate(data):
        _seed = " ".join(map(str, row))
        big_int = pull_big_int_from_seed(_seed)
        play_in(big_int)
        for item in row:
            _seed = str(item).strip()
            if not _seed:
                continue
            big_int = pull_big_int_from_seed(_seed)
            play_in(big_int)
        
        print(f"Progress {i+1:,} of {total:,}", end="\r")

if __name__ == "__main__":
    # while True: 
    main()