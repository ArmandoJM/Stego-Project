#!/usr/bin/env python3

from PIL import Image
from matplotlib import pyplot
from numpy import asarray
import sys
import os


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def openImage(fileImage):

    # with Image.open(fileImage) as image:
    #     pixel = image.load()

    # image.show()
    # print(pixel[4, 4])
    # pixel[4, 4] = (0,255, 255)
    # print(pixel[4, 4])
    # image.show()


    img = Image.open(fileImage)
    print(img)

    # convert image to numpy array
    data_image = asarray(img)
    print(data_image.shape)

    # create Pillow image
    image_pillow = Image.fromarray(data_image)
    print(image_pillow.format)
    print(image_pillow.mode)
    print(image_pillow.size)

    # create pixel map
    pixels = image_pillow.load()

    # show original image
    image_pillow.show()

    # iterate through pixels to try and change the color of a single pixel
    for column in range(image_pillow.size[0]):
        for row in range(image_pillow.size[1]):
            if pixels[column, row] != (255, 0, 0):
                pixels[0, 1] = (0, 255, 255)

    # show new image
    #image_pillow.show()
    image_pillow.save("output.bmp")
    image_pillow.show()

    # Approach 2
    #image_attempt = Image.open(fileImage, 'r')

    # extract the pixel values
    #pixel_values = list(image_attempt.getdata())

    # Fix list arrangement from tuples to list
    #pixel_values_arrange = [x for sets in pixel_values for x in sets]

    #print(pixel_values_arrange[1:3])
    #pixel_values_arrange[1:3] = (255, 0, 0)
    coordinate = x, y = 0, 0

    # show new image
    #image_pillow.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # check for number of arguments
    if len(sys.argv) != 4:
        print("Usage: " + sys.argv[0] + "<dirname> <size>")
        sys.exit(1)

    # check that the first arg is a picture(i.e bmp)
    if not os.path.exists(sys.argv[1]):
        print(sys.argv[1] + " is not a file image")
        sys.exit(1)

    # given a single message save arg into variable
    words = sys.argv[2]
    sanitize_words = map(lambda w: w.strip(".,;!?'\"").lower(), words)
    print(" ".join(sanitize_words))

    # Minimum message length should be 1-32
    min_message = int(sys.argv[3])
    # To-Do validate that the min value is within that range

    # Maximum message length should be 1-64
    max_message = int(sys.argv[4])
    # To-Do validate that the max value is within that range


    # load images
    fileImage = r'img/Img_02_24.bmp'
    openImage(fileImage)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
