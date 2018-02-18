from django.views.generic import TemplateView, ListView, DetailView, View, DeleteView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from . import models
from .forms import UserRegistrationForm, UserLoginForm, CreateOrderForm


# TODO: Подумать над хлебными крошками, чтобы не хардкодить УРЛ каждый раз

class MyListView(ListView):
    ordering_list = None
    default_ordering = None

    def get_ordering(self):
        ordering = self.request.GET.get('sort')
        if (ordering is None) or (ordering not in self.ordering_list):
            ordering = self.default_ordering
        return ordering

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['sort'] = self.get_ordering()
        return context


class IndexView(TemplateView):
    template_name = "museum/index.html"


class StylesListView(MyListView):
    template_name = "museum/styles.html"
    context_object_name = 'styles'
    paginate_by = 6
    ordering_list = ['name']
    default_ordering = ordering_list[0]

    def get_context_data(self, **kwargs):
        context = super(StylesListView, self).get_context_data(**kwargs)
        context['breadscrumbs'] = {'магазин': '#',
                                   'стили': '#'}
        return context

    def get_queryset(self):
        return models.Style.objects.order_by(self.get_ordering())


class StylePaintingsListView(MyListView):
    template_name = "museum/store.html"
    context_object_name = 'paintings'
    ordering_list = ['name', 'year']
    default_ordering = ordering_list[0]
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(StylePaintingsListView,
                        self).get_context_data(**kwargs)
        style = models.Style.objects.get(slug=self.kwargs['slug'])
        context['breadscrumbs'] = {'магазин': "#",
                                   'стили': '/styles',
                                   style.name: '#', }
        return context

    def get_queryset(self):
        return models.Painting.objects.filter(style__slug=self.kwargs['slug']).order_by(self.get_ordering())


class AuthorListView(MyListView):
    template_name = "museum/authors.html"
    context_object_name = 'authors'
    paginate_by = 10
    ordering_list = ['name']
    default_ordering = ordering_list[0]

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['breadscrumbs'] = {'магазин': "#",
                                   'художники': '/authors', }
        return context

    def get_queryset(self):
        return models.Author.objects.order_by(self.get_ordering())


class AuthorPaintingsListView(MyListView):
    template_name = "museum/store.html"
    context_object_name = 'paintings'
    paginate_by = 10
    ordering_list = ['name', 'year']
    default_ordering = ordering_list[0]

    def get_context_data(self, **kwargs):
        context = super(AuthorPaintingsListView,
                        self).get_context_data(**kwargs)
        author = models.Author.objects.get(slug=self.kwargs['slug'])
        context['breadscrumbs'] = {'магазин': "#",
                                   'художники': '/authors',
                                   author.name: '#', }
        return context

    def get_queryset(self):
        return models.Painting.objects.filter(author__slug=self.kwargs['slug']).order_by(self.get_ordering())


class StoreView(TemplateView):
    template_name = "museum/store.html"


# TODO: Хлебные крошки для картин
class ItemView(DetailView):
    template_name = "museum/item.html"
    model = models.Painting

    # add item to cart
    def post(self, request, slug):
        if not request.user.is_authenticated():
            return redirect('museum:login')
        item = models.Item()
        item.owner = request.user
        item.painting = models.Painting.objects.get(
            slug=request.POST['painting'])
        if request.POST['size'] == 'own':
            item.width = request.POST['width']
            item.height = request.POST['height']
        else:
            item.width = request.POST['size']
            item.height = float(item.width) * float(item.painting.aspect_ratio)
        item.execution = request.POST['execution']
        if item.execution == 'molding':
            item.molding = models.Molding.objects.get(
                slug=request.POST['molding'])
        item.lacquer = ('lacquer' in request.POST.keys())
        item.struc_gel = ('struc_gel' in request.POST.keys())
        item.save()
        return redirect(item.painting.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super(ItemView, self).get_context_data(**kwargs)
        context['moldings'] = models.Molding.objects.all()
        return context


class CartView(MyListView):
    template_name = "museum/cart.html"
    context_object_name = 'items'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['breadscrumbs'] = {'магазин': "/styles",
                                   'корзина': '#'}
        return context

    def get_queryset(self):
        return models.Item.objects.filter(owner=self.request.user)


class DeleteItem(DeleteView):
    model = models.Item
    success_url = reverse_lazy("museum:cart")


class OrderListView(MyListView):
    template_name = "museum/orders.html"
    context_object_name = 'orders'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['breadscrumbs'] = {'магазин': "/styles",
                                   'корзина': '/cart',
                                   'заказы': '#'}
        return context

    def get_queryset(self):
        return models.Order.objects.filter(owner=self.request.user)


# TODO: Хлебные крошки?
class OrderView(DetailView):
    template_name = "museum/order.html"
    model = models.Order


# TODO: вставить адрес страницы заказов
# TODO: проверка привилегий
class CreateOrder(View):
    form_class = CreateOrderForm
    template_name = "museum/create_order.html"

    # display blank form
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('museum:login')
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.owner = User.objects.get(username=request.user.username)
            order.save()
            return redirect('museum:cart')

        return render(request, self.template_name, {'form': form})


class LoginView(View):
    form_class = UserLoginForm
    template_name = "museum/login.html"

    # display blank form
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('museum:index')
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('museum:index')

        form = self.form_class(request.POST)
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('museum:index')


class RegistrationView(View):
    form_class = UserRegistrationForm
    template_name = "museum/registration.html"

    # display blank form
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('museum:index')
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('museum:index')

        return render(request, self.template_name, {'form': form})
