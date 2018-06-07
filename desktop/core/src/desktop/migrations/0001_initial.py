# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-06 18:55
from __future__ import unicode_literals

import desktop.models
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(db_index=True, help_text='App that this configuration belongs to.', max_length=32)),
                ('properties', models.TextField(default=b'[]', help_text='JSON-formatted default properties values.')),
                ('is_default', models.BooleanField(db_index=True, default=False)),
                ('groups', models.ManyToManyField(db_index=True, db_table=b'defaultconfiguration_groups', to='auth.Group')),
            ],
            options={
                'ordering': ['app', '-is_default', 'user'],
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'', max_length=255)),
                ('description', models.TextField(default=b'')),
                ('last_modified', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last modified')),
                ('version', models.SmallIntegerField(default=1, verbose_name='Schema version')),
                ('extra', models.TextField(default=b'')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Document2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'', max_length=255)),
                ('description', models.TextField(default=b'')),
                ('uuid', models.CharField(db_index=True, default=desktop.models.uuid_default, max_length=36)),
                ('type', models.CharField(db_index=True, default=b'', help_text='Type of document, e.g. Hive query, Oozie workflow, Search Dashboard...', max_length=32)),
                ('data', models.TextField(default=b'{}')),
                ('extra', models.TextField(default=b'')),
                ('search', models.TextField(blank=True, help_text='Searchable text for the document.', null=True)),
                ('last_modified', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Time last modified')),
                ('version', models.SmallIntegerField(db_index=True, default=1, verbose_name='Document version')),
                ('is_history', models.BooleanField(db_index=True, default=False)),
                ('is_managed', models.BooleanField(db_index=True, default=False, verbose_name='If managed under the cover by Hue and never by the user')),
                ('is_trashed', models.NullBooleanField(db_index=True, default=False, verbose_name='True if trashed')),
                ('dependencies', models.ManyToManyField(db_index=True, related_name='dependents', to='desktop.Document2')),
            ],
            options={
                'ordering': ['-last_modified', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Document2Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perms', models.CharField(choices=[(b'read', b'read'), (b'write', b'write'), (b'comment', b'comment')], db_index=True, default=b'read', max_length=10)),
                ('doc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='desktop.Document2')),
                ('groups', models.ManyToManyField(db_index=True, db_table=b'documentpermission2_groups', to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perms', models.CharField(choices=[(b'read', b'read'), (b'write', b'write')], default=b'read', max_length=10)),
                ('doc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='desktop.Document')),
                ('groups', models.ManyToManyField(db_index=True, db_table=b'documentpermission_groups', to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collect_usage', models.BooleanField(db_index=True, default=True)),
                ('tours_and_tutorials', models.BooleanField(db_index=True, default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=20)),
                ('value', models.TextField(max_length=4096)),
            ],
        ),
        migrations.CreateModel(
            name='HueUser',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='documenttag',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='documentpermission',
            name='users',
            field=models.ManyToManyField(db_index=True, db_table=b'documentpermission_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document2permission',
            name='users',
            field=models.ManyToManyField(db_index=True, db_table=b'documentpermission2_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='document2',
            name='owner',
            field=models.ForeignKey(help_text='Creator.', on_delete=django.db.models.deletion.CASCADE, related_name='doc2_owner', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
        migrations.AddField(
            model_name='document2',
            name='parent_directory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='desktop.Document2'),
        ),
        migrations.AddField(
            model_name='document',
            name='owner',
            field=models.ForeignKey(help_text='User who can own the job.', on_delete=django.db.models.deletion.CASCADE, related_name='doc_owner', to=settings.AUTH_USER_MODEL, verbose_name='Owner'),
        ),
        migrations.AddField(
            model_name='document',
            name='tags',
            field=models.ManyToManyField(db_index=True, to='desktop.DocumentTag'),
        ),
        migrations.AddField(
            model_name='defaultconfiguration',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Directory',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('desktop.document2',),
        ),
        migrations.AlterUniqueTogether(
            name='documenttag',
            unique_together=set([('owner', 'tag')]),
        ),
        migrations.AlterUniqueTogether(
            name='documentpermission',
            unique_together=set([('doc', 'perms')]),
        ),
        migrations.AlterUniqueTogether(
            name='document2permission',
            unique_together=set([('doc', 'perms')]),
        ),
        migrations.AlterUniqueTogether(
            name='document2',
            unique_together=set([('uuid', 'version', 'is_history')]),
        ),
        migrations.AlterUniqueTogether(
            name='document',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
