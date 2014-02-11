import sys
import os

from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from django.conf import settings

from django_tables2 import RequestConfig

from genomeportal.annotations.models import Sequence, SequenceType
from genomeportal.annotations.tables import SequenceTable

def results(request):
    term = request.GET.get('s')
    filter_gene = request.GET.get('gene')
    filter_type = request.GET.get('type')

    if term is not None and term != '':
        term = term.strip()
        results_list = Sequence.objects.defer('sequence').filter(Q(identifier__icontains=term) | Q(type__name=term) | Q(genes__gene__ensembl__icontains=term) | Q(genes__gene__symbol__icontains=term) | Q(ncbi_symbol__icontains=term) | Q(ncbi_name__icontains=term) | Q(entrez_id__icontains=term)).prefetch_related('genes').select_related('part_of').distinct()
    else:
        results_list = Sequence.objects.defer('sequence').all().prefetch_related('genes').select_related('part_of').distinct()

    if filter_gene == 'true':
        results_list = results_list.filter(has_genes=True) #.annotate(gene_count=Count('genes')).filter(gene_count__gt=0)
    elif filter_gene == 'false':
        results_list = results_list.filter(has_genes=False)#.annotate(gene_count=Count('genes')).filter(gene_count=0)

    if filter_type and filter_type != '':
        results_list = results_list.filter(type__name=filter_type)

    results = SequenceTable(results_list)
    RequestConfig(request).configure(results)

    start = results.page.number-3 if results.page.number-3 > 0 else 0
    end = results.page.number+3 if results.page.number+3 < results.page.end_index()+1 else results.page.end_index()+1
    pages = results.page.paginator.page_range[start:end]

    gene_pres_options = (('true', 'Show only best hit gene matches'), ('false', 'Show only low hit gene matches'))

    return render(request, 'results.jade', {
        'results': results,
        'pages': pages,
        'term': term,
        'types': SequenceType.objects.all(),
        'gene': filter_gene,
        'type': filter_type,
        'gene_pres_options': gene_pres_options,
    })

def details(request, identifier):
    details = get_object_or_404(Sequence, identifier=identifier)
    sequence = details.sequence#[0:20000]
    return render(request, 'details.jade', {
        'details': details,
        'sequence': sequence,
    })

def alignments(request, identifier):
    details = get_object_or_404(Sequence, identifier=identifier)
    if details.type.name != 'Protein':
        raise Http404
    try:
        gpg = details.part_of.genes.filter(gene__organism__name='Cavia porcellus')[0]
        filename = '{}.aln'.format(gpg.identifier)
        with open(os.path.join(settings.ALIGNMENTS_DIR, filename)) as alignment:
            return HttpResponse(alignment.read(), content_type='text/plain')
    except:
        raise Http404

def raw_sequence(request, identifier):
    details = get_object_or_404(Sequence, identifier=identifier)
    return render(request, 'raw_sequence.jade', {
        'details': details
    })
