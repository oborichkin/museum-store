from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import *

app_name = 'museum'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegistrationView.as_view(), name='register'),
    url(r'^authors/$', AuthorListView.as_view(), name='authors'),
    url(r'^authors/(?P<slug>[^\.]+)/$', AuthorPaintingsListView.as_view(), name='author-paintings'),
    url(r'^styles/$', StylesListView.as_view(), name='styles'),
    url(r'^styles/(?P<slug>[^\.]+)/$', StylePaintingsListView.as_view(), name='style-paintings'),
    url(r'^store/$', StoreView.as_view(), name='store'),
    url(r'^item/(?P<slug>[^\.]+)/$', ItemView.as_view(), name='item'),
    url(r'^cart/$', login_required(CartView.as_view()), name='cart'),
    url(r'^cart/item/(?P<pk>[^\.]+)/delete$', login_required(DeleteItem.as_view()), name='delete-item'),
    url(r'^cart/create_order/$', login_required(CreateOrder.as_view()), name='create-order'),
    url(r'^orders/$', login_required(OrderListView.as_view()), name='orders'),
    url(r'^orders/order/(?P<pk>[^\.]+)/$', login_required(OrderView.as_view()), name='order'),
]