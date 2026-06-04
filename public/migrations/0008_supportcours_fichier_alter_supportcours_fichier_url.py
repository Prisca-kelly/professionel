from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0007_remove_province_capitale_remove_province_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportcours',
            name='fichier',
            field=models.FileField(
                blank=True,
                help_text='Fichier uploadé (prioritaire sur l’URL si les deux sont renseignés).',
                max_length=500,
                null=True,
                upload_to='supports/%Y/%m/',
            ),
        ),
        migrations.AlterField(
            model_name='supportcours',
            name='fichier_url',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
