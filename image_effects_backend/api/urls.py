# image_editor_backend/api/urls.py

from django.urls import path
from .views import AdjustImageView, HistogramDataView

urlpatterns = [
    path('adjust-image/', AdjustImageView.as_view(), name='adjust_image'),
    path('histogram-data/', HistogramDataView.as_view(), name='histogram_data'),
]
