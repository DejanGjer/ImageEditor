import os
import cv2
import colorsys
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.ndimage import rotate
from PIL import ImageFile
from PIL import Image
ImageFile.LOAD_TRUNCATED_IMAGES = True


ORIGINAL_IMAGE_PATH = './api/static/img/elementi.bmp'
IMAGE_PATH = './api/static/img/elementi_adjusted.jpg'

class ImageProcessing:
    def __init__(self):
        self.initialize_settings()

    def initialize_settings(self):
        print("INITIALIZING IMAGE PROCESSING")
        self.original_image = None
        self.load_original_image()
        self.image = np.copy(self.original_image)
        self.save_adjusted_image()
        # default settings
        self.default_brightness = 0
        self.default_contrast = 1
        self.default_sharpness = 1
        self.default_blur = 1
        self.default_warmth = 0
        self.default_saturation = 1
        self.default_rotation = 0
        self.default_fade = 0
        self.default_highlights = 0
        self.default_shadows = 0
        self.default_vignette = 0
        self.default_radial_tilt_shift = 0
        self.default_linear_tilt_shift = 0
        self.default_zoom = 1
        # current settings
        self.brightness = 0
        self.contrast = 1
        self.sharpness = 1
        self.blur = 1
        self.warmth = 0
        self.saturation = 1
        self.rotation = 0
        self.fade = 0
        self.highlights = 0
        self.shadows = 0
        self.vignette = 0
        self.radial_tilt_shift = 0
        self.linear_tilt_shift = 0
        self.zoom = 1

    def get_adjusted_image_path(self):
        return IMAGE_PATH
    
    def get_original_image_path(self):
        return ORIGINAL_IMAGE_PATH
    
    def load_original_image(self):
        if self.original_image is None:
            if os.path.exists(ORIGINAL_IMAGE_PATH):
                locked = True
                while(locked):
                    try:
                        self.original_image = plt.imread(ORIGINAL_IMAGE_PATH).astype(np.int32)
                        locked  = False
                    except IOError as message:
                        print(f"IOError while loading image - continuing to load image")
                        locked = True
                
    # def load_images(self):
    #     if self.original_image is None:
    #         if os.path.exists(ORIGINAL_IMAGE_PATH):
    #             self.original_image = plt.imread(ORIGINAL_IMAGE_PATH).astype(np.int32)
    #     if self.image is None:
    #         if os.path.exists(IMAGE_PATH):
    #             with open(IMAGE_PATH, 'rb') as image_file:
    #                 self.image = plt.imread(IMAGE_PATH).astype(np.int32)

    def save_adjusted_image(self):
        self.image = cv2.cvtColor(self.image.astype(np.uint8), cv2.COLOR_BGR2RGB)
        cv2.imwrite(IMAGE_PATH, self.image)
     
    def adjust_image(self, adjustments):
        # self.load_original_image()
        # copy the original image to the image that will be adjusted
        self.image = np.copy(self.original_image)
        if 'brightness' in adjustments:
            self.brightness = adjustments['brightness']
        if self.brightness != self.default_brightness or 'brightness' in adjustments:
            self.apply_brightness()
        if 'contrast' in adjustments:
            self.contrast = adjustments['contrast']
        if self.contrast != self.default_contrast or 'contrast' in adjustments:
            self.apply_contrast()
        if 'sharpness' in adjustments:
            self.sharpness = adjustments['sharpness']
        if self.sharpness != self.default_sharpness or 'sharpness' in adjustments:
            self.apply_sharpness()
        if 'blur' in adjustments:
            self.blur = adjustments['blur']
        if self.blur != self.default_blur or 'blur' in adjustments:
            self.apply_blur()
        if 'warmth' in adjustments:
            self.warmth = adjustments['warmth']
        if self.warmth != self.default_warmth or 'warmth' in adjustments:
            self.apply_warmth()
        if 'saturation' in adjustments:
            self.saturation = adjustments['saturation']
        if self.saturation != self.default_saturation or 'saturation' in adjustments:
            self.apply_saturation()
        if 'rotation' in adjustments:
            self.rotation = adjustments['rotation']
        if self.rotation != self.default_rotation or 'rotation' in adjustments:
            self.apply_rotation()
        if 'fade' in adjustments:
            self.fade = adjustments['fade']
        if self.fade != self.default_fade or 'fade' in adjustments:
            self.apply_fade()
        if 'highlights' in adjustments:
            self.highlights = adjustments['highlights']
        if self.highlights != self.default_highlights or 'highlights' in adjustments:
            self.apply_highlights()
        if 'shadows' in adjustments:
            self.shadows = adjustments['shadows']
        if self.shadows != self.default_shadows or 'shadows' in adjustments:
            self.apply_shadows()
        if 'vignette' in adjustments:
            self.vignette = adjustments['vignette']
        if self.vignette != self.default_vignette or 'vignette' in adjustments:
            self.apply_vignette()
        if 'radial tilt shift' in adjustments:
            self.radial_tilt_shift = adjustments['radial tilt shift']
        if self.radial_tilt_shift != self.default_radial_tilt_shift or 'radial tilt shift' in adjustments:           
            self.apply_radial_tilt_shift()
        if 'linear tilt shift' in adjustments:
            self.linear_tilt_shift = adjustments['linear tilt shift']
        if self.linear_tilt_shift != self.default_linear_tilt_shift or 'linear tilt shift' in adjustments:
            self.apply_linear_tilt_shift()
        if 'zoom in' in adjustments:
            self.zoom = adjustments['zoom in']
        if self.zoom != self.default_zoom or 'zoom in' in adjustments:
            self.apply_zoom()
        self.save_adjusted_image()

    def apply_brightness(self):
        self.image = np.clip(self.image + self.brightness, 0, 255)

    def apply_contrast(self):
        # Ensure the contrast coefficient is within the valid range
        contrast_coefficient = np.clip(self.contrast, 0, 2)
        adjusted_image = (self.image - 128) * contrast_coefficient + 128
        adjusted_image = np.clip(adjusted_image, 0, 255).astype(np.int32)
        self.image = adjusted_image

    def apply_sharpness(self):
        kernel = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=np.float32)
        kernel[1, 1] = kernel[1, 1] + self.sharpness
        kernel[0, 1] = kernel[0, 1] - self.sharpness / 4
        kernel[1, 0] = kernel[1, 0] - self.sharpness / 4
        kernel[1, 2] = kernel[1, 2] - self.sharpness / 4
        kernel[2, 1] = kernel[2, 1] - self.sharpness / 4
        adjusted_image = self.image
        for i in range(3):
            adjusted_image[:, :, i] = signal.convolve2d(adjusted_image[:, :, i], kernel, 'same')
        adjusted_image = np.clip(adjusted_image, 0, 255)
        self.image = adjusted_image.astype(np.int32)

    def apply_blur(self):
        kernel_size = 2 * self.blur + 1 
        kernel = np.ones((kernel_size, kernel_size), dtype=np.float32) / (kernel_size ** 2)
        adjusted_image = self.image
        for i in range(3):
            adjusted_image[:, :, i] = signal.convolve2d(adjusted_image[:, :, i], kernel, 'same')
        adjusted_image = np.clip(adjusted_image, 0, 255)
        self.image = adjusted_image.astype(np.int32)

    def apply_warmth(self):
        warmth_coefficient = np.clip(self.warmth, -100, 100)
        adjusted_image = self.image
        adjusted_image[:, :, 0] = adjusted_image[:, :, 0] + warmth_coefficient
        adjusted_image[:, :, 2] = adjusted_image[:, :, 2] - warmth_coefficient
        adjusted_image = np.clip(adjusted_image, 0, 255).astype(np.int32)
        self.image = adjusted_image
    
    def apply_saturation(self):
        # Convert image to float for accurate calculations
        adjusted_image = self.image.astype(np.uint8)
        # Convert RGB to HSV
        adjusted_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2HSV).astype(np.int32)
        # Scale the saturation channel
        adjusted_image[:, :, 1] = self.saturation * adjusted_image[:, :, 1]
        # Clip the values to be in the valid range [0, 255]
        adjusted_image = np.clip(adjusted_image, 0, 255)
        # Convert back to BGR
        adjusted_image = cv2.cvtColor(adjusted_image.astype(np.uint8), cv2.COLOR_HSV2BGR)
        self.image = adjusted_image.astype(np.int32)

    def apply_rotation(self):
        adjusted_image = rotate(self.image, self.rotation, reshape=False, mode='nearest', cval=0)
        self.image = adjusted_image

    def apply_fade(self):
        # create white image with same size as self.image
        white_image = np.ones_like(self.image) * 255
        adjusted_image = self.fade * white_image + (1 - self.fade) * self.image
        self.image = adjusted_image.astype(np.int32)

    def apply_highlights(self):
        limit = 128
        adjusted_image = self.image
        bright_mask = adjusted_image > limit
        adjusted_image[bright_mask] = adjusted_image[bright_mask] + self.highlights * (255 - adjusted_image[bright_mask])
        adjusted_image = np.clip(adjusted_image, 0, 255).astype(np.int32)
        self.image = adjusted_image

    def apply_shadows(self):
        limit = 128
        adjusted_image = self.image
        dark_mask = adjusted_image < limit
        adjusted_image[dark_mask] = adjusted_image[dark_mask] - self.shadows * adjusted_image[dark_mask]
        adjusted_image = np.clip(adjusted_image, 0, 255).astype(np.int32)
        self.image = adjusted_image

    def apply_vignette(self):
        height, width, _ = self.image.shape
        # Create a grid of coordinates
        y, x = np.ogrid[:height, :width]
        # Calculate distance from the center
        center_y, center_x = height / 2, width / 2
        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2) / np.sqrt(center_x**2 + center_y**2)
        # Vignette effect formula
        vignette_mask = 1 - self.vignette * distance
        # Clip values to ensure they are in the valid range [0, 1]
        vignette_mask = np.clip(vignette_mask, 0, 1)
        # Apply the mask to each color channel
        self.image = self.image * vignette_mask[:, :, np.newaxis]

    def apply_radial_tilt_shift(self):
        height, width, _ = self.image.shape
        # Create a grid of coordinates
        y, x = np.ogrid[:height, :width]
        # Calculate distance from the center
        center_y, center_x = height / 2, width / 2
        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2) / np.sqrt(center_x**2 + center_y**2)
        # Blur strength based on the distance
        blur_mask = 2 * (self.radial_tilt_shift * distance * 10).astype(np.int32) + 1
        # Apply the mask to each color channel
        kernel_sizes = np.unique(blur_mask)
        adjusted_image = np.zeros_like(self.image)
        for kernel_size in kernel_sizes:
            kernel = np.ones((kernel_size, kernel_size), dtype=np.float32) / (kernel_size ** 2)
            for i in range(3):
                helper_image = signal.convolve2d(self.image[:, :, i], kernel, 'same')
                adjusted_image[:, :, i] = np.where(blur_mask == kernel_size, helper_image, adjusted_image[:, :, i])
        self.image = adjusted_image

    def apply_linear_tilt_shift(self):
        height, width, _ = self.image.shape
        # Create a grid of coordinates
        y, x = np.ogrid[:height, :width]
        # Calculate distance from the center
        center_y, center_x = height / 2, width / 2
        distance = np.abs(x - center_x) / center_x
        # Blur strength based on the distance
        blur_mask = 2 * (self.linear_tilt_shift * distance * 10).astype(np.int32) + 1
        # Apply the mask to each color channel
        kernel_sizes = np.unique(blur_mask)
        adjusted_image = np.zeros_like(self.image)
        for kernel_size in kernel_sizes:
            kernel = np.ones((kernel_size, kernel_size), dtype=np.float32) / (kernel_size ** 2)
            for i in range(3):
                helper_image = signal.convolve2d(self.image[:, :, i], kernel, 'same')
                adjusted_image[:, :, i] = np.where(blur_mask == kernel_size, helper_image, adjusted_image[:, :, i])
        self.image = adjusted_image

    def apply_zoom(self):
        zoom_factor = self.zoom
        # Get the shape of the original image
        height, width, channels = self.image.shape
        # Calculate the new dimensions after zooming
        new_height = int(height * zoom_factor)
        new_width = int(width * zoom_factor)
        # Create 1D arrays representing the new indices for rows and columns
        rows = np.arange(new_height) / zoom_factor
        cols = np.arange(new_width) / zoom_factor
        # Use broadcasting to create 2D arrays of indices
        rows_indices, cols_indices = np.meshgrid(rows, cols, indexing='ij')
        # Round indices to the nearest integer to get the corresponding pixel values
        rows_indices = np.round(rows_indices).astype(np.int32)
        cols_indices = np.round(cols_indices).astype(np.int32)
        # Clip indices to stay within the bounds of the original image
        rows_indices = np.clip(rows_indices, 0, height - 1)
        cols_indices = np.clip(cols_indices, 0, width - 1)
        # Create the zoomed image using advanced indexing
        adjusted_image = self.image[rows_indices, cols_indices, :]
        # Crop the center of the zoomed image to the original size
        self.image = adjusted_image[new_height // 2 - height // 2: new_height // 2 + height // 2, 
                                    new_width // 2 - width // 2: new_width // 2 + width // 2, :]
    
    def print_current_settings(self):
        print(f"Brightness: {self.brightness}")
        print(f"Contrast: {self.contrast}")
        print(f"Sharpness: {self.sharpness}")
        print(f"Temperature: {self.temperature}")
        print(f"Saturation: {self.saturation}")
        print(f"Rotation: {self.rotation}")
        print(f"Fade: {self.fade}")
        print(f"Zoom: {self.zoom}")




