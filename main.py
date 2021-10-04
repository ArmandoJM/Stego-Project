#!/usr/bin/env python3
import imageio.core
from PIL import Image
import base64
import bitarray
from matplotlib import pyplot
import numpy as np
import sys
import os


def openImage(fileImage, message, destination):
    # read the image from the parameter function
    img = Image.open(fileImage, 'r')

    # convert source image into an array of pixels, store the size of the image
    width, height = img.size
    array_pixels = np.array(list(img.getdata()))

    # 3 bytes if the image is RGB
    # this is just an idea
    num_bits = 3

    # calculate the amount of pixels
    total_pixels = array_pixels.size // num_bits

    print("total pixels = ", total_pixels)

    # check if message is bigger than the pixel size
    # what we want to do is hide and if the message doesn't fit then print message
    # hide it until runs out of image/message then print to the screen message didn't complete
    # is there more image or message , no then? it didn't fit
    # example hiding 4GB size
    #
    # GOAL is to hide more significant bit


    # how does the program knows where to stop the message?
    # add a delimiter and convert the message to binary

    # finally calculate the amount of pixels that will need to be embedded
    bits_array = bitarray.bitarray()
    bits_array.frombytes(message.encode('utf-8'))
    bit_array = [int(i) for i in bits_array]
    print("bit array: ", bit_array)

    # new try
    message += "$t3go"
    byte_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(byte_message)

    # check if the total pixels available is enough for the secret message or not
    # if yes then iterate thru pixels one by one to modify LSB to the bits of the message
    # if not then proceed to throw an error message


    index = 0
    for i in range(total_pixels):
        for j in range(0, 3):
            if index < req_pixels:
                array_pixels[i][j] = int(bin(array_pixels[i][j])[2:9] + byte_message[index], 2)
                index += 1

    array_pixels = array_pixels.reshape(height, width, num_bits)
    encode_image = Image.fromarray(array_pixels.astype('uint8'), img.mode)
    encode_image.save(destination)
    #print("Image encoded")

    length = len(message)
    # print(length)

    # message minimum 1
    if length < 1:
        print("No message input")
        return False


# Converts the string into binary
def messageToBinary(message):
    # Convert "string" to binary format
    if type(message) == str:
        return ''.join([format(ord(i), "08b") for i in message])
    elif type(message) == bytes or type(message) == np.array:
        return [format(i, "08b") for i in message]
    elif type(message) == int or type(message) == np.uint8:
        return format(message, "08b")
    else:
        raise TypeError("File image not supported")


# reads image to get all the bits of every pixel of it.
def openDecode(decodeImage):
    num_bytes = 0
    img = Image.open(decodeImage, 'r')
    array_image = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        num_bytes = 3

    total_pixels = array_image.size // num_bytes

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array_image[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-10:] == "$t3go":
            break
        else:
            message += chr(int(hidden_bits[i], 2))

    if "$t3go" in message:
        print("Hidden message: ", message[:-10])
    else:
        print("No hidden message found")


if __name__ == '__main__':

    program_flag = sys.argv[1]
    if program_flag == '-h':
        data_file = sys.argv[2]
        cover_file = sys.argv[3]
        stego_file = sys.argv[4]

    # ToDo: check if files datafile and coverfile exist write to the stegofile
    # i guess if it's specified

    if program_flag == '-e':
        stego_file = sys.argv[2]
        data_file = sys.argv[3]

    # check for number of arguments
    if len(sys.argv) != 3:
        print("Usage: " + sys.argv[0] + "<dirname> <size>")
        sys.exit(1)

    # check that the first arg is a picture(i.e bmp)
    if not os.path.exists(sys.argv[1]):
        print(sys.argv[1] + " is not a file image")
        sys.exit(1)

    # read file for embedded message to be hidden
    file = open(sys.argv[2], encoding='utf-8')

    # ToDo:
    # check if stegofile exists, write to datafile
    # call a function for extracting
    # load images
    fileImage = sys.argv[1]
    destination = 'output2.bmp'
    image_encoded = openImage(fileImage, file.read(), destination)

    # decode image
    decodeImage = r'output2.bmp'
    openDecode(decodeImage)
