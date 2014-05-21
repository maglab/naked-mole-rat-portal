from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('genomeportal.annotations.views',
    url(r'^/$', 'results'),
    url(r'^/results/genage/$', 'genage', name='in_genage'),
    url(r'^/results/$', 'results', name='annotation_results'),
    url(r'^/details/alignments/(?P<identifier>.*)/$', 'alignments', name='alignments'),
    url(r'^/details/(?P<identifier>.*)/raw/$', 'raw_sequence', name='raw_sequence'),
    url(r'^/details/(?P<identifier>.*)/$', 'details', name='annotation_details'),
    url(r'^/about/$', TemplateView.as_view(template_name='about_annotations.jade'), name='about_annotations'),
)
