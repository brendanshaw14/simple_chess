from PIL import Image, ImageTk
import tkinter as tk

class piece: 
    def __init__(self, name, color, position, image_path): 
        #initialize name, color, and position
        self.name = name
        self.color = color
        self.position = position
        #convert image to tk object and initialize
        image = Image.open(image_path)
        resized_image = image.resize((55, 55))
        self.image = ImageTk.PhotoImage(resized_image)
         