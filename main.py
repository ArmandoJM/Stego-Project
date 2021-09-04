#!/usr/bin/env python3
import imageio.core
from PIL import Image
import base64
import bitarray
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
    img.save("lsb_file.bmp")

    im = Image.open("lsb_file.bmp")
    width, height = im.size
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

    # Converts the message into an array of bits
    bits_array = bitarray.bitarray()
    bits_array.frombytes(message.encode('utf-8'))
    bit_array = [int(i) for i in bits_array]
    print("bit array: ", bit_array)

    # iterate through pixels to try and change the color of a single pixel
    i = 0
    for column in range(image_pillow.size[0]):
        red, green, blue = pixels[column, 0]
        print("Pixel : [%d,%d]" % (1, 0)) #(column, 0)
        print("\tBefore : (%d,%d,%d)" % (red, green, blue))

        # Default values for bits
        new_bit_red_pixel = 0
        new_bit_green_pixel = 255
        new_bit_blue_pixel = 255
        for row in range(image_pillow.size[1]):
            # check to see if the pixel it's red if it isn't then change to cyan
            if pixels[column, row] != (255, 0, 0):
                pixels[0, 1] = (0, 255, 255)

        pixels[column, 0] = (new_bit_red_pixel, new_bit_green_pixel, new_bit_blue_pixel)
        print("\tAfter  : (%d, %d, %d)" % (new_bit_red_pixel, new_bit_green_pixel, new_bit_blue_pixel))

    img.save('lsb_file.bmp')

    # show new image
    # image_pillow.show()
    image_pillow.save("output.bmp")
    # image_pillow.show()

    # Approach 2
    # image_attempt = Image.open(fileImage, 'r')

    # extract the pixel values
    # pixel_values = list(image_attempt.getdata())

    # Fix list arrangement from tuples to list
    # pixel_values_arrange = [x for sets in pixel_values for x in sets]

    # print(pixel_values_arrange[1:3])
    # pixel_values_arrange[1:3] = (255, 0, 0)
    coordinate = x, y = 0, 0

    # show new image
    # image_pillow.show()

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
                # print("asc=r: ", asc)
            encoded.putpixel((column, row), (asc, green, blue))
            index += 1
    return encoded


# Press the green button in the gutter to run the script.
def openDecode(decodeImage):

    extracted = ''

    image = Image.open(decodeImage)
    image.show()

    pixels = image.load()

    for x in range(0,image.width):
        red,green,blue = pixels[x, 0]
        # store LSB of each color channel of each pixel
        extracted += bin(red)[-1]
        extracted += bin(green)[-1]
        extracted += bin(blue)[-1]
        # print(extracted)

    chars = []
    for i in range(len(extracted)/8):
        byte = extracted[i*8:(i+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))

    flag = (''.join(chars))
    print(flag)

    pass


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
    # sanitize_words = map(lambda w: w.strip(".,;!?'\"").lower(), words)
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

    decodeImage = r'lsb_file.bmp'
    openDecode(decodeImage)

