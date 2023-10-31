from django.urls import path

from api.views import LinkController


urlpatterns = [
    path('links/', LinkController.as_view()),
]

