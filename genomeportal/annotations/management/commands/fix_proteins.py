import csv
from Bio import SeqIO

from django.core.management.base import BaseCommand

from genomeportal.annotations.models import *

class Command(BaseCommand):
    args = '<type> <files...>'
    # 1: scaffolds
    #args = '<match_file> <cds_file> <prot_file> <details_file>'
    help = 'Takes and input file and a mapping file to add the data to the database'

    def handle(self, *args, **options):
        with open(args[1]) as pl:
            proteins = [p.strip() for p in pl.read().split("\n"))]
        all_proteins = Sequence.objects.filter(type__name='Protein')
        for p in all_proteins:
            if p.identifier not in proteins:
                print p.identifier
