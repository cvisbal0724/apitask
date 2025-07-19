"""
URL configuration for apitask project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from task.views import TaskViewSet, AuditTaskViewSet
from .custom_token import CustomTokenView

admin.autodiscover()
admin.site.site_header = 'Administrador de tareas'
admin.site.site_title = 'Administrador de tareas'
router = routers.DefaultRouter()

# routes
router.register(r'task', TaskViewSet)
router.register(r'audit-task', AuditTaskViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),    
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('o/token/', CustomTokenView.as_view(), name='token'),
	path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
