import cv2
import numpy as np
import tkinter as tk
from tkinter import Label, StringVar
from tkinter import ttk
from PIL import Image, ImageTk
import os
from transformations import box_filter, gaussian_filter, median_filter, laplacian_sharpening, unsharp_masking, sobel_gradient

# Folder containing images
IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), 'images')

def resize_image(image, width=200):
    height = int(image.shape[0] * (width / image.shape[1]))
    resized_image = cv2.resize(image, (width, height))
    return resized_image

def display_images(images, titles, options):
    for widget in frame.winfo_children():
        widget.destroy()

    for i in range(len(images)):
        resized_image = resize_image(images[i])
        image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_GRAY2RGB)
        image_pil = Image.fromarray(image_rgb)
        image_tk = ImageTk.PhotoImage(image_pil)

        title_label = Label(frame, text=titles[i])
        title_label.grid(row=(i // 7) * 2, column=i % 7, padx=5, pady=(0, 5))

        label = Label(frame, image=image_tk)
        label.image = image_tk
        label.grid(row=(i // 7) * 2 + 1, column=i % 7, padx=5, pady=(0, 5))
        
        get_option = options[i];
        if get_option is not None:
            get_option().grid(row=(i // 7) * 2+2, column=i % 7, padx=5, pady=(0, 5))


def apply_transformations(selected_image):
    global original_image, frame
    if selected_image is None:
        return

    original_image = selected_image

    box_filtered = box_filter(selected_image)
    gaussian_filtered = gaussian_filter(selected_image)
    median_filtered = median_filter(selected_image)
    laplacian_sharpened = laplacian_sharpening(selected_image)
    unsharp_image = unsharp_masking(selected_image)
    sobel_gradient_image = sobel_gradient(selected_image)
    
    images = [selected_image, box_filtered, gaussian_filtered, median_filtered, laplacian_sharpened, unsharp_image, sobel_gradient_image]
    titles = ['Original', 'Box Filter', 'Gaussian Filter', 'Median Filter', 'Laplacian Sharpening', 'Unsharp Masking', 'Sobel Gradient']
    options = [None, None, None, None, None, None, None]

    display_images(images, titles, options)

def on_selection_change(event):
    print(event)
    selected_image_name = dropdown_var.get()
    selected_image_path = os.path.join(IMAGE_FOLDER, selected_image_name)
    selected_image = cv2.imread(selected_image_path, cv2.IMREAD_GRAYSCALE)
    apply_transformations(selected_image)

# Set up the main Tkinter window
root = tk.Tk()
root.title("Image Transformations")
root.state('zoomed')
# root.attributes('-zoomed', True) # For Linux and macOS


# Set up the dropdown menu
dropdown_var = StringVar()
dropdown_menu = ttk.Combobox(root, textvariable=dropdown_var)
dropdown_menu.bind("<<ComboboxSelected>>", on_selection_change)

image_files = os.listdir(IMAGE_FOLDER)
dropdown_menu['values'] = [f for f in image_files if f.endswith(('.png', '.jpg', '.jpeg'))]
dropdown_menu.pack(pady=10)

if image_files:
    dropdown_var.set(image_files[0])

# Frame for displaying images
frame = tk.Frame(root)
frame.pack(padx=10, pady=200)

original_image = None
binary_label = None
contrast_label = None

# Responsible for initial rendering
on_selection_change(0)

# Start the Tkinter main loop
root.mainloop()
