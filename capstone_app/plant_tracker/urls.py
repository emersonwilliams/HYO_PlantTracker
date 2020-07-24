from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # ex: /add-plant
    path('add-plant', views.addplant, name='addplant'),
    # ex: /my-plants
    path('my-plants', views.myplants, name='myplants'),
    # ex: /my-plants/sunny-the-sunflower
    path('my-plants/<int:plant_id>/', views.plantdetail, name='plant-detail')
    # NOTE: the above assumes we're taking in a key-word called plant-id
]

