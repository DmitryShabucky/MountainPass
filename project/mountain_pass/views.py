from rest_framework import viewsets, status
from rest_framework.response import Response


from .models import Pereval, AppUser, Coords, Level, Image
from .serializers import PerevalSerializer, CoordsSerializer, LevelSerializer, ImageSerializer, AppUserSerializer


class PerevalViewset(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    filterset_fields = ('user__email',)

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

    def partial_update(self, request, *args, **kwargs):
        '''проводит проверку статуса модели Pereval при её изменении'''

        instance = self.get_object()
        serializer = PerevalSerializer(instance, data=request.data, partial=True)

        if request.data['status'] == 'NEW':
            if serializer.is_valid():
                serializer.save()
                response = {
                    'state': 1,
                    'message': 'Успешное изменение данных.'
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'state': 0,
                    'message': 'Данные о пользователе менять нельзя!'
                }
                return Response(response, status=status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS)
        else:
            response = {
                'state': 0,
                'message': 'Ошибка. Данные проходят модерацию.'
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)

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
