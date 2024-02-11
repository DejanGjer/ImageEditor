# image_editor_backend/api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import JSONParser
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from .utils.image_processing import ImageProcessing

processing = ImageProcessing()

class AdjustImageView(APIView):
    parser_classes = [JSONParser]

    def get(self, request, format=None):
        print("Get request received")
        # asking for the original image is same as resetting the image
        processing.initialize_settings()
        if os.path.exists(processing.get_original_image_path()):
            with open(processing.get_original_image_path(), 'rb') as image_file:
                file = image_file.read()
                return HttpResponse(file, content_type="image/png")
        else:
            return HttpResponse(status=404)

    def post(self, request, format=None):
        print("Post request received")
        processing.adjust_image(request.data)
        if os.path.exists(processing.get_adjusted_image_path()):
            with open(processing.get_adjusted_image_path(), 'rb') as image_file:
                try:
                    file = image_file.read()
                    return HttpResponse(file, content_type="image/png")
                except IOError as message:
                    print(f"IOError while loading image - continuing to load image")
        else:
            return HttpResponse(status=404)

class HistogramDataView(APIView):
    parser_classes = [JSONParser]

    def histogram(self, X):
        return np.bincount(X.ravel(), minlength=256)
    
    def standard(self, mat):
        return np.clip(mat, 0, 255).astype(np.uint8)

    def get(self, request, format=None):
        print("Get request received for histogram data")
        image = None
        if os.path.exists(processing.get_adjusted_image_path()):
            image = plt.imread(processing.get_adjusted_image_path())
        else: 
            image = plt.imread(processing.get_original_image_path())
        # convert image to greyscale if it is not already
        if len(image.shape) > 2:
            image = np.sum(image, axis=2) // 3
        image = self.standard(image)
        histogram_data = self.histogram(image)
        return Response({'histogram_data': histogram_data})