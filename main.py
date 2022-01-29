#!/usr/bin/env python3

import io
import os
import sys

from PIL import Image
import sys

global message_length


# Subtract 8 bits from current length to get how many 0s to pad for one-byte length.
def pad_to_byte(bitstring):
    padding_length = 8 - len(bitstring)
    bitstring = ('0' * padding_length) + bitstring
    return bitstring


def addBitandLength(new_data, message_length):
    input_bitstring = bin(int('4', base=16)).lstrip('0b')
    new_data.append(pad_to_byte(input_bitstring))
    tmp = message_length

    for i in range(4):
        x = tmp & 0xFF
        bitstring = bin(x).lstrip('0b')
        bitstring = pad_to_byte(bitstring)
        new_data.append(bitstring)
        # bit shift right
        tmp = tmp >> 8


# manage the manipulation of the message file to be embedded
def generateData(data):
    file = open(data).read()

    # list of given data in binary array
    new_data = []
    length_data = len(data)

    # first hides number of bits
    # if sys.argv[1] == '4':
    #     message_length = os.stat(sys.argv[4]).st_size
    #     addBitandLength(new_data, message_length)
    if (sys.argv[1]) == '5':
        message_length = int(sys.argv[1])
        addBitandLength(new_data, message_length)
    # if sys.argv[1] == '6':
    #     message_length = os.stat(sys.argv[4]).st_size
    #     addBitandLength(new_data, message_length)

    print(len(new_data[2]))
    for i in file:
        new_data.append(format(ord(i), '08b'))

    # second hides the length of the message
    # print(new_data)
    return new_data


# pixels are changed into 8 bit binary
def modePix(pix, data):
    bit_length = ''
    datalist = generateData(data)
    global message_length
    lendata = len(datalist)

    # variable use for extraction
    message_length = lendata
    imdata = iter(pix)

    if len(sys.argv) < 6 or sys.argv[1] == '4':
        bit_length = '4'
        message_bit_position = 4
        # print('4')
    elif sys.argv[1] == '5':
        bit_length = 5
        message_bit_position = 5
        # print('5')
    elif sys.argv[1] == '6':
        bit_length = 6
        message_bit_position = 6
        # print('6')

    # initialize byte object

    # print(lendata)
    for i in range(lendata):
        # extract 3 pixels at the time
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]
        # print(pix[i])
        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if bit_length == 4:  # note to yourself use ' ' not just 4 by itself dumbdumb
                if datalist[i][j] == '1' and (pix[j] & 0x10) != 0:
                    # print("datalist[i][j] == '1' -> :", datalist, "pix[j] != ", pix[j])
                    continue
                if datalist[i][j] == '0' and (pix[j] & 0x10) == 0:
                    # print("datalist[i][j] == '0' -> : ", datalist, "pix[j] == ", pix[j])
                    continue
                if datalist[i][j] == '1':
                    if pix[j] <= 16:
                        pix[j] = 16
                        continue
                    x = pix[j] & 0xF
                    if x >= 8:
                        pix[j] = pix[j] + (16 - x)
                    else:
                        pix[j] = pix[j] - (x + 1)
                if datalist[i][j] == '0':
                    if pix[j] >= 240:
                        pix[j] = 239
                        continue
                    x = pix[j] & 0xF  # 0xF = 15 decimal
                    if x >= 8:
                        pix[j] = pix[j] + (16 - x)
                    else:
                        pix[j] = pix[j] - (x + 1)
            if bit_length == 5:
                for k in range(0, 8):
                    if datalist[i][j] == '1' and (pix[j] & 0x20) != 0:
                        # print("datalist[i][j] == '1' -> :", datalist[i][j], "pix[j] != ", pix[j])
                        # print("pix[j] in hex !=", hex(pix[j]))
                        continue
                    if datalist[i][j] == '0' and (pix[j] & 0x20) == 0:
                        # print("datalist[i][j] == '0' -> : ", datalist[i][j], "pix[j] == ", pix[j])
                        # print("pix[j] in hex ==", hex(pix[j]))
                        continue
                    if datalist[i][j] == '1':
                        if pix[j] <= 32:
                            # print("if pix[j] <= 32 : ", pix[j], ' = 32')
                            # print("pix[j] in hex =", hex(pix[j]))
                            pix[j] = 32
                            continue
                        x = pix[j] & 0x1F  # 31
                        # print('x = ', x)
                        # print("x in hex =", hex(x))
                        if x >= 16:
                            pix[j] = pix[j] + (32 - x)
                            # print('pix[j] = pix[j] + (32 - x)= ', pix[j])
                            # print('pix[j] in hex =", hex(pix[j]')
                        else:
                            # print("else: ", pix[j])
                            pix[j] = pix[j] - (x + 1)
                    # if datalist[i][j] == '0':
                    #     pix[j] = pix[j] & 0xDF  # 0xDF = 223
                    # elif datalist[i][j] == '1':
                    #     pix[j] = pix[j] | 0x20  # 0x20 = 32 decimal
                    if datalist[i][j] == '0':
                        if pix[j] >= 224:
                            pix[j] = 223
                            continue
                        x = pix[j] & 0x1F  # 0x1F = 31 decimal
                        if x >= 16:
                            pix[j] = pix[j] + (32 - x)
                        else:
                            pix[j] = pix[j] - (x + 1)
            # bit 6 for hiding
            if bit_length == '6':
                for k in range(0, 8):
                    if datalist[i][j] == '1' and (pix[j] & 0x40) != 0:
                        # print("datalist[i][j] == '1' -> :", datalist, "pix[j] != ", pix[j])
                        continue
                    if datalist[i][j] == '0' and (pix[j] & 0x40) == 0:
                        # print("datalist[i][j] == '0' -> : ", datalist, "pix[j] == ", pix[j])
                        continue
                    if datalist[i][j] == '1':
                        if pix[j] <= 64:
                            pix[j] = 64
                            continue
                        x = pix[j] & 0x3F  # decimal 63
                        if x >= 32:
                            pix[j] = pix[j] + (64 - x)
                        else:
                            pix[j] = pix[j] - (x + 1)
                    # if datalist[i][j] == '0':
                    #     pix[j] = pix[j] & 0xBF  # 0xBF = 191
                    # elif datalist[i][j] == '1':
                    #     pix[j] = pix[j] | 0x40  # 0x40 = 64 decimal
                    if datalist[i][j] == '0':
                        if pix[j] >= 192:
                            pix[j] = 191
                            continue
                        x = pix[j] & 0x3F  # 0x3F = 63 decimal
                        if x >= 32:
                            pix[j] = pix[j] + (64 - x)
                        else:
                            pix[j] = pix[j] - (x + 1)

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


def encode(data_file, cover_file, stego_file):  # data_file, cover_file, stego_file
    # data_file = sys.argv[3]
    image = Image.open(data_file, 'r')
    # print("opens image")

    # cover_file = sys.argv[4]
    if len(cover_file) == 0:
        raise ValueError('Data is empty')

    # read file for embedded message to be hidden
    data = cover_file
    # print('data not empty')
    newimg = image.copy()
    encode_enc(newimg, data)

    # stego_file = sys.argv[5]
    newimg.save(stego_file)


def extractBitandLength(img):
    imgdata = iter(img.getdata())
    bit_length = '5'
    data = ''
    # x is the  first 8 bits of length. Which means range(5) o
    tmp = 3251
    pass

# decode function
def decode(decodeImage, data_file):
    num_bytes = 0
    img = Image.open(decodeImage, 'r')

    pix = img.load()

    # bit_shift = extractBitandLength(img)
    # print(bit_shift)
    # opening a file

    # print(pix[0, 0])
    # print(pix[1, 0])
    # # print(pix[2, 0])
    # print(pix[3, 0])
    # print(pix[4, 0])
    # # print(pix[5, 0])
    # print(pix[6, 0])
    # print(pix[7, 0])
    # # print(pix[8, 0])
    # print(pix[9, 0])
    # print(pix[10, 0])
    # # print(pix[11, 0])
    # print(pix[12, 0])
    #print(pix[13, 0])

    bit_length = sys.argv[4]
    # extractBitandLength()
    data = ''

    imgdata = iter(img.getdata())

    for i in range(5):  # for i in range(5)
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] + imgdata.__next__()[:3]]

        binstr = ''

        for j in pixels[0:13]:  # for j in pixels[0:13]:
            k = i + j
            k = k >> 8
            binstr += str(k)

    # extract 3 pixels at a time
    while True:

        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] + imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if bit_length == '4':
                if i & 0x10 == 0:
                    binstr += '0'
                    # print(binstr)
                else:
                    binstr += '1'
                    # print(binstr)
            if bit_length == '5':
                if i & 0x20 == 0:
                    # print(" i & 0x20 = ", i)
                    binstr += '0'
                    # print(binstr)
                else:
                    # print("else i = ", i)
                    binstr += '1'
                    # print(binstr)
            if bit_length == '6':
                if i & 0x40 == 0:
                    binstr += '0'
                    # print(binstr)
                else:
                    binstr += '1'
                    # print(binstr)

        # int to char base 2 and return the decoded message
        # I think this is incorrect the way it's returning the decoded message,
        # data += chr(int(binstr, 2))
        # if pixels[-1] % 2 != 0:
        #     return data

        data += chr(int(binstr, 2))
        if pixels[-1] % 2 != 0:
            return data


def main():
    # ecnode flag
    # bit_flag = sys.argv[2]

    if sys.argv[2] == 'h':
        data_file = sys.argv[3]
        cover_file = sys.argv[4]
        stego_file = sys.argv[5]
        encode(data_file, cover_file, stego_file)
    elif sys.argv[1] == 'h':
        data_file = sys.argv[2]
        cover_file = sys.argv[3]
        stego_file = sys.argv[4]
        encode(data_file, cover_file, stego_file)

    # decode flag
    if sys.argv[1] == 'e':
        stego_file = sys.argv[2]
        data_file = sys.argv[3]

        # decode image
        data_message = decode(stego_file, data_file)
        # write back to file

        with open(data_file, 'wb') as message:
            message.write(data_message.encode('utf-8'))


if __name__ == '__main__':
    main()
