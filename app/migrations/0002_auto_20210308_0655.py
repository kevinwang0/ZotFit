# Generated by Django 3.1.5 on 2021-03-08 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='backDifficulty',
        ),
        migrations.RemoveField(
            model_name='member',
            name='bicepDifficulty',
        ),
        migrations.RemoveField(
            model_name='member',
            name='calfDifficulty',
        ),
        migrations.RemoveField(
            model_name='member',
            name='coreDifficulty',
        ),
        migrations.RemoveField(
            model_name='member',
            name='hamstringDifficulty',
        ),
        migrations.RemoveField(
            model_name='member',
            name='quadricepDifficulty',
        ),
        migrations.RemoveField(
            model_name='member',
            name='tricepDifficulty',
        ),
        migrations.AddField(
            model_name='member',
            name='benchDipDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='benchpressDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='bicepCurlDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='calfRaiseDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='chinupDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='crunchyFrogDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='deadBugDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='deadliftDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='diamondPushupDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='gluteBridgeDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='goodMorningDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='hammerCurlDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='inchwormDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='inwardCalfRaiseDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='jumpSquatDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='jumpingJackDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='latPulldownDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='lateralLungeDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='legRaiseDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='lowRowDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='lungeDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='medicineBallSlamDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='plankRowDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='plankTapDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='pressupDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='pullupDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='pushupDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='quadLegCurlDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='reverseLungeDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='reverseSnowAngelDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='romanianDeadliftDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='russianTwistDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='sealJumpDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='shoulderPressDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='singleCalfRaiseDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='situpDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='squatDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='supermanDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AddField(
            model_name='member',
            name='tricepExtensionDifficulty',
            field=models.DecimalField(decimal_places=1, default=0.5, max_digits=2),
        ),
        migrations.AlterField(
            model_name='member',
            name='goal',
            field=models.CharField(choices=[('L', 'Lose weight'), ('G', 'Gain muscle'), ('B', 'Improve general fitness / Both')], default='F', max_length=1),
        ),
    ]
