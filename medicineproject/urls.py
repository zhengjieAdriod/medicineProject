"""medicineproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from medicineproject import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('medicine.urls')),
]
# 在开发模式下,为了实现从数据库中拿到的图片路径可以直接访问
if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # 参数1,决定了在admin节目, 点击图片时,直接方法的地址为端口号之后, 直接拼接/media
    # 参数2,告诉系统,文件的实际位置
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
