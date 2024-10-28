import os

import cv2
import numpy as np

def box_filter(image, ksize=5):
    return cv2.blur(image, (ksize, ksize))

def gaussian_filter(image, ksize=5, sigma=1):
    return cv2.GaussianBlur(image, (ksize, ksize), sigma)

def median_filter(image, ksize=5):
    return cv2.medianBlur(image, ksize)

def laplacian_sharpening(image):
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    sharpened = cv2.convertScaleAbs(image - laplacian)
    return sharpened

def unsharp_masking(image, ksize=5, sigma=1.0, amount=1.5):
    blurred = cv2.GaussianBlur(image, (ksize, ksize), sigma)
    unsharp_image = cv2.addWeighted(image, 1 + amount, blurred, -amount, 0)
    return unsharp_image

def sobel_gradient(image):
    grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
    grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)
    gradient_magnitude = cv2.magnitude(grad_x, grad_y)
    return np.uint8(gradient_magnitude)

def resize_image(image, width=300):
    height = int(image.shape[0] * (width / image.shape[1]))
    return cv2.resize(image, (width, height))


def load_images(image_folder):
    images, titles = [], []
    for filename in os.listdir(image_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            images.append(cv2.imread(os.path.join(image_folder, filename), cv2.IMREAD_GRAYSCALE))
            titles.append(filename)
    return images, titles
