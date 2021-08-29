from PIL import Image
from matplotlib import pyplot
from numpy import asarray


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
    image_pillow.show()
    #image_pillow.save("output.bmp")

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
    # load images
    fileImage = r'img/Img_02_24.bmp'
    openImage(fileImage)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
