#!/usr/bin/env python3

from PIL import Image
from matplotlib import pyplot
from numpy import asarray
import sys
import os


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def openImage(fileImage, message, min_message, max_message):

    # with Image.open(fileImage) as image:
    #     pixel = image.load()

    # image.show()
    # print(pixel[4, 4])
    # pixel[4, 4] = (0,255, 255)
    # print(pixel[4, 4])
    # image.show()


    img = Image.open(fileImage)
    # print(img)

    # convert image to numpy array
    data_image = asarray(img)
    # print(data_image.shape)

    # create Pillow image
    image_pillow = Image.fromarray(data_image)
    print(image_pillow.format)
    print(image_pillow.mode)
    print(image_pillow.size)

    # create pixel map
    pixels = image_pillow.load()

    # show original image
    # image_pillow.show()

    # iterate through pixels to try and change the color of a single pixel
    for column in range(image_pillow.size[0]):
        for row in range(image_pillow.size[1]):
            if pixels[column, row] != (255, 0, 0):
                pixels[0, 1] = (0, 255, 255)

    # show new image
    #image_pillow.show()
    image_pillow.save("output.bmp")
    # image_pillow.show()

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

    length = len(message)
    # print(length)

    # message minimum 1
    if length < 1:
        print("No message input")
        return False
    # copy of image to hide text in
    encoded = image_pillow.copy()
    width, height = image_pillow.size
    index = 0
    for row in range(height):
        for column in range(width):
            red, green, blue = image_pillow.getpixel((column, row))
            # print(red, green, blue)
            if row == 0 and column == 0 and index < length:
                asc = length
                print("asc = length: ", asc)
            elif index <= length:
                character = message[index - 1]
                print("character = message[index-1]: " + character)
                asc = ord(character)
                print("asc = ord(character):", asc)
            else:
                asc = red
                #print("asc=r: ", asc)
            encoded.putpixel((column, row), (asc, green, blue))
            index += 1
    return encoded


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # check for number of arguments
    if len(sys.argv) != 5:
        print("Usage: " + sys.argv[0] + "<dirname> <size>")
        sys.exit(1)

    # check that the first arg is a picture(i.e bmp)
    if not os.path.exists(sys.argv[1]):
        print(sys.argv[1] + " is not a file image")
        sys.exit(1)

    # given a single message save arg into variable
    words = sys.argv[2]
    #sanitize_words = map(lambda w: w.strip(".,;!?'\"").lower(), words)
    print("message is: " + words)

    # Minimum message length should be 1-32
    min_message = int(sys.argv[3])
    # To-Do validate that the min value is within that range

    # Maximum message length should be 1-64
    max_message = int(sys.argv[4])
    # To-Do validate that the max value is within that range

    # load images
    fileImage = sys.argv[1]
    image_encoded = openImage(fileImage, words, min_message, max_message)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
