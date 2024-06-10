# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    # this works with mysql 5.6, prior to this the engine needs to be MyISAM
    # changing the engine does not work with 5.5 and the program_show tabl
    dependencies = [
        ("program", "0013_show_and_note_images"),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE program_host ADD FULLTEXT (name);",
            reverse_sql="DROP INDEX name ON program_host;"
        ),
        migrations.RunSQL(
            sql="ALTER TABLE program_note ADD FULLTEXT (title);",
            reverse_sql="DROP INDEX title ON program_note;"),
        migrations.RunSQL(
            sql="ALTER TABLE program_show ADD FULLTEXT (name);",
            reverse_sql="DROP INDEX name ON program_show;"
        ),
    ]
