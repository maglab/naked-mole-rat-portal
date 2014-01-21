from django.db import models

class Organism(models.Model):
    class Meta:
        ordering = ['common_name']
    taxonomy_id = models.PositiveIntegerField(db_index=True)
    name = models.CharField(max_length=50)
    common_name = models.CharField(max_length=50, blank=True, null=True)

    def convert_for_url(self):
        return self.name.replace(' ', '_')

    def __unicode__(self):
        if self.common_name != '':
            return self.common_name
        else:
            return self.name

class Gene(models.Model):
    entrez_id = models.PositiveIntegerField(db_index=True, null=True, blank=True)
    name = models.CharField(max_length=300, db_index=True)
    symbol = models.CharField(max_length=20, db_index=True)
    alias = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    omim = models.CharField(max_length=20, blank=True, null=True)
    ensembl = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    uniprot = models.CharField(max_length=20, blank=True, null=True)
    unigene = models.CharField(max_length=20, blank=True, null=True)
    in_genage = models.BooleanField(default=False)

    organism = models.ForeignKey(Organism)

    def __unicode__(self):
        return self.symbol+' ('+self.name+')'

class GeneMatch(models.Model):
    identifier = models.CharField(max_length=50, db_index=True)
    protein_percentage_match = models.FloatField()
    cdna_percentage_match = models.FloatField()
    ka = models.FloatField()
    ks = models.FloatField()
    ka_ks_ratio = models.FloatField()

    gene = models.ForeignKey(Gene)

    def __unicode__(self):
        return u'{0} ({1})'.format(self.identifier, self.gene.symbol)

class SequenceType(models.Model):
    name = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name

class Sequence(models.Model):
    identifier = models.CharField(max_length=50, db_index=True)
    sequence = models.TextField(blank=True, null=True)

    type = models.ForeignKey(SequenceType)
    part_of = models.ForeignKey('self', related_name='related_sequences', blank=True, null=True)

    genes = models.ManyToManyField(GeneMatch, blank=True, null=True)

    def position_from_identifier(self):
        return self.identifier.split('_')[-1]

    def __unicode__(self):
        return self.identifier

class miRNA(models.Model):
    identifier = models.CharField(max_length=50)
    sequences = models.ManyToManyField(Sequence)

    def __unicode__(self):
        return self.identifier
