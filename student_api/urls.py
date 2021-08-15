from django.urls import path
from .views import home, StudentList, StudentOpr

urlpatterns = [
    path('', home),
    path('student/', StudentList.as_view()),
    path('student/<int:pk>/', StudentOpr.as_view(), name="detail"),
]
