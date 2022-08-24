

from django.urls import include, path
from . import views
from django.conf.urls.static import static  # new
from django.conf import settings  # new
urlpatterns = [
    path('', views.home, name='Login'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
  
]
if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)