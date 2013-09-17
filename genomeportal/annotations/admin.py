from django.contrib import admin

from genomeportal.annotations.models import *

class SequenceAdmin(admin.ModelAdmin):
    raw_id_fields = ('part_of', 'genes',)

admin.site.register(SequenceType)
admin.site.register(Sequence, SequenceAdmin)
admin.site.register(Organism)
admin.site.register(GeneMatch)
