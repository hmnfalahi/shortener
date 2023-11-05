from django.urls import path

from api.views import LinkController


urlpatterns = [
    path('links/<str:short_url>', LinkController.as_view()),
    path('links/', LinkController.as_view()),
]

