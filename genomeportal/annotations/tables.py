from django.utils.safestring import mark_safe

import django_tables2 as tables
from django_tables2 import A

from genomeportal.annotations.models import Sequence

class SequenceTable(tables.Table):
    class Meta:
        model = Sequence
        fields = ('identifier', 'type',)
        attrs = {'class': 'table table-bordered table-striped'}

    identifier = tables.LinkColumn('annotation_details', args=[A('identifier')])
    type = tables.Column()
    gene = tables.Column(accessor=A('genes.all'), verbose_name='Gene', orderable=False)

    def render_gene(self, value):
        return mark_safe(u''.join([u'<div>{}</div>'.format(v.gene.symbol) for v in value]))
