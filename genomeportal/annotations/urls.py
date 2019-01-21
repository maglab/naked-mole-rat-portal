from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^/$', views.results),
    url(r'^/results/genage/$', views.genage, name='in_genage'),
    url(r'^/results/$', views.results, name='annotation_results'),
    url(r'^/details/alignments/(?P<identifier>.*)/$', views.alignments, name='alignments'),
    url(r'^/details/(?P<identifier>.*)/raw/$', views.raw_sequence, name='raw_sequence'),
    url(r'^/details/(?P<identifier>.*)/$', views.details, name='annotation_details'),
    url(r'^/about/$', TemplateView.as_view(template_name='about_annotations.jade'), name='about_annotations'),
]
