# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("program", "0013_show_and_note_images"),
    ]

    operations = [
        migrations.RunSQL("ALTER TABLE program_host ADD FULLTEXT (name);"),
        migrations.RunSQL("ALTER TABLE program_note ADD FULLTEXT (title);"),
        migrations.RunSQL("ALTER TABLE program_show ADD FULLTEXT (name);"),
    ]
