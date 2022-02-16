from django.urls import path
from toys.views import toy_list_view, toy_detail_view

app_name = "toys"

urlpatterns = [
    path("toys/", toy_list_view, name="toys_list"),
    path("toys/<int:pk>/", toy_detail_view, name="toy_detail"),
]
