import cv2
import numpy as np
from functools import reduce

from skimage.feature import canny
from skimage.morphology import dilation

from scipy import ndimage as ndi

import urllib.request


def extract_panels(link="", path=""):
    if link != "":
        request = urllib.request.urlopen(link)
        arr = np.asarray(bytearray(request.read()), dtype=np.uint8)
        image = cv2.imdecode(arr, -1)
    else:
        image = cv2.imread(path)

    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = canny(grayscale)
    edges = edges.astype(np.uint8) * 255

    thick_edges = dilation(edges)

    segmentation = ndi.binary_fill_holes(thick_edges)
    segmentation = segmentation.astype(np.uint8) * 255

    _, thresh = cv2.threshold(segmentation, 200, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(
        segmentation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    hull_list = []
    for contour in contours:
        if cv2.contourArea(contour) > 1500:
            hull = cv2.convexHull(contour)
            hull_list.append(hull)

    panels = []
    for index, hull in enumerate(hull_list):
        mask = np.zeros_like(image)
        cv2.drawContours(mask, [hull], -1, (0, 255, 0), 3)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        mask = ndi.binary_fill_holes(mask)
        mask = mask.astype(np.uint8) * 255
        result = cv2.bitwise_and(image, image, mask=mask)
        x, y, w, h = cv2.boundingRect(hull)
        result = result[y:y + h, x:x + w]
        # cv2.imwrite('temp/panels_{}.jpg'.format(index), result)
        panels.append(result)
    return panels


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
