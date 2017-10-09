from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'accelo'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^arb$', views.arb, name='arb'),
    url(r'^arbit$', views.arbit, name='arbit'),
    url(r'^push$', views.push, name='push'),
    url(r'^calib$', views.calib, name='calib'),
    url(r'^classify$', views.classify, name='classify'),
    url(r'^calibrat$', views.calibrat, name='calibrat'),
    url(r'^plot$', views.plot, name='plot'),
    url(r'^value$', views.value, name='value'),
    url(r'^delete$', views.delete, name='delete'),
    url(r'^dele$', views.dele, name='dele'),
     url(r'^saveit$', views.saveit, name='saveit'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


