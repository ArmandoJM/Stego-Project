#!/usr/bin/env python3

import io
import os

from PIL import Image
import sys


# manage the manipulation of the message file to be embedded
def generateData(data):
    file = open(data).read()

    # list of given data in binary array
    new_data = []

    for i in file:
        new_data.append(format(ord(i), '08b'))

    return new_data


# pixels are changed into 8 bit binary
def modePix(pix, data):
    datalist = generateData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):

        # extract 3 pixels at the time
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if datalist[i][j] == '1' and (pix[j] & 0x10) != 0:
                print("datalist == 1? :", datalist, "pix[j] != ", pix[j])
                continue
            if datalist[i][j] == '0' and (pix[j] & 0x10) == 0:
                print("datalist == 0? : ", datalist, "pix[j] == ", pix[j])
                continue
            if datalist[i][j] == 1:
                if pix[j] < 16:
                    pix[j] = 16
                    continue
                x = pix[j] & 0xF
                if x <= 8:
                    pix[j] = pix[j] - (x + 1)
            if datalist[i][j] == 0:
                if pix[j] > 240:
                    pix[j] = 240
                    continue
                x = pix[j] & 0xF
                if x <= 8:
                    pix[j] = pix[j] - (x + 1)
            #
            # if datalist[i][j] == '0':
            #     pix[j] = pix[j] & 0xFE
            # elif datalist[i][j] == '1':
            #     if pix[j] != 0:
            #         pix[j] = pix[j] | 0x01

        # eight pixels of every set tells to stop or to keep reading
        # 0 means message is done
        if i == lendata - 1:
            if pix[-1] % 2 == 0:
                if pix[-1] != 0:
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if pix[-1] % 2 != 0:
                pix[-1] -= 1

        # implemented yield notation because of the use of tuples sliced
        # instead of returning a value one at the time making it slow
        # so in this case the generator function produces a sequence of values
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


# function that takes care of the new pixels
def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    # the new pixels go into the new image
    for pixel in modePix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1


def encode():
    data_file = sys.argv[2]
    image = Image.open(data_file, 'r')

    cover_file = sys.argv[3]
    if len(cover_file) == 0:
        raise ValueError('Data is empty')

    # read file for embedded message to be hidden
    data = sys.argv[3]
    newimg = image.copy()
    encode_enc(newimg, data)

    stego_file = sys.argv[4]
    newimg.save(stego_file)


# decode function
def decode(decodeImage):
    num_bytes = 0
    img = Image.open(decodeImage, 'r')

    data = ''
    imgdata = iter(img.getdata())

    # extract 3 pixels at a time
    while True:
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] + imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if i & 0x10 == 0:
                binstr += '0'
            else:
                binstr += '1'

        # int to char base 2 and return the decoded message
        # I think this is incorrect the way it's returning the decoded message,
        data += chr(int(binstr, 2))
        if pixels[-1] & 0x10 == 0:
            return data



def main():
    # ecnode flag
    program_flag = sys.argv[1]
    if program_flag == '-h':
        encode()

    # decode flag
    if program_flag == '-e':
        stego_file = sys.argv[2]
        data_file = sys.argv[3]
        # decode image
        data_message = decode(stego_file)
        # write back to file
        with open(data_file, "w+", encoding='utf-8') as message:
            message.write(data_message)


if __name__ == '__main__':
    main()
