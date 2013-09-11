# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GeneMatch'
        db.create_table(u'annotations_genematch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('protein_percentage_match', self.gf('django.db.models.fields.FloatField')()),
            ('cdna_percentage_match', self.gf('django.db.models.fields.FloatField')()),
            ('ka', self.gf('django.db.models.fields.FloatField')()),
            ('ks', self.gf('django.db.models.fields.FloatField')()),
            ('ka_ks_ratio', self.gf('django.db.models.fields.FloatField')()),
            ('gene', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['annotations.Gene'])),
        ))
        db.send_create_signal(u'annotations', ['GeneMatch'])

        # Deleting field 'Sequence.gene'
        db.delete_column(u'annotations_sequence', 'gene_id')

        # Adding M2M table for field genes on 'Sequence'
        m2m_table_name = db.shorten_name(u'annotations_sequence_genes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sequence', models.ForeignKey(orm[u'annotations.sequence'], null=False)),
            ('genematch', models.ForeignKey(orm[u'annotations.genematch'], null=False))
        ))
        db.create_unique(m2m_table_name, ['sequence_id', 'genematch_id'])


        # Changing field 'Sequence.sequence'
        db.alter_column(u'annotations_sequence', 'sequence', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):
        # Deleting model 'GeneMatch'
        db.delete_table(u'annotations_genematch')


        # User chose to not deal with backwards NULL issues for 'Sequence.gene'
        raise RuntimeError("Cannot reverse this migration. 'Sequence.gene' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Sequence.gene'
        db.add_column(u'annotations_sequence', 'gene',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['annotations.Gene']),
                      keep_default=False)

        # Removing M2M table for field genes on 'Sequence'
        db.delete_table(db.shorten_name(u'annotations_sequence_genes'))


        # User chose to not deal with backwards NULL issues for 'Sequence.sequence'
        raise RuntimeError("Cannot reverse this migration. 'Sequence.sequence' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Sequence.sequence'
        db.alter_column(u'annotations_sequence', 'sequence', self.gf('django.db.models.fields.TextField')())

    models = {
        u'annotations.gene': {
            'Meta': {'object_name': 'Gene'},
            'alias': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ensembl': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'entrez_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
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