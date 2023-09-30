from django.urls import path 
from image import views

app_name = 'image'

urlpatterns = [
    path('create/', views.ImageView.as_view(), name='image_create'),
    path('detail/<int:pk>/<slug:slug>/', views.ImageDetailView.as_view(), name='image_detail'),
    path('like/', views.ImageLikeView.as_view(), name='image_like'),
    path('list/', views.ImageListView.as_view(), name='image_list'),
    path('ranking/', views.ImageRankingView.as_view(), name='image_ranking'),
]
