from django.urls import path
from toys.views import toy_list_view, toy_detail_view, toy_sql_view, toy_raw_sql_view

app_name = "toys"

urlpatterns = [
    path("toys/", toy_list_view, name="toys_list"),
    path("toys_sql/", toy_sql_view, name="toys_sql_list"),
    path("toys_raw/", toy_raw_sql_view, name="toys_raw_list"),
    path("toys/<int:pk>/", toy_detail_view, name="toy_detail"),
]
