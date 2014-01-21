from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django_tables2 import RequestConfig

from genomeportal.annotations.models import Sequence, SequenceType
from genomeportal.annotations.tables import SequenceTable

def results(request):
    term = request.GET.get('s')
    filter_gene = request.GET.get('gene')
    filter_type = request.GET.get('type')

    if term is not None and term != '':
        results_list = Sequence.objects.distinct().filter(Q(identifier__icontains=term) | Q(type__name=term) | Q(genes__gene__ensembl__icontains=term) | Q(genes__gene__symbol__icontains=term))
    else:
        results_list = Sequence.objects.defer('sequence').all().distinct()

    if filter_gene == 'true':
        results_list = results_list.annotate(gene_count=Count('genes')).filter(gene_count__gt=0)
    elif filter_gene == 'false':
        results_list = results_list.annotate(gene_count=Count('genes')).filter(gene_count=0)

    if filter_type and filter_type != '':
        results_list = results_list.filter(type__name=filter_type)

    results = SequenceTable(results_list)
    RequestConfig(request).configure(results)

    start = results.page.number-3 if results.page.number-3 > 0 else 0
    end = results.page.number+3 if results.page.number+3 < results.page.end_index()+1 else results.page.end_index()+1
    pages = results.page.paginator.page_range[start:end]

    gene_pres_options = (('true', 'Has gene matches'), ('false', 'No gene matches'))

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
    return render(request, 'details.jade', {
        'details': details
    })

def raw_sequence(request, identifier):
    details = get_object_or_404(Sequence, identifier=identifier)
    return render(request, 'raw_sequence.jade', {
        'details': details
    })
