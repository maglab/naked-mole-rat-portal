from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'genomeportal.views.index'),
    url(r'^about/$', TemplateView.as_view(template_name='about.jade')),
    url(r'^gene_expression/$', TemplateView.as_view(template_name='gene_expression.jade')),
    url(r'^downloads/$', TemplateView.as_view(template_name='downloads.jade')),
    url(r'^annotations', include('genomeportal.annotations.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
