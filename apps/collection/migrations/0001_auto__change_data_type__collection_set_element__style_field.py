# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from oscar.core.compat import AUTH_USER_MODEL, AUTH_USER_MODEL_NAME


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CollectionSetElement.style'
        db.alter_column('collection_set_element', 'style',
                      self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True))

    def backwards(self, orm):
        # Deleting field 'CollectionSetElement.style'
        db.delete_column('collection_set_element', 'style')

    complete_apps = ['collection']