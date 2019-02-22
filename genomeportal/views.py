from django.shortcuts import render

from genomeportal.annotations.models import Organism, SequenceType

def index(request):
    stats = SequenceType.objects.all()
    return render(request, 'index.pug', {
        'organisms': [o.common_name for o in Organism.objects.all()],
        'stats': stats,
    })
