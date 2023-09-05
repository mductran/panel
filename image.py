import cv2
import numpy as np
from functools import reduce

from skimage.feature import canny
from skimage.morphology import dilation

from scipy import ndimage as ndi

import urllib.request


def ccl(image):
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(image, (5, 5), 0)

    _, thresh = cv2.threshold(blur, 235, 255, cv2.THRESH_BINARY)

    cv2.rectangle(thresh, (0, 0), tuple(image.shape[::-1]), (0, 255, 0), 10)

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(image=thresh, connectivity=4,
                                                                            ltype=cv2.CV_32S)

    # TODO: perform grouping on connected components
    # if more than half of a component’s convex hull overlaps with another component’s
    # the two components are considered to belong to the same panel, and therefore are merged together.

    ind = np.argsort(stats[:, 4], )[::-1][1]
    panel_block_mask = ((labels == ind) * 255).astype("uint8")

    cv2.rectangle(panel_block_mask, (0, 0), tuple(panel_block_mask.shape[::-1]), (255, 255, 255), 10)
    return panel_block_mask


def is_open_panels(image):
    # check if image is binarized
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(image, 235, 255, cv2.THRESH_BINARY)
    height, width = thresh.shape[0], thresh.shape[1]

    # check horizontal border
    i = 0
    phi_prime_top, phi_prime_bot = 0, 0
    max_x_top, min_x_top, max_x_bot, min_x_bot = 0, 0, 0, 0
    while i < width - 1:
        max_x_top = max(thresh[0][i] * i / 255, max_x_top)
        min_x_top = min(thresh[0][i] * i / 255, min_x_top)
        phi_prime_top += (image[0][i + 1] - image[0][i]) / 255

        max_x_bot = max(thresh[height - 1][i] * i / 255, max_x_bot)
        min_x_bot = min(thresh[height - 1][i] * i / 255, min_x_bot)
        phi_prime_bot += (image[height - 1][i + 1] - image[0][i]) / 255
        i += 1

    # TODO: close open boundaries
    if phi_prime_top > 10 and (max_x_top - min_x_top) > 0.7 * width:
        print("top border is open")
    else:
        print("top border is closed")

    if phi_prime_bot > 10 and (max_x_bot - min_x_bot) > 0.7 * width:
        print("bottom border is open")
    else:
        print("bottom border is closed")

    # check vertical borders
    i = 0
    phi_prime_left, phi_prime_right = 0, 0
    max_y_left, min_y_left, max_y_right, min_y_right = 0, 0, 0, 0
    while i < height - 1:
        max_y_left = max(thresh[i][0] * i / 255, max_y_left)
        min_y_left = min(thresh[i][0] * i / 255, min_y_left)
        phi_prime_left += (image[i + 1][0] - image[i][0]) / 255

        max_y_right = max(thresh[i][width - 1] * i / 255, max_y_right)
        min_y_right = min(thresh[i][width - 1] * i / 255, min_y_right)
        phi_prime_right += (image[i + 1][width - 1] - image[i][width - 1]) / 255
        i += 1

    if phi_prime_left > 10 and (max_y_left - min_y_left) > 0.7 * width:
        print("left border is open")
    else:
        print("left border is closed")

    if phi_prime_right > 10 and (max_y_right - min_y_right) > 0.7 * width:
        print("right border is open")
    else:
        print("right border is closed")


def panel_block_generation():
    return


def panel_block_splitting():
    return


def panel_shape_extraction():
    return


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
