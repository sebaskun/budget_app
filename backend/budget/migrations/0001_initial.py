# Generated by Django 2.0.2 on 2019-05-29 07:08

import backend.core.utils
from decimal import Decimal
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('code', backend.core.utils.CharNullField(blank=True, max_length=15, null=True, verbose_name='código')),
                ('title', models.TextField(default='Sin título', verbose_name='Titulo')),
                ('location', backend.core.utils.CharNullField(blank=True, max_length=150, null=True, verbose_name='Locación')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='Resumen')),
                ('exchange_rate', models.DecimalField(decimal_places=3, default=Decimal('1.000'), max_digits=10, verbose_name='tipo de cambio')),
                ('base_amount', models.DecimalField(decimal_places=6, default=Decimal('0.00'), max_digits=15, verbose_name='importe base')),
                ('deadline', models.DateField(blank=True, null=True, verbose_name='fecha límite')),
                ('currency', models.CharField(choices=[('S', 'S/'), ('D', '$')], default='D', max_length=1, verbose_name='moneda')),
                ('status', models.CharField(choices=[('WA', 'pendiente'), ('NW', 'nuevo'), ('SU', 'superado'), ('CA', 'cancelado'), ('TC', 'por confirmar'), ('UD', 'sin fecha')], default='NW', max_length=2, verbose_name='estado')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='posición')),
                ('is_archived', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('workdays_per_month', models.DecimalField(decimal_places=2, default=30, max_digits=5, verbose_name='días laborables por mes')),
                ('normal_working_hours', models.DecimalField(decimal_places=2, default=8, max_digits=5, verbose_name='horas laborables del día')),
                ('ratio_manpower', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='coeficiente de paso de mano de obra')),
                ('ratio_material', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='coeficiente de paso de material')),
                ('ratio_equipment', models.DecimalField(decimal_places=5, default=Decimal('1.00'), max_digits=8, verbose_name='coeficiente de paso de equipo')),
                ('ratio_equipo_reparacion_reposicion', models.DecimalField(decimal_places=2, default=Decimal('15.00'), max_digits=5, verbose_name='ratio de equipos rep resp')),
                ('ratio_lubricante', models.DecimalField(decimal_places=2, default=Decimal('20.00'), max_digits=5, verbose_name='ratio del lubricante')),
                ('ratio_subcontract', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='coeficiente de paso de subcontrato')),
                ('scheduled_completion', models.DecimalField(decimal_places=2, default=1, max_digits=5, verbose_name='plazo de la obra (meses)')),
                ('scheduled_completion_extra', models.DecimalField(decimal_places=2, default=2, max_digits=5, verbose_name='plazo extra de la obra (meses)')),
                ('ratio_guarantee_faithful_compliance', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='emisión de carta de fianza de fiel cumplimiento')),
                ('ratio_guarantee_advance', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='emisión de carta de fianza por adelanto')),
                ('ratio2_guarantee_faithful_compliance', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='emisión de carta de fianza de fiel cumplimiento')),
                ('ratio2_guarantee_advance', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='emisión de carta de fianza por adelanto')),
                ('ratio_civil_liability_policy', models.DecimalField(decimal_places=6, default=1, max_digits=9, verbose_name='poliza de responsabilidad civil')),
                ('ratio_incidentals_manpowers', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='imprevistos mano de obra')),
                ('ratio_incidentals_equipments', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='imprevistos equipos y herramientas')),
                ('ratio_incidentals_materials', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='imprevistos materiales')),
                ('ratio_incidentals_subcontracts', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='imprevistos subcontratos')),
                ('ratio_incidentals', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='ratio_imprevistos')),
                ('ratio_over_head_manpowers', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='gastos generales mano de obra')),
                ('ratio_over_head_equipments', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='gastos generales equipos y herramientas')),
                ('ratio_over_head_materials', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='gastos generales materiales')),
                ('ratio_over_head_subcontracts', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='gastos generales subcontratos')),
                ('ratio_over_head', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='porcentaje gastos generales')),
                ('ratio_profit_manpowers', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='beneficio mano de obra')),
                ('ratio_profit_equipments', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='beneficio equipos y herramientas')),
                ('ratio_profit_materials', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='beneficio materiales')),
                ('ratio_profit_subcontracts', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='beneficio subcontratos')),
                ('ratio_profit', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='beneficio')),
                ('ratio_financial_expenses', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='gastos financieros')),
                ('ratio_itf_check_tax', models.DecimalField(decimal_places=5, default=1, max_digits=8, verbose_name='impuesto cheque itf')),
                ('ratio_gastos_generales_diff', models.DecimalField(decimal_places=5, default=0, max_digits=8, verbose_name='gastos generales diferenciado')),
                ('ratio_utilidad_diff', models.DecimalField(decimal_places=5, default=0, max_digits=8, verbose_name='utilidad diferenciado')),
                ('tree', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='arbol')),
                ('meses_obra', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='meses de obra')),
                ('meses_epp', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True, verbose_name='meses de epp')),
                ('vacuna_costo', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True, verbose_name='costo de vacuna')),
                ('vacuna_moneda', models.CharField(blank=True, choices=[('S', 'S/'), ('D', '$')], default='D', max_length=1, null=True, verbose_name='moneda vacunas')),
                ('ratio_manpower_gratificacion_julio_diciembre', models.DecimalField(decimal_places=2, default=Decimal('9.00'), max_digits=5, verbose_name='ratio de mano de obra de gratificacion julio - diciembre')),
                ('ratio_vacaciones_truncas', models.DecimalField(decimal_places=2, default=Decimal('8.33'), max_digits=5, verbose_name='ratio de vacaciones truncas')),
                ('ratio_es_salud', models.DecimalField(decimal_places=2, default=Decimal('9.00'), max_digits=5, verbose_name='ratio de essalud')),
                ('ratio_sctr_salud', models.DecimalField(decimal_places=2, default=Decimal('1.00'), max_digits=5, verbose_name='ratio de sctr salud')),
                ('ratio_sctr_pension', models.DecimalField(decimal_places=2, default=Decimal('1.00'), max_digits=5, verbose_name='ratio de sctr pension')),
                ('costo_examen_medico_pre_ocupacional', models.DecimalField(decimal_places=2, default=Decimal('429.55'), max_digits=10, verbose_name='costo de examen medico pre-ocupacional')),
                ('costo_examen_medico_post_ocupacional', models.DecimalField(decimal_places=2, default=Decimal('193.00'), max_digits=10, verbose_name='costo de examen medico post-ocupacional')),
                ('meses_costo_certificacion', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='meses de costo de certificacion')),
                ('nombre_gasto_1', models.CharField(blank=True, max_length=50, null=True, verbose_name='nombre gasto 1')),
                ('veces_gasto_1', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='veces gasto 1')),
                ('costo_gasto_1', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='costo gasto 1')),
                ('moneda_gasto_1', models.CharField(blank=True, choices=[('S', 'S/'), ('D', '$')], default='D', max_length=1, null=True, verbose_name=' moneda gasto 1')),
                ('nombre_gasto_2', models.CharField(blank=True, max_length=50, null=True, verbose_name='nombre gasto 2')),
                ('veces_gasto_2', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='veces gasto 2')),
                ('costo_gasto_2', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='costo gasto 2')),
                ('moneda_gasto_2', models.CharField(blank=True, choices=[('S', 'S/'), ('D', '$')], default='D', max_length=1, null=True, verbose_name='moneda gasto 2')),
                ('catering_hoteleria_dias', models.PositiveSmallIntegerField(blank=True, default=30, null=True, verbose_name='numero de dias de catering hoteleria')),
                ('catering_hoteleria_costo', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='costo de catering - hoteleria')),
                ('catering_hoteleria_moneda', models.CharField(blank=True, choices=[('S', 'S/'), ('D', '$')], default='D', max_length=1, null=True, verbose_name='moneda catering')),
                ('medicina_dias', models.PositiveSmallIntegerField(blank=True, default=30, null=True, verbose_name='numero de dias de medicina')),
                ('medicina_costo', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='costo de medicina')),
                ('medicina_moneda', models.CharField(blank=True, choices=[('S', 'S/'), ('D', '$')], default='D', max_length=1, null=True, verbose_name='moneda medicina')),
                ('is_cliente_asume_combustible', models.BooleanField(default=True)),
                ('precio_gasoil', models.DecimalField(decimal_places=3, default=Decimal('1.1'), max_digits=5, verbose_name='precio del gasoil')),
                ('precio_gasolina', models.DecimalField(decimal_places=3, default=Decimal('1.1'), max_digits=5, verbose_name='precio del gasolina')),
                ('ratio_consumo_equipos', models.DecimalField(decimal_places=2, default=Decimal('0.11'), max_digits=3, verbose_name='consumo de equipos')),
            ],
            options={
                'verbose_name': 'presupuesto',
                'verbose_name_plural': 'presupuestos',
                'ordering': ('-created',),
                'permissions': (('can_add_budget', 'Puede adicionar presupuesto'), ('can_edit_budget', 'Puede modificar presupuesto'), ('can_change_status_budget', 'Puede cambiar estado presupuesto'), ('can_see_view_budget', 'Puede ver presupuesto')),
            },
        ),
        migrations.CreateModel(
            name='CertificacionBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('moneda', models.CharField(choices=[('S', 'S/'), ('D', '$')], default='D', max_length=1, verbose_name='moneda')),
                ('importe', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='importe')),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='EPPBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='EPPBudgetDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('unidad', models.CharField(max_length=12, verbose_name='unidad')),
                ('periodo_reposicion', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='periodo de reposicion')),
                ('quantity', models.DecimalField(decimal_places=6, default=1, max_digits=15, verbose_name='cantidad')),
                ('is_deleted', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='EquipmentBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('unit', models.CharField(blank=True, default='Hr', max_length=15, null=True, verbose_name='unidad de costo')),
                ('currency', models.CharField(choices=[('S', 'S/'), ('D', '$')], default='D', max_length=1, verbose_name='moneda')),
                ('price', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='precio')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='posición')),
                ('allows_ratio', models.PositiveIntegerField(default=1, verbose_name='Permite coeficiente?')),
                ('is_deleted', models.BooleanField(default=False)),
                ('potencia', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='potencia del equipo')),
                ('quantity', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='cantidad')),
                ('time_valorize', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='tiempo a valorizar')),
                ('hours_equipment_operation', models.DecimalField(decimal_places=6, default=8.0, max_digits=15, verbose_name='horas de operación del equipo')),
                ('has_combustible', models.BooleanField(default=False)),
                ('tipo_combustible', models.CharField(blank=True, choices=[('GO', 'GasOil'), ('GS', 'Gasolina')], max_length=2, null=True, verbose_name='tipo de combustible')),
            ],
            options={
                'verbose_name': 'equipo',
                'verbose_name_plural': 'equipos',
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='EquipmentTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('quantity', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='cantidad')),
                ('efficiency', models.DecimalField(decimal_places=6, default=1, max_digits=15, verbose_name='rendimiento')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='posición')),
            ],
            options={
                'verbose_name': 'equipo por tarea',
                'verbose_name_plural': 'equipos por tarea',
            },
        ),
        migrations.CreateModel(
            name='ManpowerBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('unit', models.CharField(blank=True, default='Hr', max_length=15, null=True, verbose_name='unidad de costo')),
                ('currency', models.CharField(choices=[('S', 'S/'), ('D', '$')], default='D', max_length=1, verbose_name='moneda')),
                ('price', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='precio')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='posición')),
                ('allows_ratio', models.PositiveIntegerField(default=1, verbose_name='Permite coeficiente?')),
                ('is_deleted', models.BooleanField(default=False)),
                ('quantity', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='cantidad')),
                ('time_valorize', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='tiempo a valorizar')),
                ('business_cost', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='costo empresarial')),
                ('epp_cost', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='costo de epp')),
                ('type_cost', models.CharField(choices=[('D', 'DIRECTO'), ('I', 'INDIRECTO')], default='D', max_length=1, verbose_name='tipo de costo')),
                ('codigo', models.CharField(blank=True, max_length=5, null=True, verbose_name='codigo')),
                ('puesto', models.CharField(blank=True, max_length=150, null=True, verbose_name='puesto')),
                ('sueldo_bruto', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='sueldo bruto')),
                ('asignacion_familiar', models.DecimalField(decimal_places=6, default=93, max_digits=15, verbose_name='asignacion familiar')),
                ('relevo_trabajo', models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='relevo trabajo')),
                ('relevo_descanso', models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='relevo descanso')),
                ('has_gasto_1', models.BooleanField(default=False)),
                ('has_gasto_2', models.BooleanField(default=False)),
                ('has_catering', models.BooleanField(default=False)),
                ('has_medicina', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'mano de obra',
                'verbose_name_plural': 'manos de obra',
                'ordering': ('manpower__code', 'manpower__name'),
            },
        ),
        migrations.CreateModel(
            name='ManpowerTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('quantity', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='cantidad')),
                ('efficiency', models.DecimalField(decimal_places=6, default=1, max_digits=15, verbose_name='rendimiento')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='posición')),
            ],
            options={
                'verbose_name': 'mano de obra por tarea',
                'verbose_name_plural': 'manos de obra por tarea',
            },
        ),
        migrations.CreateModel(
            name='MaterialBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('unit', models.CharField(blank=True, default='Hr', max_length=15, null=True, verbose_name='unidad de costo')),
                ('currency', models.CharField(choices=[('S', 'S/'), ('D', '$')], default='D', max_length=1, verbose_name='moneda')),
                ('price', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='precio')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='posición')),
                ('allows_ratio', models.PositiveIntegerField(default=1, verbose_name='Permite coeficiente?')),
                ('is_deleted', models.BooleanField(default=False)),
                ('type_material', models.CharField(choices=[('S', 'Estandar'), ('M', 'Medico'), ('W', 'Taller'), ('O', 'Operativo'), ('V', 'Varios'), ('I', 'Insumo médico'), ('E', 'EPP')], default='S', max_length=1, verbose_name='tipo de material')),
                ('quantity', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='cantidad')),
                ('time_valorize', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='tiempo a valorizar')),
                ('amortization', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='amortización')),
                ('is_subcontract', models.BooleanField(default=False)),
                ('distancia', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True, verbose_name='distancia')),
                ('costo_unitario_transporte', models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True, verbose_name='costo unitario de transporte')),
                ('ratio_perdida', models.DecimalField(blank=True, decimal_places=2, default=Decimal('1.00'), max_digits=5, null=True, verbose_name='ratio de perdida')),
            ],
            options={
                'verbose_name': 'material',
                'verbose_name_plural': 'materiales',
            },
        ),
        migrations.CreateModel(
            name='MaterialTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('quantity', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='cantidad')),
                ('efficiency', models.DecimalField(decimal_places=6, default=1, max_digits=15, verbose_name='rendimiento')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='posición')),
            ],
            options={
                'verbose_name': 'material por tarea',
                'verbose_name_plural': 'materiales por tarea',
            },
        ),
        migrations.CreateModel(
            name='MemberBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubcontractBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('unit', models.CharField(blank=True, default='Hr', max_length=15, null=True, verbose_name='unidad de costo')),
                ('currency', models.CharField(choices=[('S', 'S/'), ('D', '$')], default='D', max_length=1, verbose_name='moneda')),
                ('price', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='precio')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='posición')),
                ('allows_ratio', models.PositiveIntegerField(default=1, verbose_name='Permite coeficiente?')),
                ('is_deleted', models.BooleanField(default=False)),
                ('quantity', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='cantidad')),
                ('time_valorize', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='tiempo a valorizar')),
                ('amortization', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='amortización')),
                ('distancia', models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True, verbose_name='distancia')),
                ('costo_unitario_transporte', models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True, verbose_name='costo unitario de transporte')),
                ('ratio_perdida', models.DecimalField(blank=True, decimal_places=2, default=Decimal('1.00'), max_digits=5, null=True, verbose_name='ratio de perdida')),
            ],
            options={
                'verbose_name': 'subcontrato',
                'verbose_name_plural': 'subcontratos',
            },
        ),
        migrations.CreateModel(
            name='SubcontractTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('quantity', models.DecimalField(decimal_places=6, default=0, max_digits=15, verbose_name='cantidad')),
                ('efficiency', models.DecimalField(decimal_places=6, default=1, max_digits=15, verbose_name='rendimiento')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='posición')),
            ],
            options={
                'verbose_name': 'subcontrato por tarea',
                'verbose_name_plural': 'subcontratos por tarea',
            },
        ),
        migrations.CreateModel(
            name='TaskBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('wbs', models.CharField(max_length=50, verbose_name='EDT')),
                ('outline_level', models.PositiveSmallIntegerField(default=0)),
                ('name', models.CharField(max_length=150, verbose_name='nombre')),
                ('unit', models.CharField(blank=True, max_length=15, null=True, verbose_name='unidad')),
                ('efficiency', models.DecimalField(blank=True, decimal_places=6, default=1, max_digits=15, null=True, verbose_name='rendimiento')),
                ('efficiency_divider', models.DecimalField(blank=True, decimal_places=6, default=1, max_digits=15, null=True, verbose_name='rendimiento divisor')),
                ('quantity', models.DecimalField(blank=True, decimal_places=6, default=1, max_digits=15, null=True, verbose_name='cantidad')),
                ('projected_start_date', models.DateField(blank=True, null=True, verbose_name='inicio')),
                ('projected_finish_date', models.DateField(blank=True, null=True, verbose_name='término')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='posición')),
                ('uid', models.PositiveIntegerField(default=0)),
                ('percentage_minor_tools', models.DecimalField(decimal_places=6, default=0.03, max_digits=15, verbose_name='porcentaje de herramientas menores')),
                ('is_parent', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_enabled', models.BooleanField(default=True)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks_budget', to='budget.Budget', verbose_name='presupuesto')),
            ],
            options={
                'verbose_name': 'tarea por presupuesto',
                'verbose_name_plural': 'tareas por presupuesto',
                'ordering': ('budget', 'position'),
            },
        ),
    ]
