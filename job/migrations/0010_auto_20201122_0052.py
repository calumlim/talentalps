# Generated by Django 3.1.3 on 2020-11-21 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0009_auto_20201121_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joblisting',
            name='industry',
            field=models.CharField(choices=[('Telecommunications', 'Telecommunications'), ('Medical', 'Medical'), ('Actuarial Work, Pensions & Insurance', 'Actuarial Work, Pensions & Insurance'), ('Transport & Logistics', 'Transport & Logistics'), ('Airline/Aviation', 'Airline/Aviation'), ('Legal Services', 'Legal Services'), ('Performing Arts', 'Performing Arts'), ('Scientific Research', 'Scientific Research'), ('Psychology', 'Psychology'), ('Engineering, Manufacturing & Construction', 'Engineering, Manufacturing & Construction'), ('Creative', 'Creative'), ('Financial Management & Accountancy', 'Financial Management & Accountancy'), ('Defence & Public Protection', 'Defence & Public Protection'), ('Languages & TEFL', 'Languages & TEFL'), ('Buying, Selling, Retailing', 'Buying, Selling, Retailing'), ('Charity & Development work', 'Charity & Development work'), ('Publishing', 'Publishing'), ('Education', 'Education'), ('Natural Resources & Environment', 'Natural Resources & Environment'), ('Banking', 'Banking'), ('Government & Politics', 'Government & Politics'), ('Management Consultancy', 'Management Consultancy'), ('Advertising, PR & Marketing', 'Advertising, PR & Marketing'), ('Media', 'Media'), ('Arts, Culture & Heritage', 'Arts, Culture & Heritage'), ('Information Technology', 'Information Technology'), ('Social, Guidance, Community', 'Social, Guidance, Community'), ('HR & Recruitment', 'HR & Recruitment'), ('Healthcare & Psychology', 'Healthcare & Psychology'), ('Hospitality & Events Management', 'Hospitality & Events Management')], max_length=80, verbose_name='industry'),
        ),
        migrations.AlterField(
            model_name='joblisting',
            name='job_functions',
            field=models.CharField(choices=[('Legal', 'Legal'), ('Administrative', 'Administrative'), ('Media & Public Relations (PR)', 'Media & Public Relations (PR)'), ('Information Technology (IT)', 'Information Technology (IT)'), ('Property Management', 'Property Management'), ('Pharmaceuticals', 'Pharmaceuticals'), ('Healthcare', 'Healthcare'), ('Retail', 'Retail'), ('Hospitality & Tourism', 'Hospitality & Tourism'), ('Education', 'Education'), ('Marketing', 'Marketing'), ('Supply Chain & Logistics', 'Supply Chain & Logistics'), ('Engineering', 'Engineering'), ('Public Service & Security', 'Public Service & Security'), ('Accounting', 'Accounting'), ('Human Resources (HR)', 'Human Resources (HR)'), ('Sales', 'Sales'), ('Customer Service', 'Customer Service'), ('Real Estate', 'Real Estate'), ('Production', 'Production'), ('Finance', 'Finance')], max_length=80, verbose_name='job functions'),
        ),
    ]
