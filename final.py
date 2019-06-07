"""
Create GUI from string.

Take in a text file and display each character of it in GUI using images
downloaded from online.

CS 162 Final Project
Simeon Patton
William Hood-Douda
"""

from tkinter import *  # pylint: disable = W0401, W0614
from os import getcwd
from shutil import rmtree
from google_images_download import google_images_download
from PIL import ImageTk, Image  # pylint = E0401


class WriteNote:
    """
    Make a randsom note from a file.

    Take in a text file and create a new file with paths to pictures.
    The class has methods for recursively spliting the words of the
    input file into individual characters, downloading images from
    google using those characters as search terms, and creating a
    file with the paths of the downloaded images.
    """

    def __init__(self, file_in="hello_world.txt", message=""):
        """
        Initialize a WriteNote object.

        Initialize an object for writing the file which contains
        image paths.

        Arguments:
        ----------
            self: current instance of WriteNote object.
            file_in: file with text to read that will become note message.
            message: string version of text from file_in. Not to be
            populated manually.
            path_list: list containing paths to downloaded files. Not to
            be populated manually.
        """
        self.file_in = file_in
        with open(self.file_in, "r") as my_file:
            message = my_file.read()
        self.message = message
        self.path_list = []

    def get_pictures(self):
        """
        Break a string into letters recursivly.

        Break up a string using recursion and pass characters to download
        function to be downloaded.

        Arguments:
        -----------
            self: current instance of WriteNote object.
        """
        if not self.message:
            return None
        front_letter = self.message[0]
        self.message = self.message[1:]
        self.download(front_letter)
        self.get_pictures()
        return None

    def download(self, char):
        """
        Download images from google.

        Download images from google and create a list with their
        paths. The method is called by the get_pictures method
        and is not to be called manually. When the character passed
        in is a space, the method will throw an index error due to
        the way that the google_images libray returns paths. This
        error is caught; the list is manually appended with a space
        and get_pictures is called. Response returns tuple with zeroth
        element being a dictionary with the search term as a key and a
        list of the paths for that term for the value.

        Arguments:
        ----------
            self: current instance of WriteNote object.
            char: character of message passed in by get_pictures to be
            used as search term.
        """
        try:
            response = (
                google_images_download.googleimagesdownload()
            )  # class instantiation
            arguments = {
                "keywords": char,
                "limit": 1,
                "print_urls": False,
                "format": "png",
            }  # search term and other arguments
            path = response.download(arguments)  # path of images
            path = path[0].get(char)[0]
            self.path_list.append(path)
        except IndexError:
            self.path_list.append(" ")
            self.get_pictures()

    def write_note(self, mode="x"):
        """
        Create file with paths of images.

        Create a text file with downloaded image paths. Writes from
        internal path_list attribute. Uses try and except to catch
        if the file already exists. If it does, the method calls
        itself with mode parameter as write.

        Arguments:
        -----------
            self: current instance of WriteNote object.
            mode: mode for opening file; defaults to "x" to create file.
        """
        try:
            randsom_note = open("randsom_note.txt", mode)
            for i in range(len(self.path_list)):
                randsom_note.write(self.path_list[i] + "\n")
            randsom_note.close()
        except FileExistsError:
            self.write_note("w")


class ReadNote:  # pylint: disable = R0903
    """
    Class to create GUI interface and display images.

    Create a GUI window that is based on the size of the incoming file.
    The images are sourced and downloaded using a python module,
    "Google-Images-Search". The images are downloaded to the local
    working directory, converted to PNG files (used by tkinter), and
    then resized using python PIL library. Images are limited to 100
    downloads to decrease time and system resource utilization.

    Methods:
    -------
    __init__:
        Initialization method to create the instance of the class object.
    display:
        Create GUI interface using tkinter for python 3.

    """

    def __init__(self, note_name="randsom_note.txt"):
        """
        Initialize function to start the ReadNote class.

        Parameters:
        ---------
        note_name:
            File name used as an input for the program to search. The contents
            of the file may not be more than 100 characters in length.
        path_list:
            List of composed images that are stored on the user computer.

        """
        self.note_name = note_name
        self.path_list = []
        self.path_list = [line.rstrip("\n") for line in open(self.note_name)]

    def display(self):
        """
        Display downloaded images.

        Creates the window that is used to display the images in a GUI fashion.
        """
        root = Tk()
        horizontal_scroll_bar = Scrollbar(root, orient=HORIZONTAL)
        horizontal_scroll_bar.pack(side=BOTTOM, fill=X)

        canvas = Canvas(
            root,
            xscrollcommand=horizontal_scroll_bar.set,
            scrollregion=(0, 0, (len(self.path_list) * 150), 5000),
            width=(len(self.path_list) * 150),
            height=150,
        )
        canvas.pack()
        horizontal_scroll_bar.config(command=canvas.xview)

        #  This controls the EXIT button
        bottom_frame = Frame(root)
        bottom_frame.pack(side=BOTTOM)
        exit_button = Button(bottom_frame, text="EXIT", command=root.destroy)
        exit_button.pack(side=BOTTOM)

        img_list = list()
        for i, _ in enumerate(self.path_list):
            for j in range(10):
                if self.path_list[i] != " ":
                    img_pil = Image.open(self.path_list[i])
                    img_pil_resized = img_pil.resize(
                        (150, 150), Image.ANTIALIAS)
                    img_tk = ImageTk.PhotoImage(img_pil_resized)
                    canvas.create_image(
                        (i * 150), j * 150, anchor=NW, image=img_tk)
                    img_list.append(img_tk)

        root.protocol("WM_DELETE_WINDOW", delete)
        root.mainloop()


def delete():
    """
    Clean up downloads folder.

    Delete the folder of downloaded images from the current working directory.
    """
    path = getcwd() + "\\downloads"
    rmtree(path)


def play_function(file_name):
    """
    Run program to download and display images from a text file.

    Function to run the program upon call and test the built in functions.
    """
    test_write = WriteNote(file_name)
    test_write.get_pictures()
    test_write.write_note()

    test_read = ReadNote()
    test_read.display()
    delete()


def main():
    """
    Run main function.

    Run the main function of the module.
    """
    play_function("test_jk.txt")


if __name__ == "__main__":
    main()
