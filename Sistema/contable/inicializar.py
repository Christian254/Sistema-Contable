from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from datetime import time, date, timedelta
from .models import *
from decimal import *

def iniciarUsuario():
	user = User.objects.all()
	i= len(user)
	if i==0:
		user = User.objects.create_user(username='ANF115', password= 'root')
		user.save()

def iniciarPeriodo():
	periodo=PeriodoContable.objects.all()
	i = len(periodo)
	if i==0 :
		periodo1= PeriodoContable()
		periodo1.fecha_inicio=date.today()
		periodo1.fecha_final=date.today() + timedelta(days=30)
		periodo1.usr_aperturo='Periodo1'
		periodo1.save()
		return periodo1
	else:
		return PeriodoContable.objects.get(id=i)


def iniciarCuenta(codigo):
	cuentas = Cuenta.objects.filter(codigo_cuenta__contains=codigo)
	pe = PeriodoContable.objects.all()
	p=len(pe)
	for cuenta in cuentas :
		try:
			libro = LibroMayor.objects.get(cuenta=cuenta.nom_cuenta)
		except (KeyError, LibroMayor.DoesNotExist):
			libro1 = LibroMayor()
			concepto = 'inicio'
			periodo = PeriodoContable.objects.get(id=p)
			libro1.periodo=periodo
			libro1.cuenta=cuenta.nom_cuenta
			libro1.codCuenta=cuenta.codigo_cuenta
			libro1.saldoDeudor=0
			libro1.saldoAcreedor=0
			libro1.estado=True
			libro1.save()
			diario =Diario()
			diario.mayor= libro1
			diario.codCuenta = cuenta.codigo_cuenta
			diario.descripcion='inicializacion'
			diario.fecha=date.today()
			diario.concepto=concepto
			diario.haber=0
			diario.debe=0
			libro1.saldoAcreedor = 0
			libro1.save()
			diario.save()

def iniciarOrden():
	cuentas = Cuenta.objects.filter(codigo_cuenta__contains='ACO')
	pe = PeriodoContable.objects.all()
	p=len(pe)
	for cuenta in cuentas :
		try:
			libro = LibroMayor.objects.get(cuenta=cuenta.nom_cuenta)
		except (KeyError, LibroMayor.DoesNotExist):
			libro1 = LibroMayor()
			concepto = 'inicio'
			periodo = PeriodoContable.objects.get(id=p)
			libro1.periodo=periodo
			libro1.cuenta=cuenta.nom_cuenta
			libro1.codCuenta=cuenta.codigo_cuenta
			libro1.saldoDeudor=0
			libro1.saldoAcreedor=0
			libro1.estado=True
			libro1.save()
			diario =Diario()
			diario.mayor= libro1
			diario.codCuenta = cuenta.codigo_cuenta
			diario.descripcion='inicializacion'
			diario.fecha=date.today()
			diario.concepto=concepto
			diario.haber=0
			diario.debe=0
			libro1.saldoAcreedor = 0
			libro1.save()
			diario.save()
		try:
			orden = OrdenFab.objects.get(codCuenta=cuenta.codigo_cuenta)
		except :
			orden = OrdenFab(codCuenta=cuenta.codigo_cuenta)
			orden.save()


def enviarKardex(monto,enviar_a,p):
	cuenta = Cuenta.objects.get(codigo_cuenta='AC002')
	cuenta1 = Cuenta.objects.get(codigo_cuenta='AC003')
	try:
		libro = LibroMayor.objects.get(cuenta=cuenta.nom_cuenta)
		libro1 = LibroMayor.objects.get(cuenta=cuenta1.nom_cuenta)
		concepto = 'Cargado'
		diario =Diario()
		diario.mayor= libro
		diario.codCuenta = cuenta.codigo_cuenta
		diario.descripcion='Paso de materia prima'
		diario.fecha=date.today()
		diario.concepto=concepto
		diario.haber=float(monto)
		diario.debe=0
		diario.save()
		libro.saldoAcreedor =libro.saldoAcreedor+float(monto)
		libro.save()		
		diario1 =Diario()
	except (KeyError, LibroMayor.DoesNotExist):
		libro1 = LibroMayor()
		concepto = 'Cargado'
		periodo = PeriodoContable.objects.get(id=p)
		libro1.periodo=periodo
		libro1.cuenta=cuenta.nom_cuenta
		libro1.codCuenta=cuenta.codigo_cuenta
		libro1.saldoDeudor=0
		libro1.saldoAcreedor=0
		libro1.estado=True
		libro1.save()
		diario =Diario()
		diario.mayor= libro1
		diario.codCuenta = cuenta.codigo_cuenta
		diario.descripcion='Compra de materia prima'
		diario.fecha=date.today()
		diario.concepto=concepto
		diario.haber=monto
		diario.debe=0
		libro1.saldoAcreedor = libro1.saldoAcreedor +float(monto)
		libro1.save()
		diario.save()
	try:
		libro1 = LibroMayor.objects.get(cuenta=cuenta1.nom_cuenta)
		concepto = 'abonado'
		diario1 =Diario()
		diario1.mayor= libro1
		diario1.codCuenta = cuenta1.codigo_cuenta
		diario1.descripcion='compra de materia prima'
		diario1.fecha=date.today()
		diario1.concepto=concepto
		diario1.debe=float(monto)
		diario1.haber=0
		diario1.save()
		libro1.saldoDeudor =libro1.saldoDeudor+float(monto)
		libro1.save()
	except (KeyError, LibroMayor.DoesNotExist):
		periodo = PeriodoContable.objects.get(id=p)
		libro1 = LibroMayor()
		concepto = 'Abonado'
		libro1.periodo=periodo
		libro1.cuenta=cuenta1.nom_cuenta
		libro1.codCuenta=cuenta1.codigo_cuenta
		libro1.saldoDeudor=0
		libro1.saldoAcreedor=0
		libro1.estado=True
		libro1.save()
		diario =Diario()
		diario.mayor= libro1
		diario.codCuenta = cuenta1.codigo_cuenta
		diario.descripcion='Compra de materia prima'
		diario.fecha=date.today()
		diario.concepto=concepto
		diario.debe=monto
		diario.haber=0
		libro1.saldoDeudor = libro1.saldoDeudor +float(monto)
		libro1.save()
		diario.save()
	
def ingresarKardex(kardex_id, fecha,cantEntrada,precEntrada):
	try:
		kardex1 = detalleKardex.objects.get(id=int(kardex_id))
		kard = kardex1.kardex_set.all()
		kard = kardex1.kardex_set.all()
		i =0
		for k in kard :
			i=k.id
		newKard = Kardex()
		newKard.fecha = fecha
		newKard.cantEntrada = cantEntrada
		newKard.cantSalida=0
		newKard.cantExistencia=cantEntrada
		newKard.precEntrada=precEntrada
		newKard.precSalida=0
		newKard.precExistencia=precEntrada
		newKard.montoEntrada = Decimal(precEntrada) * Decimal(cantEntrada)
		newKard.montoSalida=0
		newKard.montoExistencia=Decimal(precEntrada) * Decimal(cantEntrada)
		newKard.detall = kardex1
		newKard.save()
		ultimo_id = i
		if ultimo_id > 0:
			ult_kardex=Kardex.objects.get(pk=ultimo_id)
			newKard.montoExistencia = newKard.montoExistencia +  ult_kardex.montoExistencia
			newKard.cantExistencia= int(newKard.cantExistencia) + int(ult_kardex.cantExistencia)
			prec = newKard.montoExistencia / newKard.cantExistencia
			newKard.precExistencia=prec
			newKard.save()
		return newKard
	except:
		return False

def cuentaKardex(pk_cuenta,p,monto,prod):
	cuenta = Cuenta.objects.get(codigo_cuenta=pk_cuenta)
	cuenta1 = Cuenta.objects.get(codigo_cuenta=prod)
	try:
		libro = LibroMayor.objects.get(cuenta=cuenta.nom_cuenta)
		concepto = 'Cargado'
		diario =Diario()
		diario.mayor= libro
		diario.codCuenta = cuenta.codigo_cuenta
		diario.descripcion='compra de materia prima'
		diario.fecha=date.today()
		diario.concepto=concepto
		diario.haber=float(monto)
		diario.debe=0
		diario.save()
		libro.saldoAcreedor =libro.saldoAcreedor+float(monto)
		libro.save()		
		diario1 =Diario()
	except (KeyError, LibroMayor.DoesNotExist):
		libro1 = LibroMayor()
		concepto = 'Cargado'
		periodo = PeriodoContable.objects.get(id=p)
		libro1.periodo=periodo
		libro1.cuenta=cuenta.nom_cuenta
		libro1.codCuenta=cuenta.codigo_cuenta
		libro1.saldoDeudor=0
		libro1.saldoAcreedor=0
		libro1.estado=True
		libro1.save()
		diario =Diario()
		diario.mayor= libro1
		diario.codCuenta = cuenta.codigo_cuenta
		diario.descripcion='Compra de materia prima'
		diario.fecha=date.today()
		diario.concepto=concepto
		diario.haber=monto
		diario.debe=0
		libro1.saldoAcreedor = libro1.saldoAcreedor +float(monto)
		libro1.save()
		diario.save()
	try:
		libro1 = LibroMayor.objects.get(cuenta=cuenta1.nom_cuenta)
		concepto = 'abonado'
		diario1 =Diario()
		diario1.mayor= libro1
		diario1.codCuenta = cuenta1.codigo_cuenta
		diario1.descripcion='compra de materia prima'
		diario1.fecha=date.today()
		diario1.concepto=concepto
		diario1.debe=float(monto)
		diario1.haber=0
		diario1.save()
		libro1.saldoDeudor =libro1.saldoDeudor+float(monto)
		libro1.save()
	except (KeyError, LibroMayor.DoesNotExist):
		periodo = PeriodoContable.objects.get(id=p)
		libro1 = LibroMayor()
		concepto = 'Abonado'
		libro1.periodo=periodo
		libro1.cuenta=cuenta1.nom_cuenta
		libro1.codCuenta=cuenta1.codigo_cuenta
		libro1.saldoDeudor=0
		libro1.saldoAcreedor=0
		libro1.estado=True
		libro1.save()
		diario =Diario()
		diario.mayor= libro1
		diario.codCuenta = cuenta1.codigo_cuenta
		diario.descripcion='Compra de materia prima'
		diario.fecha=date.today()
		diario.concepto=concepto
		diario.debe=monto
		diario.haber=0
		libro1.saldoDeudor = libro1.saldoDeudor +float(monto)
		libro1.save()
		diario.save()
	
def inicializarCuenta():
	try:
		periodo = iniciarPeriodo()
		#inicializacion de Activos Circulante
		tipo = TipoCuenta(nom_tipo='Activo',codigo_tcuenta='A',disminuye_en='001',aumenta_en='001')
		tipo.save()
		grup =GrupoCuenta(tipo_cuenta=tipo,nom_grupo='Activo Circulante',codigo_gcuenta='AC',descripcion='Activos de facil recuperacion')
		grup.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Efectivo',descripcion='Activo de facil recuperacion',codigo_cuenta='AC000')
		cuenta.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Cuentas por cobrar',descripcion='Cuentas de rapido cobro',codigo_cuenta='AC001')
		cuenta.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Inventario de PT',descripcion='Inventario de producto terminado',codigo_cuenta='AC002')
		cuenta.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Inventario de PP',descripcion='Inventario de producto en proceso',codigo_cuenta='AC003')
		cuenta.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Orden de fabricacion 0',descripcion='Ordenes de fabricacion',codigo_cuenta='ACO00')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()
		orden=OrdenFab(codCuenta=cuenta.nom_cuenta)
		cuenta = Cuenta(grupo = grup, nom_cuenta='Inventario',descripcion='Inventario de materia prima',codigo_cuenta='AC004')
		cuenta.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Mano de obra directa',descripcion='Mano de obra directa',codigo_cuenta='AC005')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()

		cuenta = Cuenta(grupo = grup, nom_cuenta='CIF',descripcion='Costos indirectos de fabricacion',codigo_cuenta='AC006')
		cuenta.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Iva Acreditable',descripcion='Iva pagado',codigo_cuenta='AC007')
		cuenta.save()

		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()

		#activos fijos
		tipo = TipoCuenta(nom_tipo='Activo',codigo_tcuenta='A',disminuye_en='001',aumenta_en='001')
		tipo.save()
		grup =GrupoCuenta(tipo_cuenta=tipo,nom_grupo='Activo Fijo',codigo_gcuenta='AF',descripcion='Activos de recuperacion a largo plazo')
		grup.save()		
		cuenta = Cuenta(grupo = grup, nom_cuenta='Documentos por cobrar',descripcion='Cuentas a largo plazo',codigo_cuenta='AF000')
		cuenta.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Edificio',descripcion='Edificio de manofactura',codigo_cuenta='AF001')
		cuenta.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Maquinaria',descripcion='Maquinaria de manofactura',codigo_cuenta='AF002')
		cuenta.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Automovil',descripcion='Transporte de la empresa',codigo_cuenta='AF003')
		cuenta.save()

		#Activos diferidos
		tipo = TipoCuenta(nom_tipo='Activo',codigo_tcuenta='A',disminuye_en='001',aumenta_en='001')
		tipo.save()
		grup =GrupoCuenta(tipo_cuenta=tipo,nom_grupo='Activo Diferido',codigo_gcuenta='AD',descripcion='Activos diferidos')
		grup.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Gastos pagados por adelantado',descripcion='Gastos pagados por adelantado o anticipado',codigo_cuenta='AD000')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()

		#ContraCuenta Activos
		tipo = TipoCuenta(nom_tipo='Activo',codigo_tcuenta='A',disminuye_en='001',aumenta_en='001')
		tipo.save()
		grup =GrupoCuenta(tipo_cuenta=tipo,nom_grupo='Contracuenta Activo',codigo_gcuenta='AK',descripcion='Contracuenta activos')
		grup.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Depreciacion Acumulada',descripcion='Refleja el descuento del costo original del equipo',codigo_cuenta='AK000')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Amortizacion Acumulada',descripcion='Declinamiento de los activos no tangibles',codigo_cuenta='AK001')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Agotamiento Acumulado',descripcion='Declinacion del valor de los recursos naturales',codigo_cuenta='AK002')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()

		#pasivos circulantes
		tipo = TipoCuenta(nom_tipo='Pasivo',codigo_tcuenta='P',disminuye_en='001',aumenta_en='001')
		tipo.save()
		grup =GrupoCuenta(tipo_cuenta=tipo,nom_grupo='Pasivo Circulante',codigo_gcuenta='PC',descripcion='Pasivos de repido desembolso')
		grup.save()		
		cuenta = Cuenta(grupo = grup, nom_cuenta='Cuentas por Pagar',descripcion='Cuentas proximas a pagar',codigo_cuenta='PC000')
		cuenta.save()		
		cuenta = Cuenta(grupo = grup, nom_cuenta='Proveedores',descripcion='Cuentas proximas a pagar',codigo_cuenta='PC001')
		cuenta.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Iva Retenido',descripcion='Iva por pagar',codigo_cuenta='PC002')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()

		#Pasivos fijos
		tipo = TipoCuenta(nom_tipo='Pasivo',codigo_tcuenta='P',disminuye_en='001',aumenta_en='001')
		tipo.save()
		grup =GrupoCuenta(tipo_cuenta=tipo,nom_grupo='Pasivo Fijo',codigo_gcuenta='PF',descripcion='Pasivos a largo plazo')
		grup.save()		
		cuenta = Cuenta(grupo = grup, nom_cuenta='Documentos por pagar',descripcion='Documentos por pagar a largo plazo',codigo_cuenta='PF000')
		cuenta.save()

		#pasivos diferidos
		tipo = TipoCuenta(nom_tipo='Pasivo',codigo_tcuenta='P',disminuye_en='001',aumenta_en='001')
		tipo.save()
		grup =GrupoCuenta(tipo_cuenta=tipo,nom_grupo='Pasivo Diferido',codigo_gcuenta='PD',descripcion='Pasivos diferidos')
		grup.save()

		#inicializacion de capital
		tipo = TipoCuenta(nom_tipo='Capital',codigo_tcuenta='C',disminuye_en='001',aumenta_en='001')
		tipo.save()
		grup =GrupoCuenta(tipo_cuenta=tipo,nom_grupo='Capital',codigo_gcuenta='CA',descripcion='Capital aportado por el dueno')
		grup.save()		
		cuenta = Cuenta(grupo = grup, nom_cuenta='Capital Social',descripcion='Capital social',codigo_cuenta='CS000')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Inveriones',descripcion='Capital Invertido durante el periodo',codigo_cuenta='CI001')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Desembolsos',descripcion='Capital social',codigo_cuenta='CD002')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()

		#inicializamos cuentas Resultado
		tipo = TipoCuenta(nom_tipo='Resultado',codigo_tcuenta='R',disminuye_en='001',aumenta_en='001')
		tipo.save()
		grup =GrupoCuenta(tipo_cuenta=tipo,nom_grupo='Resultado',codigo_gcuenta='R',descripcion='Cuentas resultado de operaciones de la empresa')
		grup.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Ingreso por ventas',descripcion='ingresos normales de la empresa',codigo_cuenta='RI000')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Costo de lo vendido',descripcion='costos de fabricacion de un producto',codigo_cuenta='RCV00')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Utilidad Neta',descripcion='Perdida o ganancia de la empresa',codigo_cuenta='UT000')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Gastos de operacion',descripcion='Gastos operativos de la empresa',codigo_cuenta='RGO00')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Gastos de Administracion',descripcion='Gastos administrativos de la empresa',codigo_cuenta='RGA00')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Otros Gastos',descripcion='Otros Gastos de la empresa',codigo_cuenta='ROG00')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Gastos por salarios',descripcion='Gastos por salario',codigo_cuenta='RGS')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()

		cuenta = Cuenta(grupo = grup, nom_cuenta='Gastos por depreciacion',descripcion='Gastos por depreciacion de activos fijos',codigo_cuenta='RD000')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Gastos por amortizacion',descripcion='Gastos por amortizacion de bienes intangibles',codigo_cuenta='RD001')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Gastos por agotamiento',descripcion='Gastos por agotamiento de recursos',codigo_cuenta='RD002')
		cuenta.save()
		libro = LibroMayor(cuenta=cuenta.nom_cuenta,codCuenta=cuenta.codigo_cuenta,saldoDeudor=0,saldoAcreedor=0,periodo=periodo)
		libro.save()



		padre = Cuenta.objects.get(codigo_cuenta = 'PC000')
		grup = GrupoCuenta.objects.get(nom_grupo='Pasivo Circulante')

		cuenta = Cuenta(grupo = grup, nom_cuenta='Energia electrica',descripcion='Servicio de energia electrica', codigo_cuenta='PC987')
		cuenta.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Suministros de fabricacion',descripcion='Suministros utilizados en el proceso de fabricacion', codigo_cuenta='PC989')
		cuenta.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Gasolina', descripcion='Recurso utilizado para el transporte de material', codigo_cuenta='PC990')
		cuenta.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Mantenimineto de Maquinaria', descripcion='Gasto e mantenimineto de la maquinaria', codigo_cuenta='PC991')
		cuenta.save()
		cuenta = Cuenta(grupo = grup, nom_cuenta='Alquiler', descripcion='Alquiler de local', codigo_cuenta='PC992')
		cuenta.save()
		#Inicializar cuentas de CIF
		
		return True
	except :
		return False


def eliminarCuentas():
	pass

def iniciarKardex():
	try:
		kardex = detalleKardex(tipo='PP', nombre='Materia prima: Bambu ASPER',fecha=date.today())
		kardex.save()		
		kardex = detalleKardex(tipo='PP', nombre='Materia prima: Bambu TULDOIDES',fecha=date.today())
		kardex.save()		

		kardex = detalleKardex(tipo='PT', nombre='Producto: Cortinas',fecha=date.today())
		kardex.save()
		kardex = detalleKardex(tipo='PT', nombre='Producto: Lamparas',fecha=date.today())
		kardex.save()

		return True
	except :
		return False

def iniciarPuestos():
	try:
		puesto = Puesto(area='Produccion', cargo='Encargado de Produccion y Logistica', salNominal=600, total=0)
		puesto.save()
		puesto = Puesto(area='Produccion', cargo='Operario', salNominal=300, total=0)
		puesto.save()
		puesto = Puesto(area='Mercadeo', cargo='Encargado de Mercadeo y Ventas', salNominal=400, total=0)
		puesto.save()
		puesto = Puesto(area='Mercadeo', cargo='Motorista', salNominal=300, total=0)
		puesto.save()
		puesto = Puesto(area='Mercadeo', cargo='Ayudante', salNominal=300, total=0)
		puesto.save()
		puesto = Puesto(area='Administracion', cargo='Gerente General', salNominal=700, total=0)
		puesto.save()
		puesto = Puesto(area='Administracion', cargo='Contador', salNominal=350, total=0)
		puesto.save()
		puesto = Puesto(area='Administracion', cargo='Secretaria', salNominal=350, total=0)
		puesto.save()
		return True
	except :
		return False

def iniciarPlanilla():
	try:
		e = EmpPlanilla(cargo_id=6, nomEmpleado='Admin', anios=7, salPersonal=0, isss=0, afp=0, insaforp=0, vaca=0, aguinaldo=0, cmo=0)
		e.save()
		return True
	except :
		return False