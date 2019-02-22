import os

from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.utils.functional import curry
from django.views.defaults import *
from genomeportal import views as genomeViews
from genomeportal.annotations import urls
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', genomeViews.index, name='index'),
    url(r'^about$', TemplateView.as_view(template_name='about.pug')),
    url(r'^gene_expression$', TemplateView.as_view(template_name='gene_expression.pug')),
    url(r'^downloads$', TemplateView.as_view(template_name='downloads.pug')),
    url(r'^annotations', include(urls)),
    url(r'^admin', admin.site.urls),
              ] + static('/jbrowse/', document_root=os.path.join(settings.PROJECT_ROOT, 'jbrowse'))

handler404 = curry(page_not_found, template_name='404.pug')
handler500 = curry(server_error, template_name='500.pug')

