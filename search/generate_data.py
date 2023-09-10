import random
import secrets
import psycopg2
import concurrent.futures


def generate(start):
    conn = psycopg2.connect("dbname=bksearch_sample user=postgres")
    cur = conn.cursor()

    for i in range(start, start + 10 ** 4):
        phash = random.getrandbits(64)
        phash = format(phash, "0b")
        dhash = secrets.token_hex(8)
        q = "INSERT INTO bstrings (phash64, dhash16) VALUES ('{}', '{}');".format(phash, dhash)
        cur.execute(q)
    conn.commit()
    cur.close()
    conn.close()


out = [i for i in range(0, 10 ** 8, 10 ** 4)]

with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
    result = list(executor.map(generate, out))
