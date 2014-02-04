from django.utils.safestring import mark_safe

import django_tables2 as tables
from django_tables2 import A
from django_tables2.rows import BoundRows, BoundRow

from genomeportal.annotations.models import Sequence

class HighlightBoundRows(BoundRows):
    def __iter__(self):
        for record in self.data:
            row = BoundRow(record, table=self.table)
            if record.has_genes:
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

    identifier = tables.LinkColumn('annotation_details', args=[A('identifier')])
    type = tables.Column()
    gene = tables.Column(accessor=A('identifier'), verbose_name='Matches', orderable=False)

    def __init__(self, *args, **kwargs):
        super(SequenceTable, self).__init__(*args, **kwargs)
        self.rows = HighlightBoundRows(data=self.data, table=self)

    def render_gene(self, value, record):
        output = ''
        if record.ncbi_symbol is not None:
            output += u'<div>{} <small>({})</small></div>'.format(record.ncbi_symbol, 'NCBI Annotation')
        elif record.ncbi_name is not None:
            output += u'<div>{} <small>({})</small></div>'.format(record.ncbi_name, 'NCBI Annotation')
        if record.mirna_set.count() > 0:
            output += u''.join([u'<div>{}</div>'.format(v.identifier) for v in record.mirna_set.all()])
        else:
            output += u''.join([u'<div>{} <small>({})</small></div>'.format(v.gene.symbol if v.gene.symbol != '' else v.gene.ensembl, v.gene.organism.common_name) for v in record.genes.all()])
        return mark_safe(output)
