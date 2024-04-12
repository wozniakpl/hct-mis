# Generated by Django 3.2.25 on 2024-04-12 16:50

from django.db import migrations, models
import hct_mis_api.apps.account.models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0123_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='transaction_status_blockchain',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='transaction_status_blockchain',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='cashplan',
            name='delivery_type',
            field=models.CharField(choices=[('Cardless cash withdrawal', 'Cardless cash withdrawal'), ('Cash', 'Cash'), ('Cash by FSP', 'Cash by FSP'), ('Cheque', 'Cheque'), ('Deposit to Card', 'Deposit to Card'), ('Mobile Money', 'Mobile Money'), ('Pre-paid card', 'Pre-paid card'), ('Referral', 'Referral'), ('Transfer', 'Transfer'), ('Transfer to Account', 'Transfer to Account'), ('Voucher', 'Voucher'), ('Transfer to Digital Wallet', 'Transfer to Digital Wallet')], db_index=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='deliverymechanismperpaymentplan',
            name='delivery_mechanism',
            field=models.CharField(choices=[('Cardless cash withdrawal', 'Cardless cash withdrawal'), ('Cash', 'Cash'), ('Cash by FSP', 'Cash by FSP'), ('Cheque', 'Cheque'), ('Deposit to Card', 'Deposit to Card'), ('Mobile Money', 'Mobile Money'), ('Pre-paid card', 'Pre-paid card'), ('Referral', 'Referral'), ('Transfer', 'Transfer'), ('Transfer to Account', 'Transfer to Account'), ('Voucher', 'Voucher'), ('Transfer to Digital Wallet', 'Transfer to Digital Wallet')], db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='financialserviceprovider',
            name='delivery_mechanisms',
            field=hct_mis_api.apps.account.models.HorizontalChoiceArrayField(base_field=models.CharField(choices=[('Cardless cash withdrawal', 'Cardless cash withdrawal'), ('Cash', 'Cash'), ('Cash by FSP', 'Cash by FSP'), ('Cheque', 'Cheque'), ('Deposit to Card', 'Deposit to Card'), ('Mobile Money', 'Mobile Money'), ('Pre-paid card', 'Pre-paid card'), ('Referral', 'Referral'), ('Transfer', 'Transfer'), ('Transfer to Account', 'Transfer to Account'), ('Voucher', 'Voucher'), ('Transfer to Digital Wallet', 'Transfer to Digital Wallet')], max_length=32), size=None),
        ),
        migrations.AlterField(
            model_name='financialserviceproviderxlsxtemplate',
            name='columns',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('payment_id', 'Payment ID'), ('household_id', 'Household ID'), ('household_size', 'Household Size'), ('collector_name', 'Collector Name'), ('alternate_collector_full_name', 'Alternate collector Full Name'), ('alternate_collector_given_name', 'Alternate collector Given Name'), ('alternate_collector_middle_name', 'Alternate collector Middle Name'), ('alternate_collector_phone_no', 'Alternate collector phone number'), ('alternate_collector_document_numbers', 'Alternate collector Document numbers'), ('alternate_collector_sex', 'Alternate collector Gender'), ('payment_channel', 'Payment Channel'), ('fsp_name', 'FSP Name'), ('currency', 'Currency'), ('entitlement_quantity', 'Entitlement Quantity'), ('entitlement_quantity_usd', 'Entitlement Quantity USD'), ('delivered_quantity', 'Delivered Quantity'), ('delivery_date', 'Delivery Date'), ('reference_id', 'Reference id'), ('reason_for_unsuccessful_payment', 'Reason for unsuccessful payment'), ('order_number', 'Order Number'), ('token_number', 'Token Number'), ('additional_collector_name', 'Additional Collector Name'), ('additional_document_type', 'Additional Document Type'), ('additional_document_number', 'Additional Document Number'), ('registration_token', 'Registration Token'), ('status', 'Status'), ('transaction_status_blockchain', 'Transaction Status on the Blockchain')], default=['payment_id', 'household_id', 'household_size', 'collector_name', 'alternate_collector_full_name', 'alternate_collector_given_name', 'alternate_collector_middle_name', 'alternate_collector_phone_no', 'alternate_collector_document_numbers', 'alternate_collector_sex', 'payment_channel', 'fsp_name', 'currency', 'entitlement_quantity', 'entitlement_quantity_usd', 'delivered_quantity', 'delivery_date', 'reference_id', 'reason_for_unsuccessful_payment', 'order_number', 'token_number', 'additional_collector_name', 'additional_document_type', 'additional_document_number', 'registration_token', 'status', 'transaction_status_blockchain'], help_text='Select the columns to include in the report', max_length=1000, verbose_name='Columns'),
        ),
        migrations.AlterField(
            model_name='financialserviceproviderxlsxtemplate',
            name='core_fields',
            field=hct_mis_api.apps.account.models.HorizontalChoiceArrayField(base_field=models.CharField(blank=True, choices=[('age', 'Age (calculated)'), ('residence_status', 'Residence status'), ('consent', 'Do you consent?'), ('consent_sign', 'Do you consent?'), ('country_origin', 'Country of Origin'), ('country', 'Country of registration'), ('address', 'Address'), ('zip_code', 'Zip code'), ('admin1', 'Household resides in which ${admin1_h_c}?'), ('admin2', 'Household resides in which ${admin2_h_c}?'), ('admin3', 'Household resides in which ${admin3_h_c}?'), ('admin4', 'Household resides in which ${admin4_h_c}?'), ('geopoint', 'Geolocation'), ('unhcr_id', 'UNHCR Case ID'), ('returnee', 'Is this a returnee household?'), ('size', 'What is the household size?'), ('fchild_hoh', 'Child is female and head of household'), ('child_hoh', 'Child is head of household'), ('relationship', 'Relationship to head of household'), ('full_name', 'Full name'), ('given_name', 'Given name'), ('middle_name', 'Middle name(s)'), ('family_name', 'Family name'), ('sex', 'Gender'), ('birth_date', 'Birth date'), ('estimated_birth_date', 'Estimated birth date?'), ('photo', "Individual's photo"), ('marital_status', 'Marital status'), ('phone_no', 'Phone number'), ('who_answers_phone', 'Who answers this phone?'), ('phone_no_alternative', 'Alternative phone number'), ('who_answers_alt_phone', 'Who answers this (alt) phone?'), ('registration_method', 'Method of collection (e.g. HH survey, Community, etc.)'), ('collect_individual_data', "Will you be collecting all member Individuals' data?"), ('currency', 'Which currency will be used for financial questions?'), ('birth_certificate_no', 'Birth certificate number'), ('birth_certificate_issuer', 'Issuing country of birth certificate'), ('birth_certificate_photo', 'Birth certificate photo'), ('tax_id_no', 'Tax identification number'), ('tax_id_issuer', 'Issuing country of tax identification'), ('tax_id_photo', 'Tax identification photo'), ('drivers_license_no', "Driver's license number"), ('drivers_license_issuer', "Issuing country of driver's license"), ('drivers_license_photo', "Driver's license photo"), ('electoral_card_no', 'Electoral card number'), ('electoral_card_issuer', 'Issuing country of electoral card'), ('electoral_card_photo', 'Electoral card photo'), ('unhcr_id_no', 'UNHCR ID number'), ('unhcr_id_issuer', 'Issuing entity of UNHCR ID'), ('unhcr_id_photo', 'UNHCR ID photo'), ('national_passport', 'National passport number'), ('national_passport_issuer', 'Issuing country of national passport'), ('national_passport_photo', 'National passport photo'), ('national_id_no', 'National ID number'), ('national_id_issuer', 'Issuing country of national ID'), ('national_id_photo', 'National ID photo'), ('scope_id_no', 'WFP Scope ID number'), ('scope_id_issuer', 'Issuing entity of SCOPE ID'), ('scope_id_photo', 'WFP Scope ID photo'), ('other_id_type', 'If other type of ID, specify the type'), ('other_id_no', 'Other ID number'), ('other_id_issuer', 'Issuing country of other ID'), ('other_id_photo', 'ID photo'), ('female_age_group_0_5_count', 'Females Age 0 - 5'), ('female_age_group_6_11_count', 'Females Age 6 - 11'), ('female_age_group_12_17_count', 'Females Age 12 - 17'), ('female_age_group_18_59_count', 'Females Age 18 - 59'), ('female_age_group_60_count', 'Females Age 60 +'), ('pregnant_count', 'Pregnant count'), ('male_age_group_0_5_count', 'Males Age 0 - 5'), ('male_age_group_6_11_count', 'Males Age 6 - 11'), ('male_age_group_12_17_count', 'Males Age 12 - 17'), ('male_age_group_18_59_count', 'Males Age 18 - 59'), ('male_age_group_60_count', 'Males Age 60 +'), ('female_age_group_0_5_disabled_count', 'Females age 0 - 5 with disability'), ('female_age_group_6_11_disabled_count', 'Females age 6 - 11 with disability'), ('female_age_group_12_17_disabled_count', 'Females age 12 - 17 with disability'), ('female_age_group_18_59_disabled_count', 'Females Age 18 - 59 with disability'), ('female_age_group_60_disabled_count', 'Female members with Disability age 60 +'), ('male_age_group_0_5_disabled_count', 'Males age 0 - 5 with disability'), ('male_age_group_6_11_disabled_count', 'Males age 6 - 11 with disability'), ('male_age_group_12_17_disabled_count', 'Males age 12 - 17 with disability'), ('male_age_group_18_59_disabled_count', 'Males Age 18 - 59 with disability'), ('male_age_group_60_disabled_count', 'Male members with Disability age 60 +'), ('pregnant', 'Is the individual pregnant?'), ('work_status', 'Does the individual have paid employment in the current month?'), ('observed_disability', 'Does the individual have disability?'), ('seeing_disability', 'If the individual has difficulty seeing, what is the severity?'), ('hearing_disability', 'If the individual has difficulty hearing, what is the severity?'), ('physical_disability', 'If the individual has difficulty walking or climbing steps, what is the severity?'), ('memory_disability', 'If the individual has difficulty remembering or concentrating, what is the severity?'), ('selfcare_disability', 'Do you have difficulty (with self-care such as) washing all over or dressing'), ('comms_disability', 'If the individual has difficulty communicating, what is the severity?'), ('fchild_hoh', 'Female child headed household'), ('child_hoh', 'Child headed household'), ('village', 'Village'), ('deviceid', 'Device ID'), ('name_enumerator', 'Name of the enumerator'), ('org_enumerator', 'Organization of the enumerator'), ('consent_sharing', 'Which organizations may we share your information with?'), ('org_name_enumerator', 'Name of partner organization'), ('disability', 'Individual is disabled?'), ('first_registration_date', 'First individual registration date'), ('first_registration_date', 'First household registration date'), ('number_of_children', 'What is the number of children in the household?'), ('has_phone_number', 'Has phone number?'), ('has_tax_id_number', 'Has tax ID number?'), ('has_the_bank_account_number', 'Has the bank account number?'), ('role', 'Role'), ('registration_data_import', 'Registration Data Import'), ('unicef_id', 'Household unicef id'), ('unicef_id', 'Individual unicef id'), ('admin_area_title', 'Household resides in which admin area?'), ('start', 'Data collection start date'), ('end', 'Data collection end date'), ('primary_collector_id', 'List of primary collectors ids, separated by a semicolon'), ('alternate_collector_id', 'List of alternate collectors ids, separated by a semicolon'), ('household_id', 'Household ID'), ('household_id', 'Household ID'), ('email', 'Individual email'), ('preferred_language', 'Preferred language'), ('age_at_registration', 'Age at registration'), ('account_holder_name', 'Account holder name'), ('bank_branch_name', 'Bank branch name'), ('wallet_name', 'Wallet Name'), ('blockchain_name', 'Blockchain Name'), ('wallet_address', 'Wallet Address'), ('index_id', 'Index ID'), ('full_name', 'Full name'), ('given_name', 'Given name'), ('middle_name', 'Middle name(s)'), ('family_name', 'Family name'), ('sex', 'Gender'), ('birth_date', 'Birth date'), ('estimated_birth_date', 'Estimated birth date?'), ('photo', "Individual's photo"), ('address', 'Address'), ('country_origin', 'Country of Origin'), ('country', 'Country of registration'), ('zip_code', 'Zip code'), ('admin1', 'Social worker resides in which ${admin1_i_c}?'), ('admin2', 'Social worker resides in which ${admin2_i_c}?'), ('admin3', 'Social worker resides in which ${admin3_i_c}?'), ('admin4', 'Social worker resides in which ${admin4_i_c}?'), ('residence_status', 'Residence status'), ('consent', 'Do you consent?'), ('consent_sign', 'Do you consent?'), ('geopoint', 'Geolocation'), ('unhcr_id', 'UNHCR Case ID'), ('returnee', 'Is this a returnee household?'), ('registration_method', 'Method of collection (e.g. HH survey, Community, etc.)'), ('currency', 'Which currency will be used for financial questions?'), ('village', 'Village'), ('deviceid', 'Device ID'), ('name_enumerator', 'Name of the enumerator'), ('org_enumerator', 'Organization of the enumerator'), ('consent_sharing', 'Which organizations may we share your information with?'), ('org_name_enumerator', 'Name of partner organization'), ('age', 'Age (calculated)'), ('fchild_hoh', 'Child is female and head of household'), ('child_hoh', 'Child is head of household'), ('relationship', 'Relationship to head of household'), ('marital_status', 'Marital status'), ('phone_no', 'Phone number'), ('who_answers_phone', 'Who answers this phone?'), ('phone_no_alternative', 'Alternative phone number'), ('who_answers_alt_phone', 'Who answers this (alt) phone?'), ('birth_certificate_no', 'Birth certificate number'), ('birth_certificate_issuer', 'Issuing country of birth certificate'), ('birth_certificate_photo', 'Birth certificate photo'), ('tax_id_no', 'Tax identification number'), ('tax_id_issuer', 'Issuing country of tax identification'), ('tax_id_photo', 'Tax identification photo'), ('drivers_license_no', "Driver's license number"), ('drivers_license_issuer', "Issuing country of driver's license"), ('drivers_license_photo', "Driver's license photo"), ('electoral_card_no', 'Electoral card number'), ('electoral_card_issuer', 'Issuing country of electoral card'), ('electoral_card_photo', 'Electoral card photo'), ('unhcr_id_no', 'UNHCR ID number'), ('unhcr_id_issuer', 'Issuing entity of UNHCR ID'), ('unhcr_id_photo', 'UNHCR ID photo'), ('national_passport', 'National passport number'), ('national_passport_issuer', 'Issuing country of national passport'), ('national_passport_photo', 'National passport photo'), ('national_id_no', 'National ID number'), ('national_id_issuer', 'Issuing country of national ID'), ('national_id_photo', 'National ID photo'), ('scope_id_no', 'WFP Scope ID number'), ('scope_id_issuer', 'Issuing entity of SCOPE ID'), ('scope_id_photo', 'WFP Scope ID photo'), ('other_id_type', 'If other type of ID, specify the type'), ('other_id_no', 'Other ID number'), ('other_id_issuer', 'Issuing country of other ID'), ('other_id_photo', 'ID photo'), ('pregnant', 'Is the individual pregnant?'), ('work_status', 'Does the individual have paid employment in the current month?'), ('observed_disability', 'Does the individual have disability?'), ('seeing_disability', 'If the individual has difficulty seeing, what is the severity?'), ('hearing_disability', 'If the individual has difficulty hearing, what is the severity?'), ('physical_disability', 'If the individual has difficulty walking or climbing steps, what is the severity?'), ('memory_disability', 'If the individual has difficulty remembering or concentrating, what is the severity?'), ('selfcare_disability', 'Do you have difficulty (with self-care such as) washing all over or dressing'), ('comms_disability', 'If the individual has difficulty communicating, what is the severity?'), ('disability', 'Individual is disabled?'), ('first_registration_date', 'First individual registration date'), ('primary_collector_id', 'List of primary collectors ids, separated by a semicolon'), ('alternate_collector_id', 'List of alternate collectors ids, separated by a semicolon'), ('email', 'Individual email'), ('preferred_language', 'Preferred language'), ('age_at_registration', 'Age at registration'), ('account_holder_name', 'Account holder name'), ('bank_branch_name', 'Bank branch name'), ('bank_name', 'Bank name'), ('bank_account_number', 'Bank account number'), ('debit_card_issuer', 'Debit Card Issuer'), ('debit_card_number', 'Debit card number'), ('payment_delivery_phone_no', 'Payment delivery phone number'), ('wallet_name', 'Wallet Name'), ('blockchain_name', 'Blockchain Name'), ('wallet_address', 'Wallet Address'), ('bank_name', 'Bank name'), ('bank_account_number', 'Bank account number'), ('debit_card_issuer', 'Debit Card Issuer'), ('debit_card_number', 'Debit card number'), ('payment_delivery_phone_no', 'Payment delivery phone number')], max_length=255), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='fspxlsxtemplateperdeliverymechanism',
            name='delivery_mechanism',
            field=models.CharField(choices=[('Cardless cash withdrawal', 'Cardless cash withdrawal'), ('Cash', 'Cash'), ('Cash by FSP', 'Cash by FSP'), ('Cheque', 'Cheque'), ('Deposit to Card', 'Deposit to Card'), ('Mobile Money', 'Mobile Money'), ('Pre-paid card', 'Pre-paid card'), ('Referral', 'Referral'), ('Transfer', 'Transfer'), ('Transfer to Account', 'Transfer to Account'), ('Voucher', 'Voucher'), ('Transfer to Digital Wallet', 'Transfer to Digital Wallet')], max_length=255, verbose_name='Delivery Mechanism'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='delivery_type',
            field=models.CharField(choices=[('Cardless cash withdrawal', 'Cardless cash withdrawal'), ('Cash', 'Cash'), ('Cash by FSP', 'Cash by FSP'), ('Cheque', 'Cheque'), ('Deposit to Card', 'Deposit to Card'), ('Mobile Money', 'Mobile Money'), ('Pre-paid card', 'Pre-paid card'), ('Referral', 'Referral'), ('Transfer', 'Transfer'), ('Transfer to Account', 'Transfer to Account'), ('Voucher', 'Voucher'), ('Transfer to Digital Wallet', 'Transfer to Digital Wallet')], max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='paymentplan',
            name='currency',
            field=models.CharField(choices=[('', 'None'), ('AED', 'United Arab Emirates dirham'), ('AFN', 'Afghan afghani'), ('ALL', 'Albanian lek'), ('AMD', 'Armenian dram'), ('ANG', 'Netherlands Antillean guilder'), ('AOA', 'Angolan kwanza'), ('ARS', 'Argentine peso'), ('AUD', 'Australian dollar'), ('AWG', 'Aruban florin'), ('AZN', 'Azerbaijani manat'), ('BAM', 'Bosnia and Herzegovina convertible mark'), ('BBD', 'Barbados dollar'), ('BDT', 'Bangladeshi taka'), ('BGN', 'Bulgarian lev'), ('BHD', 'Bahraini dinar'), ('BIF', 'Burundian franc'), ('BMD', 'Bermudian dollar'), ('BND', 'Brunei dollar'), ('BOB', 'Boliviano'), ('BOV', 'Bolivian Mvdol (funds code)'), ('BRL', 'Brazilian real'), ('BSD', 'Bahamian dollar'), ('BTN', 'Bhutanese ngultrum'), ('BWP', 'Botswana pula'), ('BYN', 'Belarusian ruble'), ('BZD', 'Belize dollar'), ('CAD', 'Canadian dollar'), ('CDF', 'Congolese franc'), ('CHF', 'Swiss franc'), ('CLP', 'Chilean peso'), ('CNY', 'Chinese yuan'), ('COP', 'Colombian peso'), ('CRC', 'Costa Rican colon'), ('CUC', 'Cuban convertible peso'), ('CUP', 'Cuban peso'), ('CVE', 'Cape Verdean escudo'), ('CZK', 'Czech koruna'), ('DJF', 'Djiboutian franc'), ('DKK', 'Danish krone'), ('DOP', 'Dominican peso'), ('DZD', 'Algerian dinar'), ('EGP', 'Egyptian pound'), ('ERN', 'Eritrean nakfa'), ('ETB', 'Ethiopian birr'), ('EUR', 'Euro'), ('FJD', 'Fiji dollar'), ('FKP', 'Falkland Islands pound'), ('GBP', 'Pound sterling'), ('GEL', 'Georgian lari'), ('GHS', 'Ghanaian cedi'), ('GIP', 'Gibraltar pound'), ('GMD', 'Gambian dalasi'), ('GNF', 'Guinean franc'), ('GTQ', 'Guatemalan quetzal'), ('GYD', 'Guyanese dollar'), ('HKD', 'Hong Kong dollar'), ('HNL', 'Honduran lempira'), ('HRK', 'Croatian kuna'), ('HTG', 'Haitian gourde'), ('HUF', 'Hungarian forint'), ('IDR', 'Indonesian rupiah'), ('ILS', 'Israeli new shekel'), ('INR', 'Indian rupee'), ('IQD', 'Iraqi dinar'), ('IRR', 'Iranian rial'), ('ISK', 'Icelandic króna'), ('JMD', 'Jamaican dollar'), ('JOD', 'Jordanian dinar'), ('JPY', 'Japanese yen'), ('KES', 'Kenyan shilling'), ('KGS', 'Kyrgyzstani som'), ('KHR', 'Cambodian riel'), ('KMF', 'Comoro franc'), ('KPW', 'North Korean won'), ('KRW', 'South Korean won'), ('KWD', 'Kuwaiti dinar'), ('KYD', 'Cayman Islands dollar'), ('KZT', 'Kazakhstani tenge'), ('LAK', 'Lao kip'), ('LBP', 'Lebanese pound'), ('LKR', 'Sri Lankan rupee'), ('LRD', 'Liberian dollar'), ('LSL', 'Lesotho loti'), ('LYD', 'Libyan dinar'), ('MAD', 'Moroccan dirham'), ('MDL', 'Moldovan leu'), ('MGA', 'Malagasy ariary'), ('MKD', 'Macedonian denar'), ('MMK', 'Myanmar kyat'), ('MNT', 'Mongolian tögrög'), ('MOP', 'Macanese pataca'), ('MRU', 'Mauritanian ouguiya'), ('MUR', 'Mauritian rupee'), ('MVR', 'Maldivian rufiyaa'), ('MWK', 'Malawian kwacha'), ('MXN', 'Mexican peso'), ('MYR', 'Malaysian ringgit'), ('MZN', 'Mozambican metical'), ('NAD', 'Namibian dollar'), ('NGN', 'Nigerian naira'), ('NIO', 'Nicaraguan córdoba'), ('NOK', 'Norwegian krone'), ('NPR', 'Nepalese rupee'), ('NZD', 'New Zealand dollar'), ('OMR', 'Omani rial'), ('PAB', 'Panamanian balboa'), ('PEN', 'Peruvian sol'), ('PGK', 'Papua New Guinean kina'), ('PHP', 'Philippine peso'), ('PKR', 'Pakistani rupee'), ('PLN', 'Polish złoty'), ('PYG', 'Paraguayan guaraní'), ('QAR', 'Qatari riyal'), ('RON', 'Romanian leu'), ('RSD', 'Serbian dinar'), ('RUB', 'Russian ruble'), ('RWF', 'Rwandan franc'), ('SAR', 'Saudi riyal'), ('SBD', 'Solomon Islands dollar'), ('SCR', 'Seychelles rupee'), ('SDG', 'Sudanese pound'), ('SEK', 'Swedish krona/kronor'), ('SGD', 'Singapore dollar'), ('SHP', 'Saint Helena pound'), ('SLL', 'Sierra Leonean leone'), ('SOS', 'Somali shilling'), ('SRD', 'Surinamese dollar'), ('SSP', 'South Sudanese pound'), ('STN', 'São Tomé and Príncipe dobra'), ('SVC', 'Salvadoran colón'), ('SYP', 'Syrian pound'), ('SZL', 'Swazi lilangeni'), ('THB', 'Thai baht'), ('TJS', 'Tajikistani somoni'), ('TMT', 'Turkmenistan manat'), ('TND', 'Tunisian dinar'), ('TOP', 'Tongan paʻanga'), ('TRY', 'Turkish lira'), ('TTD', 'Trinidad and Tobago dollar'), ('TWD', 'New Taiwan dollar'), ('TZS', 'Tanzanian shilling'), ('UAH', 'Ukrainian hryvnia'), ('UGX', 'Ugandan shilling'), ('USD', 'United States dollar'), ('UYU', 'Uruguayan peso'), ('UYW', 'Unidad previsional[14]'), ('UZS', 'Uzbekistan som'), ('VES', 'Venezuelan bolívar soberano'), ('VND', 'Vietnamese đồng'), ('VUV', 'Vanuatu vatu'), ('WST', 'Samoan tala'), ('XAF', 'CFA franc BEAC'), ('XAG', 'Silver (one troy ounce)'), ('XAU', 'Gold (one troy ounce)'), ('XCD', 'East Caribbean dollar'), ('XOF', 'CFA franc BCEAO'), ('XPF', 'CFP franc (franc Pacifique)'), ('YER', 'Yemeni rial'), ('ZAR', 'South African rand'), ('ZMW', 'Zambian kwacha'), ('ZWL', 'Zimbabwean dollar'), ('USDC', 'Digital currency')], max_length=4),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='delivery_type',
            field=models.CharField(choices=[('Cardless cash withdrawal', 'Cardless cash withdrawal'), ('Cash', 'Cash'), ('Cash by FSP', 'Cash by FSP'), ('Cheque', 'Cheque'), ('Deposit to Card', 'Deposit to Card'), ('Mobile Money', 'Mobile Money'), ('Pre-paid card', 'Pre-paid card'), ('Referral', 'Referral'), ('Transfer', 'Transfer'), ('Transfer to Account', 'Transfer to Account'), ('Voucher', 'Voucher'), ('Transfer to Digital Wallet', 'Transfer to Digital Wallet')], max_length=32, null=True),
        ),
    ]
