import csv
from Bio import SeqIO

from django.core.management.base import BaseCommand

from genomeportal.annotations.models import *

class Command(BaseCommand):
    args = '<match_file> <cds_file> <prot_file> <details_file>'
    help = 'Takes and input file and a mapping file to add the data to the database'

    def handle(self, *args, **options):
        """
        Take match, cds and prot data and create entries in database based on further information in details file
        """
        with open(args[0]) as match_file, open(args[1]) as cds_file, open(args[2]) as prot_file, open(args[3]) as details_file:
            # Turn the details file into a dict with protein ID as key. 
            # This may bork some entries but they'd have to be manually
            details = {}
            for row in csv.DictReader(details_file, delimiter="\t"):
                details[row['Ensembl Protein ID']] = row

            # Convert the match file to a dict with protein ID as key
            matches = {}
            for row in csv.DictReader(match_file, delimiter="\t"):
                if row['SEQ1'] not in matches:
                    matches[row['SEQ1']] = []
                matches[row['SEQ1']].append(row)

            # Convert the protein file to dict, identifier as key
            protein_sequences = {}
            for seq in SeqIO.parse(prot_file, 'fasta'):
                protein_sequences[seq.id] = unicode(seq.seq) 

            o, new = Organism.objects.get_or_create(taxonomy_id=10090, name='Mus musculus', common_name='Mouse')
            seq_cds, new = SequenceType.objects.get_or_create(name='cDNA')
            seq_prot, new = SequenceType.objects.get_or_create(name='Protein')

            for seq in SeqIO.parse(cds_file, 'fasta'):
                try:
                    match = matches[seq.id]
                except KeyError:
                    match = [{'SEQ1': seq.id, 'SEQ2': None}]

                cds_sequence, new = Sequence.objects.get_or_create(identifier=seq.id, type=seq_cds, sequence=unicode(seq.seq))
                protein_sequence, new = Sequence.objects.get_or_create(identifier=seq.id, type=seq_prot, sequence=protein_sequences[seq.id], part_of=cds_sequence)

                for m in match:
                    if m['SEQ2'] in details:
                        dta = details[m['SEQ2']]
                        name = dta['Description'].split('[')
                        entrez_id = None if dta['EntrezGene ID'] == '' else dta['EntrezGene ID']
                        g, new = Gene.objects.get_or_create(name=name[0], symbol=dta['Associated Gene Name'], entrez_id=entrez_id, ensembl=dta['Ensembl Gene ID'], unigene=dta['Unigene ID'], uniprot=dta['UniProt/SwissProt ID'], organism=o)

                        gm = GeneMatch(identifier=m['SEQ2'], protein_percentage_match=m['PROT_PERCENTID'], cdna_percentage_match=m['CDNA_PERCENTID'], ka=m['Ka'], ks=m['Ks'], ka_ks_ratio=m['Ka/Ks'], gene=g)
                        gm.save()

                        cds_sequence.genes.add(gm)
