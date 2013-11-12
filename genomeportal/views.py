from django.shortcuts import render

from genomeportal.annotations.models import Organism

def index(request):
    return render(request, 'index.jade', {
        'organisms': [o.common_name for o in Organism.objects.all()],
    })
