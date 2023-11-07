import cv2
import easyocr
import numpy as np



def remove_bubble_text(image):
    reader = easyocr.Reader(["en"])
    bubbles = reader.readtext(image)

    # image_temp = np.zeros_like(image)
    image_rect = np.copy(image)
    # image_inpaint = np.copy(image)

    # texts = []

    for bub in bubbles:
        # check confidence level of detected OCR text
        bottom_left = tuple(int(x) for x in tuple(bub[0][0]))
        top_right = tuple(int(x) for x in tuple(bub[0][2]))
        # texts.append((top_right, bottom_left))
        
        # draw rectangle around detected text and white out the text
        # image_rect = cv2.rectangle(image_rect, bottom_left, top_right, (0, 255, 0), 3)
        # image_temp = cv2.rectangle(image_temp, bottom_left, top_right, (255, 255, 255), -1)

        # mask = cv2.cvtColor(image_temp, cv2.COLOR_BGR2GRAY)
        # image_inpaint = cv2.inpaint(image_inpaint, mask, 3, cv2.INPAINT_TELEA)

        # draw rectangle around detected text
        image_rect = cv2.rectangle(image_rect, bottom_left, top_right, (255, 255, 255), -1)
    return image_rect


if __name__ == "__main__":
    image = cv2.imread("temp/panels_1.jpg")

    cleaned_image = remove_bubble_text(image)

    cv2.imshow("image", image)
    cv2.imshow("cleaned", cleaned_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
