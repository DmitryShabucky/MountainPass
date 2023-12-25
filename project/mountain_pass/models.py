from django.db import models


class AppUser(models.Model):
    email = models.EmailField(max_length=150, verbose_name="Почта")
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    fam = models.CharField(max_length=20, verbose_name='Фамилия')
    name = models.CharField(max_length=20, verbose_name='Имя')
    otc = models.CharField(max_length=20, verbose_name='Отчество')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.fam} {self.name} {self.otc}'


class Pereval(models.Model):

    new = 'NEW'
    pending = 'PND'
    accepted = 'ACT'
    rejected = 'RJT'

    POSITIONS = [
        (new, 'Новое'),
        (pending, 'Принято в работу'),
        (accepted, 'Одобрено'),
        (rejected, 'Отклонено')
    ]

    beauty_title = models.CharField(max_length=100, null=False, blank=False, verbose_name="Название перевала")
    title = models.CharField(max_length=100, verbose_name="Местность")
    other_title = models.CharField(max_length=100, verbose_name="Округ")
    connect = models.TextField(blank=True, verbose_name="Что соединяет")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    status = models.CharField(max_length=3, choices=POSITIONS, default='NEW', verbose_name="Статус проверки")
    level = models.OneToOneField('Level', on_delete=models.CASCADE, verbose_name="Уровень", related_name="level")
    coords = models.OneToOneField('Coords', on_delete=models.CASCADE, verbose_name="Координаты", related_name='coords')

    class Meta:
        verbose_name = 'Перевал'
        verbose_name_plural = 'Перевалы'

    def __str__(self):
        return f'{self.beauty_title}, {self.title}, {self.other_title}.'


class Coords(models.Model):
    latitude = models.FloatField(max_length=10, blank=True, verbose_name='Широта')
    longitude = models.FloatField(max_length=10, blank=True, verbose_name="Долгота")
    height = models.IntegerField(blank=True, verbose_name='Высота')

    class Meta:
        verbose_name = 'Координат'
        verbose_name_plural = 'Координаты'
    def __str__(self):
        return f'{self.coords}'


class Level(models.Model):
    very_easy = 'A1'
    easy = 'A2'
    middle = 'B'
    rough = 'C1'
    very_rough = 'C2'

    POSITIONS = [
        (very_easy, 'Очень легко'),
        (easy, 'Легко'),
        (middle, 'Средне'),
        (rough, 'Сурово'),
        (very_rough, 'Очень сурово')
    ]

    winter = models.CharField(max_length=2, blank=True, choices=POSITIONS, verbose_name="Зимой")
    summer = models.CharField(max_length=2, blank=True, choices=POSITIONS, verbose_name="Летом")
    autumn = models.CharField(max_length=2, blank=True, choices=POSITIONS, verbose_name="Осенью")
    spring = models.CharField(max_length=2, blank=True, choices=POSITIONS, verbose_name="Весной")

    class Meta:
        verbose_name = 'Уровень'
        verbose_name_plural = 'Уровни'

    def __str__(self):
        return f'{self.level}'


class Image(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, verbose_name="Перевал", related_name='images')
    title = models.CharField(max_length=50, blank=True, null=True, verbose_name="Пометка")
    image = models.TextField(blank=False, null=True, verbose_name="Ссылка на изображение")

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return f'{self.pereval}'
