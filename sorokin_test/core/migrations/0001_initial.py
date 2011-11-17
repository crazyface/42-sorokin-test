# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'RequestStore'
        db.create_table('core_requeststore', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('url', self.gf('django.db.models.fields.TextField')()),
            ('req_get', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('req_post', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('req_cookies', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('req_session', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('req_meta', self.gf('django.db.models.fields.TextField')()),
            ('req_status_code', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['RequestStore'])

        # Adding model 'DbEntry'
        db.create_table('core_dbentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('core', ['DbEntry'])


    def backwards(self, orm):
        
        # Deleting model 'RequestStore'
        db.delete_table('core_requeststore')

        # Deleting model 'DbEntry'
        db.delete_table('core_dbentry')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.dbentry': {
            'Meta': {'object_name': 'DbEntry'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'core.requeststore': {
            'Meta': {'ordering': "['-created']", 'object_name': 'RequestStore'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'req_cookies': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'req_get': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'req_meta': ('django.db.models.fields.TextField', [], {}),
            'req_post': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'req_session': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'req_status_code': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['core']
