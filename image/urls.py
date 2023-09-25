from django.urls import path 
from image import views

app_name = 'image'

urlpatterns = [
    path('create/', views.ImageView.as_view(), name='image_create'),
    path('detail/<int:pk>/<slug:slug>/', views.ImageDetailView.as_view(), name='image_detail'),
]
