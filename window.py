from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox,QApplication, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from tkinter import filedialog
import os
import ImageHelper
import Constants
import Converter


class Window(QWidget):

    def __init__(self):
        super().__init__()

        # Selected images to be processed
        self._image_list = list()
        self._output_extension = Constants.SUPPORTED_OUTPUTS[0]

        # The following item represents a 'QLabel' used to show current image selection status
        self._status_label = self.__create_status_label()

        # The following item represents a 'QLabel' used to show current selected output directory
        self._output_directory_label = self.__create_output_directory_label()

        self.setWindowTitle("Image Converter")
        self.setGeometry(500, 200, 600, 400)
        self.setAcceptDrops(True)

        # Button bar...
        lower_button_bar = QHBoxLayout()

        lower_button_bar.addWidget(self.__create_load_from_directory_button())
        lower_button_bar.addWidget(self.__create_clear_button())

        # Extensions and output directory selectors
        higher_button_bar = QHBoxLayout()
        higher_button_bar.setAlignment(Qt.AlignmentFlag.AlignTop)
        higher_button_bar.addWidget(self.__create_output_extension_combo_box())
        higher_button_bar.addWidget(self._output_directory_label)
        higher_button_bar.addWidget(self.__craate_change_output_directory_button())

        main_layout = QVBoxLayout()
        main_layout.addLayout(higher_button_bar)
        main_layout.addWidget(self.__create_drag_area())
        main_layout.addWidget(self._status_label)
        main_layout.addLayout(lower_button_bar)
        main_layout.addWidget(self.__craate_convert_button())

        self.setLayout(main_layout)

        # Load default output directory
        self.__change_output_directory(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'))

    @staticmethod
    def __create_status_label():

        output = QLabel()

        output.setAlignment(Qt.AlignmentFlag.AlignCenter)
        output.setText(Constants.NO_IMAGE_SELECTED)
        output.setMaximumHeight(100)

        return output

    def __create_output_directory_label(self):

        output = QLabel()

        output.setAlignment(Qt.AlignmentFlag.AlignRight)
        output.setMaximumHeight(100)

        return output

    def __create_output_extension_combo_box(self):
        """
        It creates a 'QComboBox' object which will be used to select the image extension used for output image files.
        :return:
        """
        output = QComboBox()

        output.setMaximumWidth(200)
        output.addItems(Constants.SUPPORTED_OUTPUTS)
        output.currentTextChanged.connect(self.change_output_extension)

        return output

    def __create_load_from_directory_button(self):
        """
        Creates the button which will be used to load all image files from a directory and its subdirectories.

        :return: A 'QPushButton' object.
        """
        output = QPushButton("Load from directory", self)
        output.clicked.connect(self.load_images_from_directory)
        output.setMaximumWidth(200)

        return output


    def __craate_change_output_directory_button(self):

        output = QPushButton("Change", self)
        output.clicked.connect(self.change_output_directory)
        output.setMaximumWidth(100)

        return output


    def __craate_convert_button(self):

        output = QPushButton("Convert", self)
        output.clicked.connect(self.convert)
        output.setMaximumWidth(100)

        return output


    def __create_drag_area(self):

        output = QLabel()

        output.setAlignment(Qt.AlignmentFlag.AlignCenter)
        output.setText("\n\nDrop Image here\n\n")
        output.setStyleSheet('''
                    QLabel{
                        border: 4px dashed #aaa
                    }
                ''')

        return output

    def __create_clear_button(self):
        """
        Creates the button which will be used to clear all selected images.

        :return: A 'QPushButton' object.
        """
        output = QPushButton("Clear all", self)
        output.clicked.connect(self.clear)
        output.setMaximumWidth(200)

        return output

    def load_images_from_directory(self):
        """
        It adds all image files inside a directory and all its subdirectories.
        """
        folder_path = filedialog.askdirectory()
        if folder_path:

            image_list = ImageHelper.get_image_files(folder_path)

            for file in image_list:
                if file not in self._image_list:
                    self._image_list.append(file)

            self.update_selected_image_label()

    def update_selected_image_label(self):

        message = Constants.IMAGE_SELECTED_AMOUNT.format(len(self._image_list))
        self._status_label.setText(message)

    def clear(self):
        """
        It clears the list of all selected image files
        """
        self._image_list = None
        self._status_label.setText(Constants.NO_IMAGE_SELECTED)

    def change_output_extension(self, text):
        """
        It sets the extension type of output image files.

        :param text:
        :return:
        """
        self._output_extension = text
    

    def change_output_directory(self):
        """
        Set output directory
        :return:
        """
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.__change_output_directory(folder_path)

    def __change_output_directory(self, directory):

        self._output_directory = os.path.join(directory, "output")
        self._output_directory_label.setText(self._output_directory)


    def dragEnterEvent(self, event):
        event.accept()

        # if acceptable(urls,SUPPORTED_INPUTS):
        #     self.status.setText("Images detected, release to start")
        # else:
        #     self.status.setText("File formats not supported")
        
    def dragLeaveEvent(self,event):
        event.accept()
    
    def dropEvent(self, event):
        event.accept()

        urls = event.mimeData().urls()
        urls = [url.toLocalFile() for url in urls]

        for file in urls:
            if ImageHelper.is_image(file) and file not in self._image_list:
                self._image_list.append(file)
                self.update_selected_image_label()


    def convert(self):

        if len(self._image_list) == 0:
            return

        converter = Converter.ImageConverter(self._output_extension)
        converter.convert(self._image_list, self._output_directory)

        self._image_list = list()
        self.update_selected_image_label()




