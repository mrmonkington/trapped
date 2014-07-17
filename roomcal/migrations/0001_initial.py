# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Room'
        db.create_table(u'roomcal_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('min_persons', self.gf('django.db.models.fields.IntegerField')()),
            ('max_persons', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'roomcal', ['Room'])

        # Adding model 'Slot'
        db.create_table(u'roomcal_slot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roomcal.Room'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('base_price', self.gf('roomcal.models.PriceField')(max_digits=6, decimal_places=2)),
            ('extra_person_price', self.gf('roomcal.models.PriceField')(max_digits=6, decimal_places=2)),
        ))
        db.send_create_signal(u'roomcal', ['Slot'])

        # Adding model 'Customer'
        db.create_table(u'roomcal_customer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('mobile_phone', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'roomcal', ['Customer'])

        # Adding model 'Order'
        db.create_table(u'roomcal_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roomcal.Customer'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'roomcal', ['Order'])

        # Adding model 'Booking'
        db.create_table(u'roomcal_booking', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slot', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['roomcal.Slot'], unique=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roomcal.Order'], null=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('num_persons', self.gf('django.db.models.fields.IntegerField')()),
            ('date_booked', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('customer_comments', self.gf('django.db.models.fields.TextField')(null=True)),
            ('admin_comments', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'roomcal', ['Booking'])

        # Adding model 'PartyMember'
        db.create_table(u'roomcal_partymember', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('booking', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roomcal.Booking'])),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('wants_internal_marketing', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'roomcal', ['PartyMember'])


    def backwards(self, orm):
        # Deleting model 'Room'
        db.delete_table(u'roomcal_room')

        # Deleting model 'Slot'
        db.delete_table(u'roomcal_slot')

        # Deleting model 'Customer'
        db.delete_table(u'roomcal_customer')

        # Deleting model 'Order'
        db.delete_table(u'roomcal_order')

        # Deleting model 'Booking'
        db.delete_table(u'roomcal_booking')

        # Deleting model 'PartyMember'
        db.delete_table(u'roomcal_partymember')


    models = {
        u'roomcal.booking': {
            'Meta': {'object_name': 'Booking'},
            'admin_comments': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'customer_comments': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'date_booked': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_persons': ('django.db.models.fields.IntegerField', [], {}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roomcal.Order']", 'null': 'True'}),
            'slot': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['roomcal.Slot']", 'unique': 'True'})
        },
        u'roomcal.customer': {
            'Meta': {'object_name': 'Customer'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mobile_phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'roomcal.order': {
            'Meta': {'object_name': 'Order'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roomcal.Customer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'roomcal.partymember': {
            'Meta': {'object_name': 'PartyMember'},
            'booking': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roomcal.Booking']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'wants_internal_marketing': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'roomcal.room': {
            'Meta': {'object_name': 'Room'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_persons': ('django.db.models.fields.IntegerField', [], {}),
            'min_persons': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'roomcal.slot': {
            'Meta': {'object_name': 'Slot'},
            'base_price': ('roomcal.models.PriceField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'extra_person_price': ('roomcal.models.PriceField', [], {'max_digits': '6', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['roomcal.Room']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['roomcal']