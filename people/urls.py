from django.urls import include, path

import people.views

urlpatterns = [
    path("", people.views.index),
    path("naive", people.views.list_people_naive),
    path("select_related_only", people.views.list_people_select_related_only),
    path("select_related", people.views.list_people_select_related),
    path("qs_only", people.views.list_people_qs_only),
    path("values", people.views.list_people_values),
]
