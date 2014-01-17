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
        """
        With a given type of data process and load into database
        """
        if args[0] == 'scaffolds':
            self.load_scaffolds(args[1])
        elif args[0] == 'cdna':
            self.load_cds(args[1], args[2])
        elif args[0] == 'proteins':
            self.load_proteins(args[1])
        elif args[0] == 'genes':
            self.load_genes(args[1], args[2], args[3], args[4], args[5])
        elif args[0] == 'mirnas':
            self.load_mirnas(args[1])
        else:
            self.stdout.write('Type not recognised')

    def _parse_and_load_fasta(self, fasta_file, sequence_type, include_type_in_name=False, mapping_file=False, is_complement=False):
        mapping = {}
        if mapping_file:
            # Map one object to another via identifier in file
            with open(mapping_file) as mf:
                for l in mf:
                    r = l.split("\t")
                    mapping[r[0]] = r[1].strip()
        with open(fasta_file) as fasta:
            for seq in SeqIO.parse(fasta, 'fasta'):
                seq_id = seq.id.strip('|').split('|')[-1]
                if seq_id in mapping:
                    part_of = Sequence.objects.get(identifier=mapping[seq_id])
                elif is_complement:
                    part_of = Sequence.objects.get(identifier=seq_id)
                else:
                    part_of = None
                if include_type_in_name:
                    identifier = '{}.{}'.format(seq_id, sequence_type.name.lower())
                else:
                    identifier = seq_id
                s = Sequence(identifier=identifier, sequence=unicode(seq.seq), type=sequence_type, part_of=part_of)
                s.save()

    def load_scaffolds(self, scaffold_file):
        """
        Load scaffold sequences in. These are base sequences and have no mapping
        """
        sequence_type,created = SequenceType.objects.get_or_create(name='Scaffold')
        self._parse_and_load_fasta(scaffold_file, sequence_type)

    def load_cds(self, cds_file, mapping_file):
        """
        Load cDNA sequences. These map to scaffolds.
        """
        sequence_type,created = SequenceType.objects.get_or_create(name='cDNA')
        self._parse_and_load_fasta(cds_file, sequence_type, mapping_file=mapping_file)

    def load_proteins(self, protein_file):
        """
        Load protein sequences. These map to cDNA sequences.
        """
        sequence_type,created = SequenceType.objects.get_or_create(name='Protein')
        self._parse_and_load_fasta(protein_file, sequence_type, is_complement=True, include_type_in_name=True)

    def load_genes(self, match_file, details_file, species_name, species_common_name, taxonomy_id):
        """
        Load genes. There may be multiple species so this can be run multiple times.
        The match file contains the actual gene matches, the details file is for info
        from ensembl to create the gene objects. Taxonomy ID is from the NCBI.
        """
        with open(details_file) as df, open(match_file) as mf:
            sequences = Sequence.objects.filter(type__name='cDNA')
            o,c = Organism.objects.get_or_create(taxonomy_id=taxonomy_id, name=species_name, common_name=species_common_name)

            # Turn the details file into a dict with protein ID as key. 
            # This may bork some entries but they'd have to be manually
            # annotated otherwise
            details = {}
            for row in csv.DictReader(df, delimiter="\t"):
                details[row['Ensembl Protein ID']] = row

            # Convert the match file to a dict with protein ID as key
            matches = {}
            for row in csv.DictReader(mf, delimiter="\t"):
                if row['SEQ2'] not in matches:
                    matches[row['SEQ2']] = []
                matches[row['SEQ2']].append(row)

            for s in sequences:
                if s.identifier in matches:
                    match = matches[s.identifier]
                    for m in match:
                        if m['SEQ1'] in details:
                            dta = details[m['SEQ1']]
                            name = dta['Description'].split('[')
                            entrez_id = None if dta['EntrezGene ID'] == '' else dta['EntrezGene ID']
                            g, new = Gene.objects.get_or_create(name=name[0], symbol=dta['Associated Gene Name'], entrez_id=entrez_id, ensembl=dta['Ensembl Gene ID'], unigene=dta['Unigene ID'], uniprot=dta['UniProt/SwissProt ID'], organism=o)
                            gm = GeneMatch(identifier=m['SEQ1'], protein_percentage_match=m['PROT_PERCENTID'], cdna_percentage_match=m['CDNA_PERCENTID'], ka=m['Ka'], ks=m['Ks'], ka_ks_ratio=m['Ka/Ks'], gene=g)
                            gm.save()

                            s.genes.add(gm)

    def load_mirnas(self, mirna_file):
        """
        Load miRNA's. These map to scaffolds
        """
        with open(mirna_file) as mirnas:
            sequence_type,created = SequenceType.objects.get_or_create(name='miRNA')
            for r in csv.DictReader(mirnas):
                part_of_identifier = r['provisional id'].rsplit('_', 1)
                part_of = Sequence.objects.get(identifier=part_of_identifier[0])

                s = Sequence(identifier=r['provisional id'], sequence=r['consensus mature sequence'], part_of=part_of, type=sequence_type)
                s.save()

                if r['example miRBase miRNA with the same seed'] != '-':
                    mi,c = miRNA.objects.get_or_create(identifier=r['example miRBase miRNA with the same seed'])
                    mi.sequences.add(s)
