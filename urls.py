from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('Login.html', views.Login, name="Login"), 
	       path('AdminLogin.html', views.AdminLogin, name="AdminLogin"), 
	       path('Register.html', views.Register, name="Register"),
	       path('Signup', views.Signup, name="Signup"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path('AdminLoginAction', views.AdminLoginAction, name="AdminLoginAction"),
	       path('ScrapeWeb.html', views.ScrapeWeb, name="ScrapeWeb"),
	       path('ScrapeWebAction', views.ScrapeWebAction, name="ScrapeWebAction"),	  
	       path('ViewMagicbrick', views.ViewMagicbrick, name="ViewMagicbrick"),	 
	       path('ViewNoBroker', views.ViewNoBroker, name="ViewNoBroker"),	 
]