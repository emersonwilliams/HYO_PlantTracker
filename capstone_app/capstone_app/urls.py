from django.contrib import admin
from django.urls import path, include
from plant_tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('plant_tracker.urls')),
]
