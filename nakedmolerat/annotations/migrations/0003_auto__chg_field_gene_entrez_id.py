# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Gene.entrez_id'
        db.alter_column(u'annotations_gene', 'entrez_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Gene.entrez_id'
        raise RuntimeError("Cannot reverse this migration. 'Gene.entrez_id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Gene.entrez_id'
        db.alter_column(u'annotations_gene', 'entrez_id', self.gf('django.db.models.fields.PositiveIntegerField')())

    models = {
        u'annotations.gene': {
            'Meta': {'object_name': 'Gene'},
            'alias': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ensembl': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'entrez_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_genage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
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
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ka': ('django.db.models.fields.FloatField', [], {}),
            'ka_ks_ratio': ('django.db.models.fields.FloatField', [], {}),
            'ks': ('django.db.models.fields.FloatField', [], {}),
            'protein_percentage_match': ('django.db.models.fields.FloatField', [], {})
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
            'genes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['annotations.GeneMatch']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sequence': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['annotations.SequenceType']"})
        },
        u'annotations.sequencetype': {
            'Meta': {'object_name': 'SequenceType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['annotations']