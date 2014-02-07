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
            self.load_cds(args[1], args[2], args[3])
        elif args[0] == 'proteins':
            self.load_proteins(args[1], args[2])
        elif args[0] == 'genes':
            self.load_genes(args[1], args[2], args[3], args[4], args[5], args[6])
        elif args[0] == 'mirnas':
            self.load_mirnas(args[1])
        elif args[0] == 'mrna_identifiers':
            self.load_mrna_identifiers(args[1])
        elif args[0] == 'noncoding':
            self.load_noncoding(args[1])
        elif args[0] == 'entrez_ids':
            self.load_entrez(args[1])
        else:
            self.stdout.write('Type not recognised')

    def _parse_and_load_fasta(self, fasta_file, sequence_type, mapping_file=False, is_complement=False, no_sequence=False, map_protein_to_gene=False):
        mapping = {}
        if mapping_file:
            # Map one object to another via identifier in file
            with open(mapping_file) as mf:
                for l in mf:
                    r = l.split("\t")
                    mapping[r[0]] = r[1].strip()

        if map_protein_to_gene:
            protein_to_gene = {}
            with open(map_protein_to_gene) as pgf:
                for l in pgf:
                    r = l.split("\t")
                    protein_to_gene[r[0]] = r

        with open(fasta_file) as fasta:
            for seq in SeqIO.parse(fasta, 'fasta'):
                seq_id = seq.id.strip('|').split('|')[-1]
                if seq_id in mapping:
                    try:
                        part_of = Sequence.objects.get(identifier=mapping[seq_id])
                    except:
                        part_of = None
                        
                elif is_complement:
                    try:
                        part_of = Sequence.objects.get(identifier='{}'.format(seq_id))
                    except:
                        part_of = None
                else:
                    part_of = None

                ncbi_symbol = None
                ncbi_name = None
                ncbi_predicted = False
                description = seq.description.split('|')[-1].strip()
                if description.startswith('PREDICTED:'):
                    ncbi_predicted = True
                if map_protein_to_gene:
                    identifier = protein_to_gene[seq_id][1]
                    ncbi_symbol = protein_to_gene[seq_id][2]
                    ncbi_name = protein_to_gene[seq_id][3].strip()
                else:
                    identifier = seq_id
                    ncbi_name = description

                if no_sequence:
                    seq_string = None
                else:
                    seq_string = unicode(seq.seq)
                    
                #print identifier, seq_string, ncbi_name, ncbi_symbol, ncbi_predicted
                s = Sequence(identifier=identifier, sequence=seq_string, type=sequence_type, part_of=part_of, ncbi_name=ncbi_name, ncbi_symbol=ncbi_symbol, ncbi_predicted=ncbi_predicted)
                s.save()

    def load_scaffolds(self, scaffold_file):
        """
        Load scaffold sequences in. These are base sequences and have no mapping
        """
        sequence_type,created = SequenceType.objects.get_or_create(name='Scaffold')
        self._parse_and_load_fasta(scaffold_file, sequence_type, no_sequence=True)

    def load_cds(self, cds_file, mapping_file, map_protein_to_gene):
        """
        Load cDNA sequences. These map to scaffolds.
        """
        sequence_type,created = SequenceType.objects.get_or_create(name='Coding sequence')
        self._parse_and_load_fasta(cds_file, sequence_type, mapping_file=mapping_file, map_protein_to_gene=map_protein_to_gene)

    def load_proteins(self, protein_file, mapping_file):
        """
        Load protein sequences. These map to cDNA sequences.
        """
        sequence_type,created = SequenceType.objects.get_or_create(name='Protein')
        self._parse_and_load_fasta(protein_file, sequence_type, is_complement=True, mapping_file=mapping_file)

    def load_genes(self, match_file, details_file, species_name, species_common_name, taxonomy_id, identifier_order):
        """
        Load genes. There may be multiple species so this can be run multiple times.
        The match file contains the actual gene matches, the details file is for info
        from ensembl to create the gene objects. Taxonomy ID is from the NCBI.
        """
        with open(details_file) as df, open(match_file) as mf:
            sequences = Sequence.objects.filter(type__name='Coding sequence')
            o,c = Organism.objects.get_or_create(taxonomy_id=taxonomy_id, name=species_name, common_name=species_common_name)

            # Turn the details file into a dict with protein ID as key. 
            # This may bork some entries but they'd have to be manually
            # annotated otherwise
            details = {}
            for row in csv.DictReader(df, delimiter="\t"):
                details[row['Ensembl Protein ID']] = row

            if identifier_order == 'external_first':
                external = 'SEQ1'
                internal = 'SEQ2'
            else:
                external = 'SEQ2'
                internal = 'SEQ1'

            # Convert the match file to a dict with protein ID as key
            matches = {}
            for row in csv.DictReader(mf, delimiter="\t"):
                if row[internal] not in matches:
                    matches[row[internal]] = []
                matches[row[internal]].append(row)

            for s in sequences:
                identifier = s.identifier
                if identifier in matches:
                    match = matches[identifier]
                    for m in match:
                        if m[external] in details:
                            dta = details[m[external]]
                            name = dta['Description'].split('[')
                            entrez_id = None if dta['EntrezGene ID'] == '' else dta['EntrezGene ID']
                            g, new = Gene.objects.get_or_create(name=name[0], symbol=dta.get('Associated Gene Name'), entrez_id=entrez_id, ensembl=dta.get('Ensembl Gene ID'), unigene=dta.get('Unigene ID'), uniprot=dta.get('UniProt/SwissProt ID'), organism=o)
                            gm = GeneMatch(identifier=m[external], protein_percentage_match=m['PROT_PERCENTID'], cdna_percentage_match=m['CDNA_PERCENTID'], ka=m['Ka'], ks=m['Ks'], ka_ks_ratio=m['Ka/Ks'], gene=g)
                            gm.save()

                            s.has_genes = True
                            s.save()
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

    def load_mrna_identifiers(self, mrna_mapping_file, suffix='cDNA'):
        with open(mrna_mapping_file) as mrna_file:
            for line in csv.reader(mrna_file, delimiter="\t"):
                try:
                    seq = Sequence.objects.get(identifier='{}.{}'.format(line[0],suffix))
                    seq.part_of_mrna = line[1]
                    seq.save()
                except:
                    pass

    def load_noncoding(self, noncoding_file):
        """
        Load non-coding sequences. These map to scaffolds
        """
        sequence_type,created = SequenceType.objects.get_or_create(name='Non-coding sequence')
        with open(noncoding_file) as nf:
            for line in csv.reader(nf, delimiter="\t"):
                part_of = Sequence.objects.get(identifier=line[3])
                ncbi_predicted = False
                if line[2].startswith('PREDICTED:'):
                    ncbi_predicted = True
                s = Sequence(identifier=line[0], sequence=line[4], type=sequence_type, part_of=part_of, ncbi_name=line[2], ncbi_symbol=line[1], ncbi_predicted=ncbi_predicted)
                s.save()

    def load_entrez(self, entrez_file):
        """
        Load entrez ids into genes.
        """
        with open(entrez_file) as ef:
            for line in csv.reader(ef, delimiter="\t"):
                try:
                    seq = Sequence.objects.get(identifier=line[0])
                    seq.entrez_id = int(line[1])
                    seq.save()
                except:
                    pass
