from Bio import SeqIO

input_filename = 'source_downloads/hgb_ref_HetGla_female_1.0_chrUn.fa'

for seq in SeqIO.parse(open(input_filename), 'fasta'):
    split_desc = seq.description.split('|')
    print '>{} {}\n{}'.format(split_desc[3], seq.description, str(seq.seq))
