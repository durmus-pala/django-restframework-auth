from django.shortcuts import HttpResponse
from .models import Student
from .serializers import StudentSerializer
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoObjectPermissions, DjangoModelPermissions
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from .permissions import IsAdminOrReadOnly, IsAddedByUserOrReadOnly
# Create your views here.
from rest_framework.response import Response
from rest_framework import status


def home(request):
    return HttpResponse('<h1>API Page</h1>')


class StudentList(generics.ListCreateAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    # permission_classes = [DjangoModelPermissions]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # print(request.headers)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.validated_data['user'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "created successfully"}, status=status.HTTP_201_CREATED, headers=headers)


class StudentOpr(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [IsAddedByUserOrReadOnly]
