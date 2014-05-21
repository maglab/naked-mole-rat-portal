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
    #score = tables.Column(accessor=A('score'))

    def __init__(self, *args, **kwargs):
        super(SequenceTable, self).__init__(*args, **kwargs)
        self.rows = HighlightBoundRows(data=self.data, table=self)

    def render_gene(self, value, record):
        output = record.matches #''
        '''
        if record.part_of and record.part_of.type.name != 'Scaffold':
            output += '<span class="highlight-related">Part of <a href="{0}">{1}</a></span>'.format(reverse('genomeportal.annotations.views.details', args=(record.part_of.identifier,)), record.part_of.identifier)
        if record.ncbi_symbol is not None:
            output += u'<div>{} <small>({})</small></div>'.format(record.ncbi_symbol, 'NCBI Annotation')
        elif record.ncbi_name is not None:
            output += u'<div>{} <small>({})</small></div>'.format(record.ncbi_name, 'NCBI Annotation')
        output += u''.join([u'<div>{} <small>({})</small></div>'.format(v.gene.symbol if v.gene.symbol != '' else v.gene.ensembl, v.gene.organism.common_name) for v in record.genes.all()])
        '''
        return mark_safe(output)

class GenageSequenceTable(tables.Table):
    class Meta:
        model = Sequence
        fields = ('identifier', 'type') 
        attrs = {'class': 'table table-bordered table-striped'}

    identifier = tables.LinkColumn('annotation_details', args=[A('identifier')], verbose_name='Identifier')
    type = tables.Column(verbose_name='Type', orderable=False)
    gene = tables.Column(accessor=A('identifier'), verbose_name='Matches', orderable=False)

    def render_gene(self, record, value):
        output = ''
        for g in record.genes.filter(gene__in_genage=True):
            output += u'<div>{} <small>({})</small></div>'.format(g.gene.symbol, g.gene.organism.common_name)
        return mark_safe(output)
