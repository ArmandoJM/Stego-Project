from PIL import Image
from matplotlib import pyplot
from numpy import asarray


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def openImage(fileImage):
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

    image_pillow.show()
    for column in range(image_pillow.size[0]):
        for row in range(image_pillow.size[1]):
            pixels[column, row] = (0, 0, 0)

    image_pillow.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # load images
    fileImage = r'img/Img_02_24.bmp'
    openImage(fileImage)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
