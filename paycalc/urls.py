"""paycalc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from opt import views

urlpatterns = [
    path('', include('core.urls')),
    path('opt/', include('opt.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]

# from django.conf.urls import url
# from django.contrib import admin
# from django.conf.urls.static import static
# from django.conf import settings
#
# # путь импорта для удобных URL
# from django.urls import path
#
# # импортировать наши представления, чтобы urls.py мог их вызывать
# from opt.views import NoticesFeed
#
# urlpatterns = [
#     # Путь к корню нашего веб-сайта, который будет отображать ленту сообщений
#     path('', NoticesFeed.as_view(template_name="index.html"), name="NoticesFeed"),
#     url(r'^admin/', admin.site.urls),
# ]
#
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)