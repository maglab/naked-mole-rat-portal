import csv
from Bio import SeqIO

from django.core.management.base import BaseCommand

from genomeportal.annotations.models import *

class Command(BaseCommand):
    help = 'Checks if a sequnce has a gene in marks true if so'

    def handle(self, *args, **options):
        for s in Sequence.objects.all():
            if s.genes.count() > 0:
                s.has_genes = True
                s.save()
