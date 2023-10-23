import random
import secrets
import psycopg2
import concurrent.futures


def generate(start):
    conn = psycopg2.connect("dbname=bksearch_sample user=postgres")
    cur = conn.cursor()

    for i in range(start, start + 10 ** 4):
        phash = secrets.token_hex(10)
        # phash = format(phash, "0b")
        # dhash = secrets.token_hex(16)
        q = "INSERT INTO bstrings20 (id, phash) VALUES ({}, '{}');".format(i, phash)
        cur.execute(q)
    conn.commit()
    cur.close()
    conn.close()


def generate_text(start):
    print(start)
    with open("hash", "a") as f:
        for i in range(start, start + 10 ** 3):
            dhash = secrets.token_hex(64)
            f.write(dhash + "\n")
    


out = [i for i in range(1, 10 ** 6, 10 ** 4 + 1)]

with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
    result = list(executor.map(generate, out))
