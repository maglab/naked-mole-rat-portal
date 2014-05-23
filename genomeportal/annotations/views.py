import sys
import os

from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from django.conf import settings

from django_tables2 import RequestConfig

from haystack.query import SearchQuerySet
from haystack.inputs import Raw

from genomeportal.annotations.models import Sequence, SequenceType
from genomeportal.annotations.tables import SequenceTable, GenageSequenceTable


def results(request):
    """ Show the results of a query and filters """
    term = request.GET.get('s')
    filter_gene = request.GET.get('gene')
    filter_type = request.GET.get('type')

    if term is not None and term != '':
        term = term.strip()
        results_list = SearchQuerySet().filter(content=Raw(term))
    else:
        results_list = SearchQuerySet().all()

    if filter_gene == 'true':
        results_list = results_list.filter(has_genes=True)
    elif filter_gene == 'false':
        results_list = results_list.filter(has_genes=False)

    if filter_type and filter_type != '':
        results_list = results_list.filter(type__name=filter_type)

    results = SequenceTable(results_list)
    RequestConfig(request).configure(results)

    # This shows page numbers before and after the current page, without negative numbers getting involved
    start = results.page.number-3 if results.page.number-3 > 0 else 0
    end = results.page.number+3 if results.page.number+3 < results.page.end_index()+1 else results.page.end_index()+1
    pages = results.page.paginator.page_range[start:end]

    # Avoids repetition of stuff in the templates
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
    """ Show the details of a sequence based on identifier """
    details = get_object_or_404(Sequence, identifier=identifier)
    sequence = details.sequence
    return render(request, 'details.jade', {
        'details': details,
        'sequence': sequence,
    })

def alignments(request, identifier):
    """ Show the contents of an alignment file """
    if identifier != '':
        try:
            filename = '{}.aln'.format(identifier)
            with open(os.path.join(settings.ALIGNMENTS_DIR, filename)) as alignment:
                return HttpResponse(alignment.read(), content_type='text/plain')
        except:
            raise Http404
    else:
        raise Http404

def raw_sequence(request, identifier):
    """ Display a raw genomics sequence based on the identifier provided"""
    details = get_object_or_404(Sequence, identifier=identifier)
    return render(request, 'raw_sequence.jade', {
        'details': details
    })

def genage(request):
    """ List all of the sequences that are also in the GenAge database """
    results_list = Sequence.objects.filter(in_genage=True) 
    results = GenageSequenceTable(results_list)
    RequestConfig(request).configure(results)

    start = results.page.number-3 if results.page.number-3 > 0 else 0
    end = results.page.number+3 if results.page.number+3 < results.page.end_index()+1 else results.page.end_index()+1
    pages = results.page.paginator.page_range[start:end]

    return render(request, 'results_genage.jade', {
        'pages': pages,
        'results': results
    })
