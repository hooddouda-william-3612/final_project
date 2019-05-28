from os import startfile
from tkinter import *
from PIL import ImageTk, Image #Will need to download
from google_images_download import google_images_download #Will need to download
 
def get_words(): #function for I/O
    with open("test.txt", "r") as message: #Hard coded for now
        message = str(message.readlines()[0]) #change contents of text file into string. ONLY WORKS FOR ONE LINE
    return message

def recurse(message = get_words()): #function for recursion
    if len(message) == 1:
        get_pics(message)
        return message
    else:
        message = message[1:]
        return recurse(message)
    
def get_pics(char):
    response = google_images_download.googleimagesdownload()   #class instantiation
    arguments = {"keywords":char,"limit":1, "print_urls":False}   #creating list of arguments
    path = response.download(arguments)   #passing the arguments to the function
    return path   #printing absolute paths of the downloaded images

def display(pic):
    root = Tk()  
    canvas = Canvas(root, width = 3000, height = 3000)  
    canvas.pack()  
    img = ImageTk.PhotoImage(Image.open(pic))  
    canvas.create_image(0, 0, anchor=NW, image=img)  
    root.mainloop()  

def main():
    get_pics("h")

if __name__ == "__main__":
    main()
