from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class TipoCuenta(models.Model):
	nom_tipo = models.CharField(max_length=50)
	codigo_tcuenta = models.CharField(max_length=1)
	disminuye_en = models.CharField(max_length=10)
	aumenta_en = models.CharField(max_length=10)

class GrupoCuenta(models.Model):
	tipo_cuenta = models.OneToOneField(TipoCuenta)
	nom_grupo = models.CharField(max_length=50, blank=False, unique=True)
	codigo_gcuenta = models.CharField(max_length=2, blank=False, unique=True)
	descripcion = models.CharField(max_length=200, blank=False)

class Cuenta(models.Model):
	grupo = models.ForeignKey(GrupoCuenta, blank=False, on_delete=models.CASCADE)
	nom_cuenta = models.CharField(max_length=100, blank=False, unique=True)
	descripcion = models.CharField(max_length=200, blank=False)
	codigo_cuenta = models.CharField(max_length=7, blank=False, unique=True)
	cuenta_padre = models.CharField(max_length=50)

	class Meta:
		verbose_name='Cuenta'
		verbose_name_plural='Cuentas'
	def __str__(self):
		return '%s' %(self.nom_cuenta)

class PeriodoContable(models.Model):
	fecha_inicio = models.DateField()
	fecha_final = models.DateField()
	usr_aperturo = models.CharField(max_length=20, blank=False)
	usr_cerro = models.CharField(max_length=20, blank=True)
	activo = models.BooleanField(default=True)

class LibroMayor(models.Model):
	cuenta = models.CharField(max_length=100)
	codCuenta=models.CharField(max_length=10)
	saldoDeudor = models.FloatField()
	saldoAcreedor = models.FloatField()
	estado = models.BooleanField(default=True)
	periodo = models.ForeignKey(PeriodoContable, on_delete=models.CASCADE)
	saldo =models.FloatField(default=0.00)
	class Meta:
		verbose_name='LibroMayor'
		verbose_name_plural='LibroMayor'
	def __str__(self):
		return '%s' %(self.cuenta)

class OrdenFab(models.Model):
	codCuenta=models.CharField(max_length=100,unique=True)
	saldo=models.FloatField(default=0.00)
	materiaPrima= models.FloatField(default=0)
	manoObra=models.FloatField(default=0)
	cif= models.FloatField(default=0)
	invInici=models.FloatField(default=0)

class Diario(models.Model):
	mayor = models.ForeignKey(LibroMayor, blank=False, null=False)
	codCuenta = models.CharField(max_length=10)
	concepto = models.CharField(max_length=20, blank=False)
	fecha = models.DateField(blank=False)
	descripcion = models.CharField(max_length=200)
	debe = models.FloatField()
	haber=models.FloatField()

	class Meta:
		verbose_name='Docuemnto'
		verbose_name_plural='Documento'
	def __str__(self):
		return '%s' %(self.id)

class detalleKardex(models.Model):
	tipo = models.CharField(max_length=4)
	nombre = models.CharField(max_length=200)
	fecha = models.DateField()

class Kardex(models.Model):
	fecha = models.DateField()
	cantEntrada = models.IntegerField()
	cantSalida = models.IntegerField()
	cantExistencia = models.IntegerField()
	precEntrada = models.DecimalField(max_digits=7,decimal_places=2)
	precSalida = models.DecimalField(max_digits=7,decimal_places=2)
	precExistencia = models.DecimalField(max_digits=10,decimal_places=2)
	montoEntrada =models.DecimalField(max_digits=20,decimal_places=2)
	montoSalida =models.DecimalField(max_digits=20,decimal_places=2)
	montoExistencia= models.DecimalField(max_digits=20,decimal_places=2)
	detall = models.ForeignKey(detalleKardex,on_delete=models.CASCADE)

class EstadoResultado(models.Model):
	nombre_empresa=models.CharField(max_length=200)
	periodo = models.OneToOneField(PeriodoContable, on_delete=models.CASCADE)

class datosResultado(models.Model):
	cuenta = models.CharField(max_length=100)
	codCuenta=models.CharField(max_length=10)
	saldo =models.FloatField(default=0.00)
	estado=models.ForeignKey(EstadoResultado, on_delete=models.CASCADE)

#MOD
class Puesto(models.Model):
	area = models.CharField(max_length=50)
	cargo = models.CharField(max_length=70)
	salNominal = models.FloatField()
	total = models.FloatField(blank=True, null=True)

	class Meta:
		verbose_name='Puestos'
		verbose_name_plural='Puestos'
	def __str__(self):
		return '%s' %(self.cargo)

class EmpPlanilla(models.Model):
	cargo = models.ForeignKey(Puesto)
	salPersonal = models.FloatField(blank=True, null=True)
	nomEmpleado = models.CharField(max_length=70)
	anios = models.FloatField()
#	dias = models.IntegerField()
#	horas = models.IntegerField()
	isss = models.FloatField(blank=True, null=True)
	afp = models.FloatField(blank=True, null=True)
	insaforp = models.FloatField(blank=True, null=True)
	vaca = models.FloatField(blank=True, null=True)
	aguinaldo = models.FloatField(blank=True, null=True)
	cmo = models.FloatField(blank=True, null=True)

class sancionSalarial(models.Model):
	planilla = models.ForeignKey(EmpPlanilla, on_delete=models.CASCADE)
	tiempo = models.CharField(max_length=10)
	unidades = models.IntegerField()
	monto = models.FloatField(blank=True, null=True)
	descripcion = models.CharField(max_length=200)

	class Meta:
		verbose_name='Sanciones'
		verbose_name_plural='Sanciones'
	def __str__(self):
		return '%s' %(self.planilla)

