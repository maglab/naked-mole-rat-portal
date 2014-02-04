# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Sequence.ncbi_symbol'
        db.alter_column(u'annotations_sequence', 'ncbi_symbol', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

    def backwards(self, orm):

        # Changing field 'Sequence.ncbi_symbol'
        db.alter_column(u'annotations_sequence', 'ncbi_symbol', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

    models = {
        u'annotations.gene': {
            'Meta': {'object_name': 'Gene'},
            'alias': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ensembl': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'entrez_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_genage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'db_index': 'True'}),
            'omim': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'organism': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['annotations.Organism']"}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'unigene': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'uniprot': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        u'annotations.genematch': {
            'Meta': {'object_name': 'GeneMatch'},
            'cdna_percentage_match': ('django.db.models.fields.FloatField', [], {}),
            'gene': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['annotations.Gene']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'ka': ('django.db.models.fields.FloatField', [], {}),
            'ka_ks_ratio': ('django.db.models.fields.FloatField', [], {}),
            'ks': ('django.db.models.fields.FloatField', [], {}),
            'protein_percentage_match': ('django.db.models.fields.FloatField', [], {})
        },
        u'annotations.mirna': {
            'Meta': {'object_name': 'miRNA'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sequences': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['annotations.Sequence']", 'symmetrical': 'False'})
        },
        u'annotations.organism': {
            'Meta': {'ordering': "['common_name']", 'object_name': 'Organism'},
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'taxonomy_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'annotations.sequence': {
            'Meta': {'object_name': 'Sequence'},
            'entrez_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'genes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['annotations.GeneMatch']", 'null': 'True', 'blank': 'True'}),
            'has_genes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'ncbi_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'ncbi_predicted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ncbi_symbol': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'part_of': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'related_sequences'", 'null': 'True', 'to': u"orm['annotations.Sequence']"}),
            'sequence': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['annotations.SequenceType']"})
        },
        u'annotations.sequencetype': {
            'Meta': {'object_name': 'SequenceType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['annotations']