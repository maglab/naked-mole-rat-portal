from django.contrib import admin

from genomeportal.annotations.models import *

admin.site.register(SequenceType)
admin.site.register(Sequence)
admin.site.register(Organism)
