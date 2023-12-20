from rest_framework import viewsets, status
from rest_framework.response import Response


from .models import Pereval, AppUser, Coords, Level, Image
from .serializers import PerevalSerializer, CoordsSerializer, LevelSerializer, ImageSerializer, AppUserSerializer


class PerevalViewset(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

    def create(self, request, *args, **kwargs):

        serializer = PerevalSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response = {
                'status': 200,
                'message': '',
                'id': serializer.data.get('id')
            }
        elif status.HTTP_500_INTERNAL_SERVER_ERROR:
            response = {
                'status': 500,
                'message': 'Ошибка подключения к базе данных',
                'id': serializer.data.get('id')
            }
        elif status.HTTP_400_BAD_REQUEST:
            response = {
                'status': 400,
                'message': 'Неверный запрос',
                'id': serializer.data.get('id')
            }
        return Response(response)

class AppUserViewset(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer

class CoordsViewset(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer

class LevelViewset(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

class ImageViewset(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
