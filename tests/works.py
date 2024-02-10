import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import cv2
import numpy as np
from matplotlib import pyplot as plt

currentImage = None

def displayImage(displayImage):
    global currentImage
    # ImagetoDisplay = displayImage.resize((900,600), Image.ANTIALIAS)
    ImagetoDisplay = displayImage.resize((900,600))
    ImagetoDisplay = ImageTk.PhotoImage(ImagetoDisplay)
    showWindow.config(image=ImagetoDisplay)
    showWindow.photo_ref = ImagetoDisplay
    showWindow.pack()
    currentImage = displayImage

def importImage():
    global originalImage
    filename = filedialog.askopenfilename()
    originalImage = Image.open(filename)
    displayImage(originalImage)
    calculate_histogram()
    
def calculate_histogram():
    #global currentImage
    # Convert PIL Image to NumPy array
    if currentImage:
        image_np = np.array(currentImage)
        hist_Y = np.zeros(256)
        y = np.arange(256)
        total_pixels = image_np.shape[0] * image_np.shape[1]
    #A = image_np.astype(dtype='uint8')
        for i in range(image_np.shape[0]):
            for j in range(image_np.shape[1]):
                hist_Y[image_np[i,j]] = hist_Y[image_np[i,j]]+1
    
        hist_Y_normalized = hist_Y / total_pixels
        plt.bar(y, hist_Y_normalized)
        plt.title('Histogram')
        plt.show()

def refresh_filters():
    global currentImage
    displayImage(currentImage)
    brightnessSlider.set(1)
    contrastSlider.set(1)
    sharpnessSlider.set(2)
    temperatureSlider.set(0)
    saturationSlider.set(1)
    rotationSlider.set(0)
    fadeSlider.set(0)
    zoomSlider.set(1)
    calculate_histogram()
    
def brightness(brightness_pos):
    global currentImage
    brightness_pos = float(brightness_pos)
    enhancer = ImageEnhance.Brightness(originalImage)
    currentImage = enhancer.enhance(brightness_pos)
    displayImage(currentImage)

def contrast(contrast_pos):
    global currentImage
    contrast_pos = float(contrast_pos)
    # enhancer = ImageEnhance.Contrast(originalImage)
    # currentImage = enhancer.enhance(contrast_pos)

    adjusted_image = np.array(originalImage).astype(np.int32)
    print(adjusted_image.dtype)
    print(adjusted_image.shape)
    print(type(contrast_pos))
    adjusted_image = (adjusted_image - 128) * contrast_pos + 128
    adjusted_image = np.clip(adjusted_image, 0, 255)
    currentImage = Image.fromarray(adjusted_image.astype('uint8'))
    displayImage(currentImage)
    
def sharpness(sharpness_pos):
    global currentImage
    sharpness_pos = float(sharpness_pos)
    enhancer = ImageEnhance.Sharpness(originalImage)
    currentImage = enhancer.enhance(sharpness_pos)
    displayImage(currentImage)

def saturation(saturation_pos):
    global currentImage
    saturation_pos = float(saturation_pos)
    # Convert the image to the HSV color space
    img_hsv = originalImage.convert("HSV")

    # Split the image into hue, saturation, and value channels
    h, s, v = img_hsv.split()

    # Adjust the saturation channel
    s = s.point(lambda p: p * saturation_pos)

    # Merge the channels back to an HSV image
    img_hsv = Image.merge("HSV", (h, s, v))

    # Convert the HSV image back to RGB
    currentImage = img_hsv.convert("RGB")

    displayImage(currentImage)

# def saturation(value):
#     # Update saturation value and apply the filter
#     saturation_value = float(value)
#     filtered_image = apply_saturation_filter(saturation_value)

#     # Display the filtered image
#     displayImage(filtered_image) 
    
def temperature(temperature_pos):
    global currentImage
    temperature_pos = float(temperature_pos)
    # Convert the image to the RGB mode
    img_rgb = originalImage.convert("RGB")

    # Split the image into red, green, and blue channels
    r, g, b = img_rgb.split()

    # Adjust the color balance based on temperature
    r = r.point(lambda p: p * (1.0 + 0.01*temperature_pos))
    b = b.point(lambda p: p * (1.0 - 0.1*temperature_pos))

    # Merge the channels back to an RGB image
    currentImage = Image.merge("RGB", (r, g, b))

    displayImage(currentImage)

# def temperature(value):
#     # Update temperature value and apply the filter
#     temperature_value = float(value)
#     filtered_image = apply_temperature_filter(temperature_value)

#     # Display the filtered image
#     displayImage(filtered_image)
    
def rotation(angle):
    global currentImage
    currentImage = originalImage.rotate(int(angle))
    displayImage(currentImage)
    
def fade(fade_pos):
    global currentImage
    fade_pos = float(fade_pos)
    background = Image.new('RGB', originalImage.size, (255, 255, 255))
    currentImage = Image.blend(originalImage, background, fade_pos / 255)
    displayImage(currentImage)

def zoom(zoom_factor):
    global currentImage
    zoom_factor = float(zoom_factor)
    # Get image dimensions
    width, height = originalImage.size

    # Calculate new dimensions after zooming
    new_width = int(width / zoom_factor)
    new_height = int(height / zoom_factor)

    # Calculate the center of the image
    center_x, center_y = width // 2, height // 2

    # Calculate the top-left corner of the zoomed region
    top_left_x = max(0, center_x - new_width // 2)
    top_left_y = max(0, center_y - new_height // 2)

    # Calculate the bottom-right corner of the zoomed region
    bottom_right_x = min(width, center_x + new_width // 2)
    bottom_right_y = min(height, center_y + new_height // 2)

    # Crop and resize the zoomed region
    zoomed_image = originalImage.crop((top_left_x, top_left_y, bottom_right_x, bottom_right_y))
    currentImage = zoomed_image.resize((width, height), Image.ANTIALIAS)

    displayImage(currentImage)    

def vignette(strength):
    global currentImage
    strength = float(strength)
    image = np.array(originalImage)
    
    kernel_x = cv2.getGaussianKernel(image.shape[1], strength)
    kernel_y = cv2.getGaussianKernel(image.shape[0], strength)
    kernel = kernel_y * kernel_x.T
    
    kernel = kernel / np.linalg.norm(kernel)
    mask = kernel*255
    output = np.copy(image)
    mask_imposed = mask[:image.shape[0], :image.shape[1]]

    # Apply the modified strength to the mask and each channel
    for i in range(3):
        output[:, :, i] = output[:, :, i] * mask_imposed
    
    currentImage = Image.fromarray(output.astype('uint8'))
    
    displayImage(currentImage)
    
window = tk.Tk()
window.geometry("1000x800")
window.title("DIY Instagram Editor")
window.config(bg="white")

Frame1 = tk.Frame(window, width=400, height=800, bg="white")
Frame1.pack(side="left", fill="y")

image_button = tk.Button(Frame1, text="Open Image", command=importImage, bg="white")
image_button.pack(padx=35, pady=10)

brightnessSlider = tk.Scale(Frame1, label="Brightness", from_=0, to=2, orient=tk.HORIZONTAL, resolution=0.1,
                            command=brightness)
brightnessSlider.set(1)
brightnessSlider.pack(anchor=tk.N)

contrastSlider = tk.Scale(Frame1, label="Contrast", from_=0, to=2, orient=tk.HORIZONTAL, resolution=0.1,
                          command=contrast)
contrastSlider.set(1)
contrastSlider.pack(anchor=tk.N)

sharpnessSlider = tk.Scale(Frame1, label="Sharpness", from_=0, to=4, orient=tk.HORIZONTAL, resolution=0.1,
                            command=sharpness)
sharpnessSlider.set(2)
sharpnessSlider.pack(anchor=tk.N)

temperatureSlider = tk.Scale(Frame1, label="Warmth", from_=-2, to=2, orient="horizontal", resolution=0.1,
                              command=temperature)
temperatureSlider.set(0)
temperatureSlider.pack(anchor=tk.N)

saturationSlider = tk.Scale(Frame1, label="Saturation", from_=0, to=2, resolution=0.01, orient="horizontal",
                              command=saturation)
saturationSlider.set(1)
saturationSlider.pack(anchor=tk.N)

rotationSlider = tk.Scale(Frame1, label="Rotation", from_=-25, to=25, orient="horizontal",
                              command=rotation)
rotationSlider.set(0)
rotationSlider.pack(anchor=tk.N)

fadeSlider = tk.Scale(Frame1, label="Fade", from_=0, to=100, orient="horizontal",
                              command=fade)
fadeSlider.set(0)
fadeSlider.pack(anchor=tk.N)

# shadowSlider = tk.Scale(Frame1, label="Shadows", from_=0, to=1, resolution=0.01, orient="horizontal",
#                               command=shadow)
# shadowSlider.set(0.5)
# shadowSlider.pack(anchor=tk.N)

zoomSlider = tk.Scale(Frame1, label="Zoom", from_=1, to=10, orient="horizontal", command=zoom)
zoomSlider.set(1)
zoomSlider.pack(anchor=tk.N)

vignetteSlider = tk.Scale(Frame1, label="Vignette", from_=140, to=200, orient="horizontal", command=vignette)
vignetteSlider.set(170)
vignetteSlider.pack(anchor=tk.N)

refresh_button = tk.Button(Frame1, text="Refresh", command=refresh_filters, bg="white")
refresh_button.pack(padx=35, pady=10)

showWindow = tk.Label(window)
showWindow.pack()
tk.mainloop()
