import os
import Constants

from PIL import Image


def is_image(file):
    """
    It returns 'True' if specified file is an image; otherwise, it returns 'False'
    :param file: The full path to a file.
    :return:
    """
    try:
        if not os.path.isfile(file):
            return False

        source_image = Image.open(file, mode='r')
        if source_image.format.lower() not in Constants.SUPPORTED_INPUTS:
            return False

        source_image.close()

        return True

    except:
        return False


def get_image_files(path):
    """
    It returns a list of all image files inside specified directory.
    """
    output = list()

    for name in os.listdir(path):

        fullname = os.path.join(path, name)

        if is_image(fullname):
            output.append(fullname)

        if os.path.isdir(fullname):
            image_list = get_image_files(fullname)
            output += image_list

    return output