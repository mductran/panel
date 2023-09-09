import cv2

FILLED_RATIO_LIMIT = 0.25
BLACK_THRESHOLD = 127


def find_border_left(image):
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = image.shape[0], image.shape[1]
    filled_limit = FILLED_RATIO_LIMIT * height

    # scan left border
    for i in range(width):
        filled_count = 0
        for j in range(height):
            if image[j][i] < BLACK_THRESHOLD:
                filled_count += 1

        if filled_count > filled_limit:
            return i

    return width - 1


def find_border_right(image):
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = image.shape[0], image.shape[1]
    filled_limit = FILLED_RATIO_LIMIT * height

    # scan left border
    for i in range(width - 1, -1, -1):
        filled_count = 0
        for j in range(height):
            if image[j][i] < BLACK_THRESHOLD:
                filled_count += 1

        if filled_count > filled_limit:
            return i

    return width - 1


def find_border_top(image):
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = image.shape[0], image.shape[1]
    filled_limit = FILLED_RATIO_LIMIT * width

    # scan left border
    for i in range(height):
        filled_count = 0
        for j in range(width):
            if image[i][j] < BLACK_THRESHOLD:
                filled_count += 1

        if filled_count > filled_limit:
            return i

    return height - 1


def find_border_bottom(image):
    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = image.shape[0], image.shape[1]
    filled_limit = FILLED_RATIO_LIMIT * width

    # scan left border
    for i in range(height - 1, -1, -1):
        filled_count = 0
        for j in range(width):
            if image[i][j] < BLACK_THRESHOLD:
                filled_count += 1

        if filled_count > filled_limit:
            return i

    return height - 1
