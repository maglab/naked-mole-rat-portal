from django.core.urlresolvers import reverse
from haystack import indexes
from genomeportal.annotations.models import Sequence

class SequenceIndex(indexes.Indexable, indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)

    identifier = indexes.CharField(model_attr='identifier')
    type = indexes.CharField(model_attr='type')
    has_genes = indexes.BooleanField(model_attr='has_genes')
    matches = indexes.CharField()

    ka_ks_ratio = indexes.MultiValueField()
    cds_percentage = indexes.MultiValueField()
    protein_percentage = indexes.MultiValueField()

    def get_model(self):
        return Sequence

    def prepare_matches(self, obj):
        output = u''
        if obj.part_of and obj.part_of.type.name != 'Scaffold':
            output += '<span class="highlight-related">Part of <a href="{0}">{1}</a></span>'.format(reverse('genomeportal.annotations.views.details', args=(obj.part_of.identifier,)), obj.part_of.identifier)
        if obj.ncbi_symbol is not None:
            output += u'<div>{} <small>({})</small></div>'.format(obj.ncbi_symbol, 'NCBI Annotation')
        elif obj.ncbi_name is not None:
            output += u'<div>{} <small>({})</small></div>'.format(obj.ncbi_name, 'NCBI Annotation')
        output += u''.join([u'<div>{} <small>({})</small></div>'.format(v.gene.symbol if v.gene.symbol != '' else v.gene.ensembl, v.gene.organism.common_name) for v in obj.genes.all()])
        return output 

    def prepare_ka_ks_ratio(self, obj):
        return [g.ka_ks_ratio for g in obj.genes.all()]

    def prepare_cds_percentage(self, obj):
        return [g.cdna_percentage_match for g in obj.genes.all()]

    def prepare_protein_percentage(self, obj):
        return [g.protein_percentage_match for g in obj.genes.all()]

    def prepare(self, obj):
        data = super(SequenceIndex, self).prepare(obj)
        if obj.has_genes:
            data['boost'] = 1.5
        elif obj.type.name == 'Coding sequence' and obj.has_genes is False:
            data['boost'] = 0.1
        return data
