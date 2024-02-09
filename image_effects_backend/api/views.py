# image_editor_backend/api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import JSONParser
from .image_processing.utils import adjust_image
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

ORIGINAL_IMAGE_PATH = './api/static/img/lena.tif'
IMAGE_PATH = './api/static/img/lena_adjusted.jpg'

class AdjustImageView(APIView):
    parser_classes = [JSONParser]

    def get(self, request, format=None):
        print("Get request received")
        if os.path.exists(IMAGE_PATH):
            with open(IMAGE_PATH, 'rb') as image_file:
                file = image_file.read()
                return HttpResponse(file, content_type="image/png")
        else:
            return HttpResponse(status=404)

    def post(self, request, format=None):
        print("Post request received")
        print(request.data)
        brightness = request.data.get('brightness', 0)
        print(brightness)
        image = plt.imread(ORIGINAL_IMAGE_PATH).astype(np.int32)
        print(image.shape)
        # brightness_factor = 1.0 + (brightness / 100.0)
        # Increase the brightness
        adjusted_image = np.clip(image + brightness, 0, 255).astype(np.uint8)
        adjusted_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2RGB)
        print(adjusted_image.shape)
        adjusted_image_path = IMAGE_PATH
        cv2.imwrite(adjusted_image_path, adjusted_image)

        if os.path.exists(adjusted_image_path):
            with open(adjusted_image_path, 'rb') as image_file:
                file = image_file.read()
                return HttpResponse(file, content_type="image/png")
        else:
            return HttpResponse(status=404)

        #OLD CODE
        # image_file = request.FILES.get('image')
        # adjustments = request.data

        # # Read the image
        # image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), -1)

        # # Apply adjustments
        # adjusted_image = adjust_image(image, adjustments)

        # # Convert the processed image to bytes
        # _, buffer = cv2.imencode('.jpg', adjusted_image)
        # processed_image = buffer.tobytes()


        # processed_image = "Hello World"

        # return Response({'processed_image': processed_image})

class HistogramDataView(APIView):
    parser_classes = [JSONParser]

    def histogram(self, X):
        hist_x = np.zeros(256)
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                hist_x[X[i,j]] += 1
        return hist_x
    
    def standard(self, mat):
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                if(mat[i,j]>255):
                    mat[i,j]=255
                if(mat[i,j]<0):
                    mat[i,j]=0
        return mat.astype(np.uint8)

    def get(self, request, format=None):
        print("Get request received for histogram data")
        image = None
        if os.path.exists(IMAGE_PATH):
            image = plt.imread(IMAGE_PATH)
        else: 
            image = plt.imread(ORIGINAL_IMAGE_PATH)
        if len(image.shape) > 2:
            image = np.sum(image, axis=2) / 3
        # convert image to greyscale if it is not already
        image = self.standard(image)
        histogram_data = self.histogram(image)
        # print(histogram_data)
        return Response({'histogram_data': histogram_data})