from django.urls import path

from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
        #Leave as empty string for base url
	path('', views.home, name="home"),
	path('login/', auth_view.LoginView.as_view(template_name='store/login.html'), name="login"),
	path('logout/', auth_view.LogoutView.as_view(template_name='store/logout.html'), name="logout"),
	path('register/', views.register, name="register"),
	path('shop/', views.shop, name="shop"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	

]