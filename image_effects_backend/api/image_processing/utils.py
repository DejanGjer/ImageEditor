# image_editor_backend/image_processing/utils.py

import cv2
import numpy as np

def adjust_image(image, adjustments):
    # Adjust brightness, contrast, and saturation
    brightness = adjustments.get('brightness', 0)
    contrast = adjustments.get('contrast', 0)
    saturation = adjustments.get('saturation', 0)

    # Convert image to HSV color space for saturation adjustment
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Apply adjustments
    hsv_image[:,:,2] = np.clip(hsv_image[:,:,2] + brightness, 0, 255)
    hsv_image[:,:,1] = np.clip(hsv_image[:,:,1] + contrast, 0, 255)
    hsv_image[:,:,1] = np.clip(hsv_image[:,:,1] * (1 + saturation / 100), 0, 255)

    # Convert back to BGR color space
    adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    return adjusted_image
