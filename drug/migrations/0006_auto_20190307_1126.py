# Generated by Django 2.1.7 on 2019-03-07 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drug', '0005_auto_20190307_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredesc',
            name='desc_id',
            field=models.CharField(default='TBD', max_length=500, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ingredesc',
            name='ingredient_name',
            field=models.CharField(default='TBD', max_length=500),
        ),
        migrations.AlterField(
            model_name='ingredesc',
            name='one_liner',
            field=models.CharField(default='TBD', max_length=500),
        ),
        migrations.AlterField(
            model_name='ingredesc',
            name='one_liner_kr',
            field=models.CharField(default='TBD', max_length=500),
        ),
        migrations.AlterField(
            model_name='ingredesc',
            name='translate_status',
            field=models.CharField(default='TBD', max_length=500),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='ing_code',
            field=models.CharField(default='TBD', max_length=500, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ingreform',
            name='desc_id',
            field=models.CharField(default='TBD', max_length=500),
        ),
        migrations.AlterField(
            model_name='ingreform',
            name='form',
            field=models.CharField(default='TBD', max_length=500),
        ),
        migrations.AlterField(
            model_name='ingreform',
            name='ing_form_id',
            field=models.CharField(default='TBD', max_length=500, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='ingreform',
            name='ing_name_eng',
            field=models.CharField(default='TBD', max_length=500),
        ),
        migrations.AlterField(
            model_name='ingreform',
            name='ing_name_kr',
            field=models.CharField(default='TBD', max_length=500),
        ),
        migrations.AlterField(
            model_name='ingreform',
            name='note',
            field=models.CharField(default='TBD', max_length=500),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_code',
            field=models.CharField(default='TBD', max_length=500, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='registration',
            name='attach',
            field=models.CharField(default='TBD', max_length=10000),
        ),
        migrations.AlterField(
            model_name='registration',
            name='drug_class',
            field=models.CharField(default='TBD', max_length=500),
        ),
        migrations.AlterField(
            model_name='registration',
            name='exp_date',
            field=models.CharField(default='TBD', max_length=500),
        ),
        migrations.AlterField(
            model_name='registration',
            name='img_file',
            field=models.CharField(default='TBD', max_length=500),
        ),
        migrations.AlterField(
            model_name='registration',
            name='ing_code',
            field=models.CharField(default='TBD', max_length=500),
        ),
        migrations.AlterField(
            model_name='registration',
            name='manufac_id',
            field=models.CharField(default='TBD', max_length=500),
        ),
        migrations.AlterField(
            model_name='registration',
            name='manufacturer',
            field=models.CharField(default='TBD', max_length=500),
        ),
        migrations.AlterField(
            model_name='registration',
            name='reg_code',
            field=models.CharField(default='TBD', max_length=500, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='registration',
            name='storage',
            field=models.CharField(default='TBD', max_length=500),
        ),
    ]
