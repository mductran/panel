import cv2
import numpy as np

from functools import reduce


# https://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html
def dhash(image, width=8, height=8):
    resized = cv2.resize(image, (width, height))
    resized = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    res = []
    for i in range(height):
        # ignore 4 corners
        if i == 0 or i == height - 1:
            for j in range(1, width - 2):
                res.append(resized[i][j] < resized[i][j + 1])
        else:
            for j in range(width - 1):
                res.append(resized[i][j] < resized[i][j + 1])

    return reduce(lambda x, y: str(int(x)) + str(int(y)), res)


def phash(image, width=32, height=32):
    resized = cv2.resize(image, (width, height))
    resized = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    resized = resized.astype(np.float32)

    dct_block = cv2.dct(resized)
    dct_block = dct_block[:8, :8]
    dct_average = (dct_block.mean() * dct_block.size - dct_block[0, 0]) / (dct_block.size - 1)
    dct_block[dct_block < dct_average] = 0.0
    dct_block[dct_block != 0] = 1.0

    dct_block = dct_block.astype(np.uint8).flatten().tolist()
    return reduce(lambda x, y: str(x) + str(y), dct_block)


def hamming(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))


def generate_hash(image):
    im_dhash = dhash(image)
    im_phash = phash(image)
    return im_phash, im_dhash
