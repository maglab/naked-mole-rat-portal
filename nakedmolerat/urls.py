from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', 'nakedmolerat.views.home', name='home'),
    url(r'^$', TemplateView.as_view(template_name='index.jade')),
    url(r'^about/$', TemplateView.as_view(template_name='about.jade')),
    url(r'^gene_expression/$', TemplateView.as_view(template_name='gene_expression.jade')),
    url(r'^downloads/$', TemplateView.as_view(template_name='downloads.jade')),
    url(r'^annotations', include('nakedmolerat.annotations.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
