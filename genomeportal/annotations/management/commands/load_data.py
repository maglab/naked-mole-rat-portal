import csv
from Bio import SeqIO

from django.core.management.base import BaseCommand

from genomeportal.annotations.models import *

class Command(BaseCommand):
    args = '<input_file> <mapping_file>'
    help = 'Takes and input file and a mapping file to add the data to the database'

    def handle(self, *args, **options):
        with open(args[0]) as input_file, open(args[1]) as mapping_file, open(args[2]) as fasta_file:
            mapping_data = {}
            for row in csv.DictReader(mapping_file, delimiter="\t"):
                mapping_data[row['Ensembl Protein ID']] = row

            sequence_matches = {}
            for row in csv.DictReader(input_file, delimiter="\t"):
                sequence_matches[row['SEQ1']] = row

            seq_type, new = SequenceType.objects.get_or_create(name='cDNA')

            o, new = Organism.objects.get_or_create(taxonomy_id=10090, name='Mus musculus', common_name='Mouse')

            for seq in SeqIO.parse(fasta_file, 'fasta'):
                
                try:
                    match = sequence_matches[seq.id]
                except KeyError:
                    match = {'SEQ1': seq.id, 'SEQ2': None}

                s, new = Sequence.objects.get_or_create(identifier=match['SEQ1'], type=seq_type, sequence=unicode(seq.seq))

                if match['SEQ2'] in mapping_data:
                    dta = mapping_data[match['SEQ2']]
                    name = dta['Description'].split('[')
                    entrez_id = None if dta['EntrezGene ID'] == '' else dta['EntrezGene ID']
                    g, new = Gene.objects.get_or_create(name=name[0], symbol=dta['Associated Gene Name'], entrez_id=entrez_id, ensembl=dta['Ensembl Gene ID'], unigene=dta['Unigene ID'], uniprot=dta['UniProt/SwissProt ID'], organism=o)

                    gm = GeneMatch(identifier=match['SEQ2'], protein_percentage_match=match['PROT_PERCENTID'], cdna_percentage_match=match['CDNA_PERCENTID'], ka=match['Ka'], ks=match['Ks'], ka_ks_ratio=match['Ka/Ks'], gene=g)
                    gm.save()

                    s.genes.add(gm)
