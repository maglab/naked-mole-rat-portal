from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

import django_tables2 as tables
from django_tables2 import A
from django_tables2.rows import BoundRows, BoundRow

from genomeportal.annotations.models import Sequence

class HighlightBoundRows(BoundRows):
    def __iter__(self):
        for record in self.data:
            row = BoundRow(record, table=self.table)
            if record.has_genes or (record.part_of is not None and record.part_of.has_genes):
                row.style = 'highlight'
            yield row

    def __getitem__(self, key):
        container = HighlightBoundRows if isinstance(key, slice) else BoundRow
        return container(self.data[key], table=self.table)

class SequenceTable(tables.Table):
    class Meta:
        model = Sequence
        fields = ('identifier', 'type',)
        attrs = {'class': 'table table-bordered table-striped'}

    identifier = tables.LinkColumn('annotation_details', args=[A('identifier')], verbose_name='Identifier')
    type = tables.Column(verbose_name='Type', orderable=False)
    gene = tables.Column(accessor=A('identifier'), verbose_name='Matches', orderable=False)

    def __init__(self, *args, **kwargs):
        super(SequenceTable, self).__init__(*args, **kwargs)
        self.rows = HighlightBoundRows(data=self.data, table=self)

    def render_gene(self, value, record):
        output = record.matches
        return mark_safe(output)

class GenageSequenceTable(tables.Table):
    class Meta:
        model = Sequence
        fields = ('identifier', 'type') 
        attrs = {'class': 'table table-bordered table-striped'}

    identifier = tables.LinkColumn('annotation_details', args=[A('identifier')], verbose_name='Identifier')
    type = tables.Column(verbose_name='Type', orderable=False)
    gene = tables.Column(accessor=A('identifier'), verbose_name='Matches in GenAge', orderable=False)

    def render_gene(self, record, value):
        output = ''
        for g in record.genes.filter(gene__in_genage=True):
            output += u'<div><a href="http://genomics.senescence.info/genes/entry.php?hgnc={}">{}</a> <small>({})</small></div>'.format(g.gene.symbol, g.gene.symbol, g.gene.organism.common_name)
        return mark_safe(output)
