#!/usr/bin/env python3
import imageio.core
from PIL import Image
import base64
import bitarray
from matplotlib import pyplot
import numpy as np
import sys
import os


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def openImage(fileImage, message, destination):

    # read the image from the parameter function
    img = Image.open(fileImage, 'r')

    # convert source image into an array of pixels, store the size of the image
    width, height = img.size
    array_pixels = np.array(list(img.getdata()))

    # 3 bytes if the image is RGB

    num_bits = 3
    # this is just an idea
    # how can i assign n to the amount of bits?

    # calculate the amount of pixels
    total_pixels = array_pixels.size//num_bits

    print("total pixels = ", total_pixels)

    # how does the program knows where to stop the message?
    # add a delimiter and convert the message to binary
    message += "@"
    # finally calculate the amount of pixels that will need to be embedded
    bits_array = bitarray.bitarray()
    bits_array.frombytes(message.encode('utf-8'))
    bit_array = [int(i) for i in bits_array]
    print("bit array: ", bit_array)


    # new try
    byte_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(byte_message)

    # check if the total pixels available is enough for the secret message or not
    # if yes then iterate thru pixels one by one to modify LSB to the bits of the message
    # if not then proceed to throw an error message

    if req_pixels > total_pixels:
        print("Image size is smaller than message")
    else:
        index = 0
        for i in range(total_pixels):
            for j in range(0, 3):
                if index < req_pixels:
                    array_pixels[i][j] = int(bin(array_pixels[i][j])[2:9] + byte_message[index], 2)
                    index += 1

    array_pixels = array_pixels.reshape(height, width, num_bits)
    encode_image = Image.fromarray(array_pixels.astype('uint8'), img.mode)
    encode_image.save(destination)
    print("Image encoded")







    # create Pillow image
    #image_pillow = Image.fromarray(data_image)
    #print(image_pillow.format)
    #print(image_pillow.mode)
    #print(image_pillow.size)

    # create pixel map
    # pixels = image_pillow.load()

    # show original image
    # image_pillow.show()

    # Converts the message into an array of bits


    # iterate through pixels to try and change the color of a single pixel
    i = 0
    # for column in range(image_pillow.size[0]):
    #     red, green, blue = pixels[column, 0]
    #     print("Pixel : [%d,%d]" % (1, 0)) #(column, 0)
    #     print("\tBefore : (%d,%d,%d)" % (red, green, blue))
    #
    #     # Default values for bits
    #     new_bit_red_pixel = 0
    #     new_bit_green_pixel = 255
    #     new_bit_blue_pixel = 255
    #     for row in range(image_pillow.size[1]):
    #         # check to see if the pixel it's red if it isn't then change to cyan
    #         if pixels[column, row] != (255, 0, 0):
    #             pixels[0, 1] = (0, 255, 255)
    #
    #     pixels[column, 0] = (new_bit_red_pixel, new_bit_green_pixel, new_bit_blue_pixel)
    #     print("\tAfter  : (%d, %d, %d)" % (new_bit_red_pixel, new_bit_green_pixel, new_bit_blue_pixel))img

    # img.save('lsb_file.bmp')

    # show new image
    # image_pillow.show()
    #image_pillow.save("output.bmp")
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



# Press the green button in the gutter to run the script.
def openDecode(decodeImage):

    print("function yet to be program")
    pass



if __name__ == '__main__':

    # check for number of arguments
    if len(sys.argv) != 3:
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
    # min_message = int(sys.argv[3])
    # To-Do validate that the min value is within that range

    # Maximum message length should be 1-64
    # max_message = int(sys.argv[4])
    # To-Do validate that the max value is within that range

    # load images
    fileImage = sys.argv[1]
    destination = 'output2.bmp'
    image_encoded = openImage(fileImage, words, destination)

    decodeImage = r'lsb_file.bmp'
    openDecode(decodeImage)

