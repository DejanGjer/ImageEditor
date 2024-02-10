import os
import cv2
import colorsys
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import rotate
from PIL import ImageFile
from PIL import Image
ImageFile.LOAD_TRUNCATED_IMAGES = True


ORIGINAL_IMAGE_PATH = './api/static/img/elementi.bmp'
IMAGE_PATH = './api/static/img/elementi_adjusted.jpg'

class ImageProcessing:
    def __init__(self, original_image=None, image=None):
        self.original_image = original_image
        self.image = image
        if self.original_image is None or self.image is None:
            self.load_images()
        self.initialize_settings()
        print("INITIALIZING IMAGE PROCESSING")

    def initialize_settings(self):
        self.brightness = 0
        self.contrast = 1
        self.sharpness = 1
        self.warmth = 0
        self.saturation = 1
        self.rotation = 0
        self.fade = 0
        self.highlights = 0
        self.shadows = 0
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
                
    def load_images(self):
        if self.original_image is None:
            if os.path.exists(ORIGINAL_IMAGE_PATH):
                self.original_image = plt.imread(ORIGINAL_IMAGE_PATH).astype(np.int32)
        if self.image is None:
            if os.path.exists(IMAGE_PATH):
                with open(IMAGE_PATH, 'rb') as image_file:
                    self.image = plt.imread(IMAGE_PATH).astype(np.int32)

    def save_adjusted_image(self):
        # print(f"SHAPE OF ADJUSTED IMAGE: {self.image.shape}")
        # print(f"TYPE OF ADJUSTED IMAGE: {self.image.dtype}")
        self.image = cv2.cvtColor(self.image.astype(np.uint8), cv2.COLOR_BGR2RGB)
        cv2.imwrite(IMAGE_PATH, self.image)
        # # save image with matplotlib
        # plt.imsave("./api/static/img/plt_saved.jpg", self.image)
        # pil_image = Image.fromarray(self.image)
        # pil_image.save("./api/static/img/pil_saved.jpg")
        # # save image array to file
        # np.save("./api/static/img/np_saved.npy", self.image)

    # def rgb_to_hsv(self, rgb_image):
    #     # Convert RGB image to HSV
    #     hsv_image = np.zeros_like(rgb_image, dtype=np.float32)
    #     for i in range(rgb_image.shape[0]):
    #         for j in range(rgb_image.shape[1]):
    #             hsv_image[i, j, :] = colorsys.rgb_to_hsv(*rgb_image[i, j, :]/255.0)

    #     return hsv_image

    # def hsv_to_rgb(self, hsv_image):
    #     # Convert HSV image to RGB
    #     rgb_image = np.zeros_like(hsv_image, dtype=np.uint8)
    #     for i in range(hsv_image.shape[0]):
    #         for j in range(hsv_image.shape[1]):
    #             rgb_image[i, j, :] = np.array(colorsys.hsv_to_rgb(*hsv_image[i, j, :])) * 255.0

    #     return rgb_image


    def adjust_image(self, adjustments):
        # self.load_original_image()
        # copy the original image to the image that will be adjusted
        self.image = np.copy(self.original_image)
        if 'brightness' in adjustments:
            self.brightness = adjustments['brightness']
        self.apply_brightness()
        if 'contrast' in adjustments:
            self.contrast = adjustments['contrast']
        self.apply_contrast()
        if 'sharpness' in adjustments:
            self.sharpness = adjustments['sharpness']
        self.apply_sharpness()
        if 'warmth' in adjustments:
            self.warmth = adjustments['warmth']
        self.apply_warmth()
        if 'saturation' in adjustments:
            self.saturation = adjustments['saturation']
        self.apply_saturation()
        if 'rotation' in adjustments:
            self.rotation = adjustments['rotation']
        self.apply_rotation()
        if 'fade' in adjustments:
            self.fade = adjustments['fade']
        self.apply_fade()
        if 'highlights' in adjustments:
            self.highlights = adjustments['highlights']
        self.apply_highlights()
        if 'shadows' in adjustments:
            self.shadows = adjustments['shadows']
        self.apply_shadows()
        if 'zoom' in adjustments:
            self.zoom = adjustments['zoom']
        self.apply_zoom()
        # check if adjusted image has any pixels different than 0
        # if np.any(self.image):
        #     print("ADJUSTED IMAGE HAS PIXELS")
        # else: 
        #     print("ADJUSTED IMAGE HAS NO PIXELS!!!!!!!!")
        self.save_adjusted_image()

    def apply_brightness(self):
        adjusted_image = np.clip(self.image + self.brightness, 0, 255)
        self.image = adjusted_image

    def apply_contrast(self):
        # Ensure the contrast coefficient is within the valid range
        contrast_coefficient = np.clip(self.contrast, 0, 2)
        adjusted_image = (self.image - 128) * contrast_coefficient + 128
        adjusted_image = np.clip(adjusted_image, 0, 255).astype(np.int32)
        self.image = adjusted_image

    def apply_sharpness(self):
        # kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        # adjusted_image = cv2.filter2D(self.image, -1, kernel)
        # self.image = adjusted_image
        pass

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

    def apply_zoom(self):
        pass
    
    def print_current_settings(self):
        print(f"Brightness: {self.brightness}")
        print(f"Contrast: {self.contrast}")
        print(f"Sharpness: {self.sharpness}")
        print(f"Temperature: {self.temperature}")
        print(f"Saturation: {self.saturation}")
        print(f"Rotation: {self.rotation}")
        print(f"Fade: {self.fade}")
        print(f"Zoom: {self.zoom}")




