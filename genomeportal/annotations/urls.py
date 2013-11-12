from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('genomeportal.annotations.views',
    #url(r'^/$', TemplateView.as_view(template_name='search.jade')),
    url(r'^/$', 'results'),
    url(r'^/results/$', 'results', name='annotation_results'),
    url(r'^/details/(?P<identifier>.*)/$', 'details', name='annotation_details'),
    url(r'^/detail/(?P<identifier>.*)/raw/$', 'raw_sequence', name='raw_sequence'),
    url(r'^/about/$', TemplateView.as_view(template_name='about_annotations.jade'), name='about_annotations'),
)
