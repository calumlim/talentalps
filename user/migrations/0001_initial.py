# Generated by Django 3.1.2 on 2020-10-21 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('avatar', models.ImageField(upload_to=user.models.get_company_avatar_image_path, verbose_name='avatar')),
                ('company_name', models.CharField(max_length=150, verbose_name='company_name')),
                ('description', models.TextField(max_length=1200, verbose_name='description')),
                ('website', models.CharField(max_length=1000, verbose_name='website')),
                ('company_size', models.CharField(choices=[('1 - 10', '1 - 10 Employees'), ('10 - 50', '10 - 50 Employees'), ('50 - 250', '50 - 250 Employees'), ('250 - 500', '250 - 500 Employees'), ('500 - 1000', '500 - 1,000 Employees'), ('1000 - 5000', '1,000 - 5,000 Employees'), ('5000 - 10000', '5,000 - 10,000 Employees'), ('10000+', '10,000+ Employees')], max_length=50, verbose_name='company size')),
                ('company_type', models.CharField(choices=[('sole_proprietorship', 'Sole Proprietorship'), ('partnership', 'Partnership'), ('LLP', 'Limited Liability Partnership (LLP)'), ('SDN_BHD', 'Private Limited Company (SDN BHD)'), ('public_limited', 'Public Limited Company'), ('guarantee', 'Company Limited By Guarantee'), ('foreign', 'Foreign Company')], max_length=50, verbose_name='type')),
                ('founded', models.CharField(max_length=5, verbose_name='founded')),
                ('header_image', models.ImageField(upload_to=user.models.get_company_header_image_path, verbose_name='header image')),
                ('industry', models.CharField(choices=[('telecommunications', 'Telecommunications')], max_length=150, verbose_name='industry')),
                ('other_industry', models.CharField(blank=True, max_length=100, null=True, verbose_name='other industry')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='address')),
                ('postcode', models.PositiveIntegerField(blank=True, null=True, verbose_name='postcode')),
                ('state', models.CharField(blank=True, choices=[('johor', 'Johor'), ('kedah', 'Kedah'), ('kelantan', 'Kelantan'), ('melaka', 'Melaka'), ('negeri_sembilan', 'Negeri Sembilan'), ('pahang', 'Pahang'), ('penang', 'Penang'), ('perak', 'Perak'), ('perlis', 'Perlis'), ('sabah', 'Sabah'), ('sarawak', 'Sarawak'), ('selangor', 'Selangor'), ('terengganu', 'Terengganu'), ('kuala_lumpur', 'Wilayah Persekutuan Kuala Lumpur'), ('labuan', 'Wilayah Persekutuan Labuan'), ('putrajaya', 'Wilayah Persekutuan Putrajaya')], max_length=100, null=True, verbose_name='state')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='name')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='address')),
                ('postcode', models.PositiveIntegerField(blank=True, null=True, verbose_name='postcode')),
                ('state', models.CharField(blank=True, choices=[('johor', 'Johor'), ('kedah', 'Kedah'), ('kelantan', 'Kelantan'), ('melaka', 'Melaka'), ('negeri_sembilan', 'Negeri Sembilan'), ('pahang', 'Pahang'), ('penang', 'Penang'), ('perak', 'Perak'), ('perlis', 'Perlis'), ('sabah', 'Sabah'), ('sarawak', 'Sarawak'), ('selangor', 'Selangor'), ('terengganu', 'Terengganu'), ('kuala_lumpur', 'Wilayah Persekutuan Kuala Lumpur'), ('labuan', 'Wilayah Persekutuan Labuan'), ('putrajaya', 'Wilayah Persekutuan Putrajaya')], max_length=100, null=True, verbose_name='state')),
                ('contact', models.CharField(blank=True, max_length=15, null=True, verbose_name='contact')),
                ('is_employer', models.BooleanField(default=False, verbose_name='is employer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DailyStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('totaltraffic', models.PositiveIntegerField(verbose_name='total traffic')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.company', verbose_name='company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='company',
            name='userprofile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.userprofile', verbose_name='user profile'),
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10, verbose_name='gender')),
                ('nationality', models.CharField(choices=[('AF', 'Afghanistan'), ('AX', 'Aland Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'), ('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BT', 'Bhutan'), ('BO', 'Bolivia, Plurinational State of'), ('BQ', 'Bonaire, Sint Eustatius and Saba'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'), ('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'), ('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo, the Democratic Republic of the'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('CI', "Cote d'Ivoire"), ('HR', 'Croatia'), ('CU', 'Cuba'), ('CW', 'Curacao'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands (Malvinas)'), ('FO', 'Faroe Islands'), ('FJ', 'Fiji'), ('FI', 'Finland'), ('FR', 'France'), ('GF', 'French Guiana'), ('PF', 'French Polynesia'), ('TF', 'French Southern Territories'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'), ('DE', 'Germany'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GR', 'Greece'), ('GL', 'Greenland'), ('GD', 'Grenada'), ('GP', 'Guadeloupe'), ('GU', 'Guam'), ('GT', 'Guatemala'), ('GG', 'Guernsey'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HT', 'Haiti'), ('HM', 'Heard Island and McDonald Islands'), ('VA', 'Holy See (Vatican City State)'), ('HN', 'Honduras'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IS', 'Iceland'), ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran, Islamic Republic of'), ('IQ', 'Iraq'), ('IE', 'Ireland'), ('IM', 'Isle of Man'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'), ('JP', 'Japan'), ('JE', 'Jersey'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'), ('KI', 'Kiribati'), ('KP', "Korea, Democratic People's Republic of"), ('KR', 'Korea, Republic of'), ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', "Lao People's Democratic Republic"), ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'), ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'), ('MO', 'Macao'), ('MK', 'Macedonia, the former Yugoslav Republic of'), ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'), ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MQ', 'Martinique'), ('MR', 'Mauritania'), ('MU', 'Mauritius'), ('YT', 'Mayotte'), ('MX', 'Mexico'), ('FM', 'Micronesia, Federated States of'), ('MD', 'Moldova, Republic of'), ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MA', 'Morocco'), ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'), ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NC', 'New Caledonia'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'), ('NE', 'Niger'), ('NG', 'Nigeria'), ('NU', 'Niue'), ('NF', 'Norfolk Island'), ('MP', 'Northern Mariana Islands'), ('NO', 'Norway'), ('OM', 'Oman'), ('PK', 'Pakistan'), ('PW', 'Palau'), ('PS', 'Palestine, State of'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'), ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PN', 'Pitcairn'), ('PL', 'Poland'), ('PT', 'Portugal'), ('PR', 'Puerto Rico'), ('QA', 'Qatar'), ('RE', 'Reunion'), ('RO', 'Romania'), ('RU', 'Russian Federation'), ('RW', 'Rwanda'), ('BL', 'Saint Barthelemy'), ('SH', 'Saint Helena, Ascension and Tristan da Cunha'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'), ('MF', 'Saint Martin (French part)'), ('PM', 'Saint Pierre and Miquelon'), ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'), ('SM', 'San Marino'), ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'), ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'), ('SX', 'Sint Maarten (Dutch part)'), ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'), ('ZA', 'South Africa'), ('GS', 'South Georgia and the South Sandwich Islands'), ('SS', 'South Sudan'), ('ES', 'Spain'), ('LK', 'Sri Lanka'), ('SD', 'Sudan'), ('SR', 'Suriname'), ('SJ', 'Svalbard and Jan Mayen'), ('SZ', 'Swaziland'), ('SE', 'Sweden'), ('CH', 'Switzerland'), ('SY', 'Syrian Arab Republic'), ('TW', 'Taiwan, Province of China'), ('TJ', 'Tajikistan'), ('TZ', 'Tanzania, United Republic of'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'), ('TM', 'Turkmenistan'), ('TC', 'Turks and Caicos Islands'), ('TV', 'Tuvalu'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom'), ('US', 'United States'), ('UM', 'United States Minor Outlying Islands'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela, Bolivarian Republic of'), ('VN', 'Viet Nam'), ('VG', 'Virgin Islands, British'), ('VI', 'Virgin Islands, U.S.'), ('WF', 'Wallis and Futuna'), ('EH', 'Western Sahara'), ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe')], default='MY', max_length=50, verbose_name='nationality')),
                ('description', models.TextField(max_length=1200, verbose_name='description')),
                ('seeking_status', models.CharField(choices=[('active', 'Actively Seeking'), ('looking', 'Just looking around')], max_length=50, verbose_name='seeking status')),
                ('avatar', models.ImageField(upload_to=user.models.get_avatar_image_path, verbose_name='avatar')),
                ('header', models.ImageField(upload_to=user.models.get_header_image_path, verbose_name='header')),
                ('boost', models.BooleanField(default=False, verbose_name='boost')),
                ('userprofile', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='user.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
