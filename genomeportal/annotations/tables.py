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
    gene = tables.Column(accessor=A('identifier'), verbose_name='Gene/miRNA', orderable=False)

    def render_gene(self, value):
        if record.mirna_set.count() > 0:
            output = u''.join([u'<div>{}</div>'.format(v.identifier) for v in record.mirna_set.all()])
        else:
            output = u''.join([u'<div>{} <small>({})</small></div>'.format(v.gene.symbol, v.gene.organism.common_name) for v in record.genes.all()])
        return mark_safe(output)
