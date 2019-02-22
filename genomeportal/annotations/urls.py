from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib import admin
from . import views
admin.autodiscover()
#app_name = 'annotations'
urlpatterns = [
    url(r'^$', views.results),
    url(r'^results/genage/$', views.genage, name='in_genage'),
    url(r'^results/$', views.results, name='annotation_results'),
    url(r'^details/alignments/(?P<identifier>.*)/$', views.alignments, name='alignments'),
    url(r'^details/(?P<identifier>.*)/raw/$', views.raw_sequence, name='raw_sequence'),
    url(r'^details/(?P<identifier>.*)/$', views.details, name='annotation_details'),
    url(r'^about/$', TemplateView.as_view(template_name='about_annotations.pug'))
]
