# Generated by Django 4.1.6 on 2023-03-17 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('courseID', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('courseName', models.CharField(max_length=100)),
                ('projectType', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('evaluationID', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('deadline', models.DateField()),
                ('evaluationDate', models.DateField()),
                ('evaluationCompleted', models.BooleanField(default=False)),
                ('evaluationRemarks', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('projectID', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('projectName', models.CharField(max_length=100)),
                ('projectDescription', models.TextField()),
                ('projectType', models.CharField(choices=[('Course Project', 'Course Project'), ('Research Project', 'Research Project')], default='Course Project', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CourseProject',
            fields=[
                ('projectID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Projects.project')),
                ('year', models.IntegerField()),
                ('midTermEvaluation', models.BooleanField(default=False)),
                ('midTermEvaluationDate', models.DateField(blank=True, null=True)),
                ('midTermEvaluationRemarks', models.TextField(blank=True, null=True)),
                ('endTermEvaluation', models.BooleanField(default=False)),
                ('endTermEvaluationDate', models.DateField(blank=True, null=True)),
                ('endTermEvaluationRemarks', models.TextField(blank=True, null=True)),
                ('semester', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ResearchProject',
            fields=[
                ('projectID', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Projects.project')),
                ('researchArea', models.CharField(max_length=100)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('requestID', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('requestDescription', models.TextField()),
                ('requestStatus', models.CharField(max_length=100)),
                ('supportingDocuments', models.FileField(blank=True, null=True, upload_to='documents/')),
                ('requestDate', models.DateField()),
                ('requestRemarks', models.TextField()),
                ('projectID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Projects.project')),
                ('requestFrom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.profile')),
                ('requestTo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Users.instructor')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100)),
                ('projectID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isApproved', models.BooleanField(default=False)),
                ('kerberosID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.student')),
                ('projectID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectInstructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isApproved', models.BooleanField(default=False)),
                ('kerberosID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.instructor')),
                ('projectID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectDocument',
            fields=[
                ('documentID', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('documentName', models.FileField(upload_to='documents/')),
                ('documentDescription', models.TextField()),
                ('uploadedOn', models.DateTimeField(auto_now_add=True)),
                ('projectID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.project')),
                ('uploadedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.profile')),
            ],
        ),
        migrations.AddConstraint(
            model_name='projecttag',
            constraint=models.UniqueConstraint(fields=('projectID', 'tag'), name='unique_project_tag'),
        ),
        migrations.AddConstraint(
            model_name='projectstudent',
            constraint=models.UniqueConstraint(fields=('projectID', 'kerberosID'), name='unique_project_student'),
        ),
        migrations.AddConstraint(
            model_name='projectinstructor',
            constraint=models.UniqueConstraint(fields=('projectID', 'kerberosID'), name='unique_project_instructor'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='projectID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.researchproject'),
        ),
        migrations.AddField(
            model_name='courseproject',
            name='courseID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Projects.course'),
        ),
    ]