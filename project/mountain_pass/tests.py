from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .serializers import PerevalSerializer
from .models import *


class MountainPassTestCase(APITestCase):

    def setUp(self):
        # создает первый объект модели Pereval
        self.perval_1 = Pereval.objects.create(
            user=AppUser.objects.create(
                email='mail@mail.ru',
                phone='+79009009090',
                fam='Иванов',
                name='Иван',
                otc='Иванович'
            ),
            beauty_title='beauty_title',
            title='title',
            other_title='other_title',
            connect='connect',
            coords=Coords.objects.create(
                latitude=22.222,
                longitude=11.111,
                height=2500
            ),
            level=Level.objects.create(
                winter='C2',
                summer='A1',
                autumn='B',
                spring='A2'
            )
        )
        # первое изображение для первого объкта Pereval
        self.image_1 = Image.objects.create(
            title='Some title',
            image='https://mountains.com/some_image',
            pereval=self.perval_1
        )

        # второе изображение для первого объкта Pereval
        self.image_2 = Image.objects.create(
            title='Some title 2',
            image='https://mountains.com/some_image2',
            pereval=self.perval_1
        )

        # создает второй объект модели Pereval
        self.perval_2 = Pereval.objects.create(
            user=AppUser.objects.create(
                email='mail@mail.ru',
                phone='+79009009090',
                fam='Иванов',
                name='Иван',
                otc='Иванович'
            ),
            beauty_title='beauty_title2',
            title='title2',
            other_title='other_title2',
            connect='connect2',
            coords=Coords.objects.create(
                latitude=33.222,
                longitude=22.111,
                height=1500
            ),
            level=Level.objects.create(
                winter='B',
                summer='A2',
                autumn='B',
                spring='A2'
            )
        )
        # первое изображение для второго объкта Pereval
        self.image_1 = Image.objects.create(
            title='Some title3',
            image='https://mountains.com/some_image3',
            pereval=self.perval_2
        )

        # второе изображение для второго объкта Pereval
        self.image_2 = Image.objects.create(
            title='Some title 4',
            image='https://mountains.com/some_image4',
            pereval=self.perval_2
        )

    def test_mountainPass_list(self):
        '''тестирует endpoint /perevals/ - список всех объектов модели Pereval'''

        responce = self.client.get(reverse('pereval-list'))
        serializer_data = PerevalSerializer([self.perval_1, self.perval_2], many=True).data

        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, responce.data)

    def test_mountainPass_detail(self):
        ''' проверяет endpoint /perevals/{pereval_id} - объекта Pereval по его id'''

        responce = self.client.get(reverse('pereval-detail', kwargs={'pk': self.perval_1.id}))
        serializer_data = PerevalSerializer(self.perval_1).data

        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, responce.data)

    def test_by_email(self):
        '''проверяет сбор всех объектов модели Pereval, отфильтрованных по user.email'''

        email = self.perval_1.user.email
        url = f'/perevals/?email={email}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
