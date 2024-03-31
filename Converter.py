import os

from PIL import Image
from os import path

import Constants


class ImageConverter(object):

    def __init__(self, target_format):
        """
        It constructs a 'Converter' object.

        :param target_format:
        """
        if not isinstance(target_format, str):
            raise ValueError("[ERROR]: 'target_format' must be a 'str' type object")

        if target_format not in Constants.SUPPORTED_OUTPUTS:
            raise ValueError("[ERROR]: Output file format is not supported")

        if target_format != 'HEIC':
            target_format = target_format.lower()

        self.__target_format = target_format

    def convert(self, image_path_list, output_directory):
        """
        It converts the file format of all specified image files.

        :param image_path_list:
        :param output_directory:
        :return:
        """
        for image_path in image_path_list:
            self.__convert(image_path, output_directory)

    def __convert(self, image_path, output_directory):
        """
        It converts the file format of specified image file creating a new image file.
        The old image file will be not overwritten or deleted.

        :param image_path:
        :param target_format:
        :param output_directory:
        :return:
        """

        if output_directory is None:
            base_path = path.dirname(image_path)
            output_directory = "{}/{}".format(base_path, "output")

        if not path.exists(output_directory):
            os.mkdir(output_directory)

        source_image = Image.open(image_path, mode='r')
        source_image.load()

        name = os.path.splitext(os.path.basename(image_path))[0]

        extension = self.__target_format.lower()

        converted_image_filename = "{}/{}.{}".format(output_directory,
                                                     name,
                                                     extension)

        source_image.save(converted_image_filename, extension)



