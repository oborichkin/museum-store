from django.db import models
from django.contrib.auth.models import User
from .validators import validate_exec, validate_order_status

# TODO: Добавить unique_together


class Molding(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    slug = models.SlugField(max_length=15, verbose_name='Имя CSS класса')
    price = models.FloatField(verbose_name='Цена (за метр)')
    width = models.IntegerField(verbose_name='Ширина (мм)')
    image = models.ImageField(upload_to='molding', verbose_name='Изображение')
    widthImage = models.IntegerField(verbose_name='Ширина рамки в изображении')
    thumbnail = models.ImageField(
        upload_to='molding/thumbnail', verbose_name='Предпросмотр')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Багет'
        verbose_name_plural = 'Багеты'


class Author(models.Model):
    name = models.CharField(max_length=60, verbose_name='Имя')
    slug = models.SlugField(max_length=60, verbose_name='URL Автора')
    logo = models.ImageField(upload_to='authors', verbose_name='Логотип')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    @models.permalink
    def get_absolute_url(self):
        return 'museum:author-paintings', None, {'slug': self.slug}


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    slug = models.SlugField(max_length=15, verbose_name='URL Категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Style(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    slug = models.SlugField(max_length=15, verbose_name='URL Направления')
    logo = models.ImageField(upload_to='styles', verbose_name='Логотип')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'

    @models.permalink
    def get_absolute_url(self):
        return 'museum:style-paintings', None, {'slug': self.slug}


class Service(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название услуги')
    price = models.FloatField(verbose_name='Цена (за кв. м)')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Доп. Услуга'
        verbose_name_plural = 'Доп. Услуги'


class Painting(models.Model):
    name = models.CharField(max_length=60, verbose_name='Название')
    slug = models.SlugField(max_length=30, verbose_name='URL')
    description = models.TextField(
        verbose_name='Описание картины', blank=True, null=True)
    year = models.IntegerField(null=True, verbose_name='Год')
    # TODO: null в авторе, направлении, категории?
    author = models.ForeignKey(
        'Author', null=True, verbose_name='Автор', on_delete=models.SET_NULL)
    style = models.ForeignKey(
        'Style', null=True, verbose_name='Направление',
        on_delete=models.SET_NULL)
    category = models.ForeignKey(
        'Category', null=True, verbose_name='Категория',
        on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='paintings',
                              verbose_name='Изображение (~228x228)')
    full_image = models.ImageField(
        upload_to='paintings', verbose_name='Полное изображение')
    width = models.FloatField()
    aspect_ratio = models.FloatField()

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'museum:item', None, {'slug': self.slug}

    class Meta:
        verbose_name = 'Картина'
        verbose_name_plural = 'Картины'


class Item(models.Model):
    owner = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    painting = models.ForeignKey(Painting, on_delete=models.CASCADE)
    molding = models.ForeignKey(
        Molding, null=True, default=None, on_delete=models.SET_NULL)
    width = models.FloatField(null=False)
    height = models.FloatField(null=False)
    execution = models.CharField(
        null=False, default='canvas', max_length=16,
        validators=[validate_exec])
    lacquer = models.BooleanField(null=False, default=False)
    struc_gel = models.BooleanField(null=False, default=False)
    # Если order_id равен null, значит товар в корзине
    order_id = models.ForeignKey('Order', null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.painting.name + " " + \
            str(self.width) + "x" + str(self.height)


class Order(models.Model):
    id = models.AutoField(primary_key=True)

    order_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    first_name = models.CharField(null=False, max_length=64)
    last_name = models.CharField(null=False, max_length=64)
    patronymic = models.CharField(null=True,  max_length=64)
    phone_num = models.CharField(null=False, max_length=32)
    email = models.EmailField(null=True)
    country = models.CharField(null=False, max_length=64)
    region = models.CharField(null=False, max_length=128)
    city = models.CharField(null=False, max_length=96)
    street = models.CharField(null=False, max_length=64)
    house = models.CharField(null=False, max_length=64)
    flat = models.CharField(null=False, max_length=64)
    index = models.CharField(null=False, max_length=32)

    order_status = models.CharField(
        null=False, default='processing', max_length=16)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    @models.permalink
    def get_absolute_url(self):
        return 'museum:order', None, {'pk': self.pk}

    def __str__(self):
        return "Заказ №" + str(self.id)
