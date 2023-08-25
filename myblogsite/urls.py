from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('programs/', include('programs.urls')),
    path('', views.homepage, name="homepage")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
