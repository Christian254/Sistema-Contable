from django.contrib.auth import authenticate, login, update_session_auth_hash 
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import loader
from django.http.response import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import time, date, timedelta
from .models import *
from decimal import *
from contable.inicializar import *
#metodo para logearse
def auth_login(request):
	if request.method == 'POST':
		username = request.POST.get('username',None)
		password = request.POST.get('password', None)
		user = authenticate(username=username, password=password)
	 	if user:
			login(request,user)
			return redirect('/')
		else :
			valor = "*Ingrese usuario valido o contrasena correcta"
			context= { 'valor':valor }
			return render(request,'Main/login.html',context)

	context= {}
	return render(request,'Main/login.html',context)

#metodo para registrarse
def auth_signup(request):
	if request.method == 'POST':
		username = request.POST.get('username',None)
		password = request.POST.get('password', None)
		email=request.POST.get('email',None)
		user = authenticate(username=username, password=password)
		if user:
		 	valor = "Ese usuario ya esta registrado, seleccione otro"
			context= { 'valor':valor }
			return render(request,'Main/registrar.html',context)
		else :			
			user = User.objects.create_user(username=username,email=email, password= password)
		 	user.save()
		 	login(request,user)
		 	return redirect('/')
	context= {}
	return render(request,'Main/registrar.html',context)


def index(request):
	template = loader.get_template('Main/index.html')
	cuentas = GrupoCuenta.objects.all()
	puestos = Puesto.objects.all()
	kardex= detalleKardex.objects.all()
	e = EmpPlanilla.objects.all()
	ingr = False
	if len(cuentas) == 0:
		iniz =inicializarCuenta()
	if len(kardex) <1:
		iniciarKardex()
	if len(puestos) == 0:
		iniz = iniciarPuestos()
	if len(e) == 0:
		iniz = iniciarPlanilla()
	iniciarUsuario()
	return HttpResponse(template.render({} , request))



def OF(request):
	template=loader.get_template('Main/OrdenesFabricacion.html')
	iniciarOrden()
	libro = LibroMayor.objects.filter(codCuenta__contains='ACO')
	if request.method=='POST':
		action = request.POST.get('action',None)
		if action=='editar':
			opcion= request.POST.get('opcion',None)
			monto1= request.POST.get('MOD',None)
			monto2= request.POST.get('CIF',None)
			try:
				orden=OrdenFab.objects.get(codCuenta=opcion)
			except Exception as e:
				orden=OrdenFab(codCuenta=opcion)

			orden.manoObra=float(monto1)
			cif = float(monto1)*(float(monto2)/100)
			orden.cif=cif
			orden.saldo=orden.saldo+cif+float(monto1)
			orden.save()
			i = len(PeriodoContable.objects.all())
			cuentaKardex('AC005',i,monto1,opcion)
			cuentaKardex('AC006',i,cif,opcion)
	orden= LibroMayor.objects.filter(codCuenta__contains='ACO')
	for o in orden:
		o.saldo= float(o.saldoDeudor) - float(o.saldoAcreedor)
		o.save()
	context={
		'libro':libro,
		'orden':orden,
	}
	return HttpResponse(template.render(context , request))


def terminar(request, of_id):
	template=loader.get_template('Main/OrdenesFabricacion.html')
	terminada = LibroMayor.objects.get(pk=of_id)
	terminada.estado=False
	terminada.save()
	orden= LibroMayor.objects.filter(codCuenta__contains='ACO')
	context={
		'orden':orden,
	}
	return HttpResponse(template.render(context , request))

def ver(request, of_id):
	template=loader.get_template('Main/ver.html')
	ordenfab = LibroMayor.objects.get(pk=of_id)
	detalle=OrdenFab.objects.get(codCuenta=ordenfab.codCuenta)
	context={
		'orden':ordenfab,
		'detalle':detalle,
	}
	return HttpResponse(template.render(context , request))


def ingresarCuenta(request):
	template=loader.get_template('Main/ingresar_cuenta.html')

	tipoCuenta = GrupoCuenta.objects.all()
	
	context = {
		'tipo':tipoCuenta,
	}
	if request.method=='POST':
		try:
			action = request.POST.get('action',None)
			if action =='newCuenta':
				codigot = request.POST.get('tipo',None)
				nombret = request.POST.get('nombret',None)
				codigog= request.POST.get('grupo',None)
				nombreg = request.POST.get('nombreg',None)
				desg = request.POST.get('descripciong',None)
				tipoC = TipoCuenta()
				tipoC.nom_tipo=nombret
				tipoC.codigo_tcuenta=codigot
				tipoC.disminuye_en='001'
				tipoC.aumenta_en='001'
				tipoC.save()
				grup =GrupoCuenta()
				grup.tipo_cuenta=tipoC
				grup.nom_grupo=nombreg
				grup.codigo_gcuenta=codigot + codigog
				grup.descripcion=desg
				grup.save()
		except Exception as e:
			print(e.message)
			context = {
				'tipo':tipoCuenta,
				'anadido':False,
			}
			return HttpResponse(template.render(context , request))

	return HttpResponse(template.render(context , request))

def insertCuenta(request, grupo_id):
	template=loader.get_template('Main/nuevaCuenta.html')
	grupo1= get_object_or_404(GrupoCuenta,pk=grupo_id)
	cuenta = grupo1.cuenta_set.all()
	ingr = False
	context ={
	'ingr':ingr,
	'grupo':grupo1,
	'cuenta':cuenta,
	}
	if request.method=='POST':
		action = request.POST.get('action',None)
		if action =='insert':
			try:
				cuent = Cuenta()
				cod = request.POST.get('codigo',None)
				cuent.nom_cuenta = request.POST.get('nombrec',None)
				cuent.descripcion=request.POST.get('descripcion',None)
				cuent.cuenta_padre= request.POST.get('cuentaP',None)
				cuent.codigo_cuenta=grupo1.codigo_gcuenta+cod
				cuent.grupo = grupo1
				cuent.save()
				grupo1= get_object_or_404(GrupoCuenta,pk=grupo_id)
				cuenta = grupo1.cuenta_set.all()
				context ={
					'ingr':ingr,
					'grupo':grupo1,
					'cuenta':cuenta,
				}			
				template=loader.get_template('Main/nuevaCuenta.html')
				return HttpResponse(template.render(context,request ))
			except Exception as e:
				raise
			
	return HttpResponse(template.render(context,request ))


#metodo para renderizar lo de costo promedio XD

def kardex(request):
	template=loader.get_template('Main/detalle.html')
	kardex= detalleKardex.objects.all()
	
	context ={
		'kardex':kardex,
	}
	if request.method=='POST':
		action = request.POST.get('action',None)
		if action =='new':
			nombre = request.POST.get('nombre',None)
			tipo = request.POST.get('tipo',None)
			fecha = date.today()
			detalle = detalleKardex()
			detalle.nombre= nombre
			detalle.tipo = tipo
			detalle.fecha=fecha
			detalle.save()
	return HttpResponse(template.render(context , request))

def CP(request, kardex_id):
	template=loader.get_template('Main/kardex.html')
	kardex1= get_object_or_404(detalleKardex,pk=kardex_id)
	kard = kardex1.kardex_set.all()
	prodPP= LibroMayor.objects.filter(codCuenta__contains='ACO', estado=True)
	prodPT= LibroMayor.objects.filter(codCuenta__contains='ACO', estado=False)
	i =0
	for k in kard :
		i=k.id
	final = None
	if i > 0:
		final = kard.get(pk=i)
	context = {
		'prodPP':prodPP,
		'prodPT':prodPT,
		'kardex1':kardex1,
		'kardex':kard,
		'i':i,
		'final':final,
	}
	if request.method=='POST':
		action = request.POST.get('action',None)
		if action =='insert':
			kardex1= get_object_or_404(detalleKardex,pk=kardex_id)
			fecha = request.POST.get('fechaE',None)
			cantEntrada=request.POST.get('cantidadE',None)
			precEntrada= request.POST.get('precioE',None)
			pk_cuenta= request.POST.get('cuenta',None)
			newKard = ingresarKardex(int(kardex1.id),fecha,cantEntrada,precEntrada)
			pe = PeriodoContable.objects.all()
			p = len(pe)
			if p > 0 :
				prod= ''
				if kardex1.tipo=='PP':
					prod='AC003'
				else :
					prod='AC002'
				cuentaKardex(pk_cuenta,p,newKard.montoEntrada,prod)
		elif action=='ordenfab':
			kardex1= get_object_or_404(detalleKardex,pk=kardex_id)
			fecha = request.POST.get('fechaO',None)
			cantEntrada=request.POST.get('cantidadO',None)
			pk_cuenta= request.POST.get('PT',None)
			pe = PeriodoContable.objects.all()
			p = len(pe)
			orden1 = get_object_or_404(LibroMayor,codCuenta=pk_cuenta,periodo=p)
			precEntrada=orden1.saldo/ int(cantEntrada)

			newKard = ingresarKardex(int(kardex1.id),fecha,cantEntrada,precEntrada)
			if p > 0 :
				prod= ''
				if kardex1.tipo=='PP':
					prod='AC003'
				else :
					prod='AC002'
				cuentaKardex(pk_cuenta,p,newKard.montoEntrada,prod)

		elif action =='delete':
			i =0
			for k in kard :
				i=k.id
			ultimo_id=i
			if ultimo_id > 0:
				newKard = Kardex()
				newKard.fecha = request.POST.get('fechaS',None)
				cantSalida=request.POST.get('cantidadS',None)
				enviar = request.POST.get('PP',None)

				newKard.cantEntrada = 0
				newKard.cantSalida= cantSalida
				newKard.cantExistencia=0
				newKard.precEntrada=0
				newKard.precSalida=0
				newKard.precExistencia=0
				newKard.montoEntrada = 0
				newKard.montoSalida=0
				newKard.montoExistencia=0
				newKard.detall = kardex1
				newKard.save()

				ult_kardex=Kardex.objects.get(pk=ultimo_id)
				prec= ult_kardex.precExistencia
				newKard.precSalida=prec
				newKard.cantExistencia= int(ult_kardex.cantExistencia) - int(newKard.cantSalida)
				montSalida= Decimal(prec) * Decimal(newKard.cantSalida)
				newKard.montoSalida=montSalida
				newKard.montoExistencia = ult_kardex.montoExistencia - montSalida
				newKard.precExistencia=prec
				newKard.save()

				pe = PeriodoContable.objects.all()
				p = len(pe)
				pk_cuenta='AC003'
				if p > 0 :
					cuentaKardex(pk_cuenta,p,montSalida,enviar)
					
		elif action =='vender':
			i =0
			for k in kard :
				i=k.id
			ultimo_id=i
			if ultimo_id > 0:
				newKard = Kardex()
				newKard.fecha = request.POST.get('fechaV',None)
				cantSalida=request.POST.get('cantidadV',None)
				ganancia = request.POST.get('ganancia',None)
				enviar = request.POST.get('PT',None)

				newKard.cantEntrada = 0
				newKard.cantSalida= cantSalida
				newKard.cantExistencia=0
				newKard.precEntrada=0
				newKard.precSalida=0
				newKard.precExistencia=0
				newKard.montoEntrada = 0
				newKard.montoSalida=0
				newKard.montoExistencia=0
				newKard.detall = kardex1
				newKard.save()

				ult_kardex=Kardex.objects.get(pk=ultimo_id)
				prec= ult_kardex.precExistencia
				newKard.precSalida=prec
				newKard.cantExistencia= int(ult_kardex.cantExistencia) - int(newKard.cantSalida)
				montSalida= Decimal(prec) * Decimal(newKard.cantSalida)
				newKard.montoSalida=montSalida
				newKard.montoExistencia = ult_kardex.montoExistencia - montSalida
				newKard.precExistencia=prec
				newKard.save()
				costoV = 'RCV00'
				ingresoV = 'RI000'
				pe = PeriodoContable.objects.all()
				p = len(pe)
				pk_cuenta='AC002'
				porcventa=1+ Decimal(ganancia) / 100
				Iventa= montSalida*porcventa

				if p > 0 :
					cuentaKardex(pk_cuenta,p,montSalida,costoV)
					cuentaKardex(ingresoV,p,Iventa,enviar)

				
		else: 
			if i > 0:
				CV = 0
				MD =0
				for kardex in kard :
					CV +=kardex.montoSalida
					MD +=kardex.montoEntrada
				context = {
				'kardex1':kardex1,
				'kardex':kard,
				'i':i,
				'CV':CV,
				'MD':MD,
				'final':final,
			}
			return HttpResponse(template.render(context,request ))
	return HttpResponse(template.render(context,request ))

def nuevoPeriodo(request):
	template=loader.get_template('Main/nuevoPeriodo.html')
	periodo = PeriodoContable.objects.all()
			
	mensaje=''
	if request.method=='POST':
		action = request.POST.get('action',None)
		i=1
		if action =='nuevo':
			if i > 0 :
				i=len(periodo)
				periodoanterior = periodo.get(pk=i)
				if periodoanterior.activo :
					mensaje ='Debe cerrar el periodo anterior para iniciar este'
					context={
					'periodo':periodo,
					'mensaje':mensaje,
					}
					return HttpResponse(template.render(context , request))
			fi = request.POST.get('fecha_inicio',None)
			ff = request.POST.get('fecha_final',None)
			us = request.POST.get('usuario',None)
			usf = 'desconocido'
			periodo1 = PeriodoContable()
			periodo1.fecha_inicio = fi
			periodo1.fecha_final =ff
			periodo1.usr_aperturo = us
			periodo1.usr_cerro =usf
			periodo1.save()
			if periodo1.fecha_inicio == periodo1.fecha_final :
				mensaje='no puede ingresar la misma fecha inicial y final, pero por ser pruebas admito lo que sea XD por ahorita, enrealidad solo pedira la fecha de inicio y a esta se le sumara un mes'
			periodo = PeriodoContable.objects.all()
			context={
				'periodo':periodo,
				'mensaje':mensaje,
			}
			return HttpResponse(template.render(context , request))

		elif action=='cerrar' :
			if i>0 :
				i=len(periodo)
				periodocerrar = periodo.get(pk=i)
				periodocerrar.activo=False
				periodocerrar.save()
				periodo = PeriodoContable.objects.all()
				context={
					'periodo':periodo,
					'mensaje':mensaje,
				}
				return HttpResponse(template.render(context , request))
	context={
		'periodo':periodo,
		'mensaje':mensaje,
	}
	return HttpResponse(template.render(context , request))


def reg_transaccion(request, periodo_id):
	template=loader.get_template('Main/reg_transaccion.html')
	periodo = get_object_or_404(PeriodoContable,pk=periodo_id)
	cuentas = Cuenta.objects.exclude(codigo_cuenta__contains='ACO') #Excluimos las ordenes de fabricacion
	LibroMayor1= periodo.libromayor_set.all()
	text =''
	if request.method =='POST':
		action = request.POST.get('action')
		check=request.POST.get('check')
		if action == 'insert':
			cuenta = get_object_or_404(Cuenta,pk= request.POST.get('cuenta'))
			try:
				libro = LibroMayor1.get(cuenta=cuenta.nom_cuenta)
				monto = request.POST.get('monto')
				concepto = request.POST.get('concepto')
				IVA=request.POST.get('IVA')
				diario =Diario()
				diario.mayor= libro
				diario.codCuenta = cuenta.codigo_cuenta
				diario.descripcion=request.POST.get('descripcion')
				diario.fecha=date.today()
				diario.concepto=concepto
				if concepto =='cargar':
					diario.debe=float(monto)
					diario.haber=0
					diario.save()
					libro.saldoDeudor = libro.saldoDeudor+float(monto)
					libro.save()
					if check:
						libro.saldoDeudor=(float(monto)*0.13)+libro.saldoDeudor
						libro.save()
				else :
					diario.haber=float(monto)
					diario.debe=0
					diario.save()
					libro.saldoAcreedor =libro.saldoAcreedor+float(monto)
					libro.save()
					if check:
						libro.saldoAcreedor=(float(monto)*0.13)+libro.saldoAcreedor
						libro.save()
			except (KeyError, LibroMayor.DoesNotExist):
				libro1 = LibroMayor()
				monto = request.POST.get('monto')
				concepto = request.POST.get('concepto')
				IVA=request.POST.get('IVA')
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
				diario.descripcion=request.POST.get('descripcion')
				diario.fecha=date.today()
				diario.concepto=concepto
				if concepto =='cargar':
					diario.debe=monto
					diario.haber=0
					libro1.saldoDeudor =libro1.saldoDeudor + float(monto)
					libro1.save()
					if check:
						libro1.saldoDeudor=(float(monto)*0.13)+libro1.saldoDeudor
						libro1.save()
				else :
					diario.haber=monto
					diario.debe=0
					libro1.saldoAcreedor = libro1.saldoAcreedor +float(monto)
					libro1.save()
					if check:
						libro1.saldoAcreedor=(float(monto)*0.13)+libro1.saldoAcreedor
						libro1.save()
				diario.save()
		elif action =='comprobar':
			salDebe=0
			salHaber=0
			for p in periodo.libromayor_set.all():
				salDebe += p.saldoDeudor
				salHaber += p.saldoAcreedor
			if salHaber == salDebe :
				text='comprobado saldo deudor igual al acreedor, no se si estara bien pero esa honda te cuadra XD'
			elif salDebe > salHaber :
				text ='saldo deudor mayor al acreedor, esto no cuadra'
			elif salDebe <salHaber :
				text='saldo deudor menor al saldo acreedor, esto tampoco cuadra'
		elif action=='ajuste' :
			pass
		elif action =='estados':
			pass
	lib = periodo.libromayor_set.all()
#	lib = LibroMayor.objects.filter(periodo=periodo)
	libros = LibroMayor.objects.all()
	return HttpResponse(template.render({'periodo':periodo, 'cuentas':cuentas, 'lib':lib,'libros':libros,'text':text}, request))

def depreciacion(request):
	template=loader.get_template('Main/depreciacion.html')
	periodo = PeriodoContable.objects.all()
	depreciacion=0

	
	if request.method =='POST':
		action = request.POST.get('action')
		
		if action == 'insert':
				
			vactual=request.POST.get('vactual')
			vfinal=request.POST.get('vfinal')
			vutil=request.POST.get('vutil')
			depreciacion=((float(vactual)-float(vfinal))/int(vutil))/12

				
	
	return HttpResponse(template.render({'periodo':periodo, 
		'depreciacion':depreciacion}, request))

def amortizacion(request):
	template=loader.get_template('Main/amortizacion.html')
	periodo = PeriodoContable.objects.all()
	amortizacion=0
	
	if request.method =='POST':
		action = request.POST.get('action')
		
		if action == 'insert':
				
			vactivo1=request.POST.get('vactivo1')
			tduracion=request.POST.get('tduracion')
			amortizacion=(float(vactivo1)/int(tduracion))/12
				
	
	return HttpResponse(template.render({'periodo':periodo, 
		'amortizacion':amortizacion}, request))
def agotamiento(request):
	template=loader.get_template('Main/agotamiento.html')
	periodo = PeriodoContable.objects.all()
	agotamiento=0
	
	if request.method =='POST':
		action = request.POST.get('action')
		
		if action == 'insert':
				
			vrecurso=request.POST.get('vrecurso')
			ctotal=request.POST.get('ctotal')
			agotamiento=float(vrecurso)/float(ctotal)
				
	
	return HttpResponse(template.render({'periodo':periodo, 
		'agotamiento':agotamiento}, request))

def adelantado(request):
	template=loader.get_template('Main/adelantado.html')
	periodo = PeriodoContable.objects.all()
	gperiodo=0
	
	if request.method =='POST':
		action = request.POST.get('action')
		
		if action == 'insert':
				
			gadelantado=request.POST.get('gadelantado')
			tpagado=request.POST.get('tpagado')
			tcontable=request.POST.get('tcontable')
			gperiodo=(float(gadelantado)/float(tpagado))*(float(tcontable))
		    
				
	
	return HttpResponse(template.render({'periodo':periodo, 
		'gperiodo':gperiodo}, request))

def gacumulado(request):
	template=loader.get_template('Main/gacumulado.html')
	periodo = PeriodoContable.objects.all()
	gacumulado=0
	
	if request.method =='POST':
		action = request.POST.get('action')
		
		if action == 'insert':
				
			prestamo=request.POST.get('prestamo')
			tasainteres=request.POST.get('tasainteres')
			tinteres=request.POST.get('tinteres')
			tcontable=request.POST.get('tcontable')
			gacumulado=((float(prestamo)*(float(tasainteres)/100)*float(tinteres))/12)*(float(tcontable))
		    
				
	
	return HttpResponse(template.render({'periodo':periodo, 
		'gacumulado':gacumulado}, request))

def estados (request,periodo_id):
	template=loader.get_template('Main/estados.html')
	periodo= get_object_or_404(PeriodoContable,pk=periodo_id)
	cuentasT = LibroMayor.objects.filter(periodo=periodo)
	debe =0
	haber =0

	for t in periodo.libromayor_set.all() :
		t.saldo=t.saldoDeudor - t.saldoAcreedor
		if t.saldo < 0 :
			t.saldo = t.saldo*(-1)
			haber += t.saldo
		else :
			debe +=t.saldo
		t.save()
	
	iniciarCuenta('UT')

	util =0 
	libR = LibroMayor.objects.filter(periodo=periodo,codCuenta__contains ='R')
	for t in libR :
		util += t.saldoAcreedor-t.saldoDeudor
	
#	utilidad1 = LibroMayor.objects.get(codCuenta='UT000')
#	utilidad1.saldo=util
#	utilidad1.save()
	activoC = LibroMayor.objects.filter(periodo=periodo,codCuenta__contains='AC')
	activoF = LibroMayor.objects.filter(periodo=periodo,codCuenta__contains='AF')
	activoD = LibroMayor.objects.filter(periodo=periodo,codCuenta__contains='AD')
	activoK = LibroMayor.objects.filter(periodo=periodo,codCuenta__contains='AK')
	pasivoC = LibroMayor.objects.filter(periodo=periodo,codCuenta__contains='PC')
	pasivoF = LibroMayor.objects.filter(periodo=periodo,codCuenta__contains='PF')
	pasivoD = LibroMayor.objects.filter(periodo=periodo,codCuenta__contains='PD')

	mensajeBC='No cuadra'
	if debe==haber:
		mensajeBC='Felicidades balance de comprobacion cuadra exitosamente'
	#hasta aqui todo para generar el balance comprobacion, si es el de resultado buscar las cuentas que seran afectadas, y toda la honda
	#Esta empezando por lo tanto se invierte todo el capital
	capitalS = LibroMayor.objects.filter(periodo=periodo,codCuenta__contains='CS')
	totalCapiS =0 
	for t in capitalS :
		totalCapiS += t.saldoAcreedor-t.saldoDeudor
	
	capitalI = LibroMayor.objects.filter(periodo=periodo,codCuenta__contains='CI')
	totalCapiI =0 
	for t in capitalI :
		totalCapiI += t.saldoAcreedor-t.saldoDeudor
	
	capitalD = LibroMayor.objects.filter(periodo=periodo,codCuenta__contains='CD')
	totalCapiD =0 
	for t in capitalD :
		totalCapiD += t.saldoAcreedor-t.saldoDeudor
	
	capital = LibroMayor.objects.filter(periodo=periodo,codCuenta__contains='C0000')
	totalCapi=util+totalCapiS+totalCapiI+totalCapiD

	AC = LibroMayor.objects.filter(periodo=periodo,codCuenta__contains ='AC')
	AC1=0
	for t in AC :
		AC1 += t.saldoDeudor-t.saldoAcreedor
	AF = LibroMayor.objects.filter(periodo=periodo,codCuenta__contains ='AF')
	AF1=0
	for t in AF :
		AF1 += t.saldoDeudor-t.saldoAcreedor
	AD = LibroMayor.objects.filter(periodo=periodo,codCuenta__contains ='AD')
	AD1=0
	for t in AD :
		AD1 += t.saldoDeudor-t.saldoAcreedor
	AK = LibroMayor.objects.filter(periodo=periodo,codCuenta__contains ='AK')
	AK1=0
	for t in AK :
		AK1 += t.saldoDeudor-t.saldoAcreedor

	P = LibroMayor.objects.filter(periodo=periodo,codCuenta__contains ='P')
	P1=0
	for t in P :
		P1 += t.saldoAcreedor-t.saldoDeudor

	capitalTotal=-AC1-AF1-AK1-AD1+P1+totalCapi

	context ={
#		'utilidad':utilidad1,
		'util':util,
		'periodo':periodo,
		'libR':libR,
		'cuenta':cuentasT,
		'debe':debe,
		'haber':haber,
		'mensaje':mensajeBC,
		'activoC':activoC,
		'activoF':activoF,
		'activoD':activoD,
		'activoK':activoK,
		'pasivoC':pasivoC,
		'pasivoF':pasivoF,
		'pasivoD':pasivoD,
		'capitalS':capitalS,
		'capitalI':capitalI,
		'capitalD':capitalD,
		'capital':capital,
		'totalCapi':totalCapi,
		'capitalTotal':capitalTotal,
	}
	return HttpResponse(template.render(context,request ))


#MOD
def conPuestos(request):
	puestos = Puesto.objects.all()
	val=0
	return render(request,'Main/cargo.html', {'puestos':puestos, 'val':val})

def ingresarPuesto(request):
	val=1
	if request.method =='POST':
		puesto = Puesto()
		puesto.cargo = request.POST.get('cargo')
		puesto.area = request.POST.get('area')
		puesto.salNominal = float(request.POST.get('sal'))
		puesto.total=0.0
		puesto.save()
		return redirect('contable:con_puestos')
	return render(request,'Main/cargo.html', {'val':val})

def editPuesto(request, id_puesto):
	val=2
	puesto = Puesto.objects.get(id=id_puesto)
	if request.method =='POST':
		puesto.cargo = request.POST.get('cargo')
		puesto.area = request.POST.get('area')
		puesto.salNominal = float(request.POST.get('sal'))
		puesto.save()
		return redirect('contable:con_puestos')
	return render(request,'Main/cargo.html', {'puesto':puesto, 'val':val})

def conPlanilla(request):
	p = EmpPlanilla.objects.all()
	c = Puesto.objects.all()
	val=1
	sal=0
	total=costoMO()

	if request.method =='POST':
		planilla = EmpPlanilla()
		cargo = request.POST.get('cargo')
		planilla.cargo_id = cargo
		planilla.nomEmpleado = request.POST.get('empleado')
		anios = request.POST.get('anios')
		planilla.anios = anios

		for puesto in c:
			if int(cargo) == int(puesto.id): #Necesario convertir a entero
				sal = puesto.salNominal

				planilla.isss = sal*0.075
				planilla.afp = sal*0.0675

				if puesto.cargo == "Operario":
					planilla.insaforp = sal*0.01
				else:
					planilla.insaforp = 0

				salDia = sal/30
				planilla.vaca = salDia*15*(1 + 0.30 + 0.075 + 0.0675) 

				if int(anios)>1:
					if int(anios)<3:
						planilla.aguinaldo = salDia*15
					if int(anios)>=3 and int(anios)<10:
						planilla.aguinaldo = salDia*18
					if int(anios)>=10:
						planilla.aguinaldo = salDia*21
				else:
					planilla.aguinaldo=0
				
				planilla.cmo = float(sal) + planilla.isss + planilla.afp + planilla.insaforp + planilla.vaca/12 + planilla.aguinaldo/12
				planilla.salPersonal = planilla.cmo #ASIGNACION INICIAL DE SALARIO INDIVIDUAL
				puesto.total += planilla.cmo
				puesto.save()
				planilla.save()
				break
		return redirect('contable:con_planilla')
	return render(request,'Main/planilla.html', {'p':p, 'c':c, 'val':val, 'total':total})

def menuSisPlanilla(request):
	val=0
	return render(request,'Main/planilla.html', {'val':val})

def costoMO():
	total=0
	puestos = Puesto.objects.all()
	for puesto in puestos:
		total += puesto.total
	return total

def areaPlanilla(request):
	p = EmpPlanilla.objects.all()
	c = Puesto.objects.all()
	to=0
	tm=0
	ta=0
	val=2
	total = costoMO()
	for puesto in c:
		if puesto.area == "Produccion":
			to += puesto.total
		if puesto.area == "Mercadeo":
			tm += puesto.total
		if puesto.area == "Administracion":
			ta += puesto.total
	return render(request,'Main/planilla.html', {'to':to, 'tm':tm, 'ta':ta, 'p':p, 'c':c, 'val':val, 'total':total})

def adminPlanilla(request, id_planilla):
	p = EmpPlanilla.objects.get(id=id_planilla)
	s = sancionSalarial.objects.filter(planilla_id=id_planilla)
	c = Puesto.objects.get(id=p.cargo_id)
	val=1
	return render(request,'Main/admin-planilla.html', {'p':p, 'val':val, 's':s, 'c':c})

def elmPlanilla(request, id_planilla):
	val=2
	p = EmpPlanilla.objects.get(id=id_planilla)
	if request.method == 'POST':
		p.delete()
		return redirect('contable:con_planilla')
	return render(request, 'Main/admin-planilla.html', {'p': p, 'val':val})

def sanPlanilla(request, id_planilla):
	val=3
	p = EmpPlanilla.objects.get(id=id_planilla)
	if request.method == 'POST':

		tiempo = request.POST.get('tiempo')
		num = request.POST.get('num')

		san = sancionSalarial()
		san.tiempo = tiempo
		san.unidades = num
		san.planilla_id = id_planilla

		if tiempo == "dias":
			san.monto = (p.salPersonal/30)*int(num) #CALCULO DE DIAS DESCONTADOS
			p.salPersonal = p.salPersonal - san.monto
		if tiempo == "horas":
			san.monto = ((p.salPersonal/30)/8)*int(num) #CALCULO DE HORAS DESCONTADOS
			p.salPersonal = p.salPersonal - san.monto

		san.save()
		p.save()
		return redirect('contable:con_planilla')
	return render(request, 'Main/admin-planilla.html', {'p': p, 'val':val})

def conProrrateo(request):
	periodo = PeriodoContable.objects.all()
	idp=len(periodo)

	for p in periodo:
		if p.activo:
			idp=p.id
	lmayor = LibroMayor.objects.all()

	#Inicializacion
	luz=0
	agua=0
	so=0
	gas=0
	maq=0
	alquiler=0
	d1=[None]*5
	d2=[None]*5
	d3=[None]*5
	d4=[None]*5
	d5=[None]*5
	d6=[None]*5

	for mayor in lmayor:
		if mayor.periodo_id==idp:
			if mayor.codCuenta == 'PC987':
				luz=mayor.saldoAcreedor
			if mayor.codCuenta == 'PC988':
				agua=mayor.saldoAcreedor
			if mayor.codCuenta == 'PC989':
				so=mayor.saldoAcreedor
			if mayor.codCuenta == 'PC990':
				gas=mayor.saldoAcreedor
			if mayor.codCuenta == 'PC991':
				maq=mayor.saldoAcreedor
			if mayor.codCuenta == 'PC992':
				alquiler=mayor.saldoAcreedor
	#Energia
	total=2039.7696
	por=1942.864/total
	luz=luz*por

	#Bases
	ne1=1
	ne2=2
	ne3=4
	ne4=2
	ne5=1

	base=ne1+ne2+ne3+ne4+ne5

	d1[0] = (luz/base)*ne1
	d1[1] = (luz/base)*ne2
	d1[2] = (luz/base)*ne3
	d1[3] = (luz/base)*ne4
	d1[4] = (luz/base)*ne5

	d2[0] = (agua/base)*ne1
	d2[1] = (agua/base)*ne2
	d2[2] = (agua/base)*ne3
	d2[3] = (agua/base)*ne4
	d2[4] = (agua/base)*ne5

	d3[0] = (so/base)*ne1 
	d3[1] = (so/base)*ne2
	d3[2] = (so/base)*ne3
	d3[3] = (so/base)*ne4
	d3[4] = (so/base)*ne5

	d4[0] = (gas/base)*ne1
	d4[1] = (gas/base)*ne2
	d4[2] = (gas/base)*ne3
	d4[3] = (gas/base)*ne4
	d4[4] = (gas/base)*ne5

	d5[0] = (maq/base)*ne1
	d5[1] = (maq/base)*ne2
	d5[2] = (maq/base)*ne3
	d5[3] = (maq/base)*ne4
	d5[4] = (maq/base)*ne5

	d6[0] = (alquiler/base)*ne1
	d6[1] = (alquiler/base)*ne2
	d6[2] = (alquiler/base)*ne3
	d6[3] = (alquiler/base)*ne4
	d6[4] = (alquiler/base)*ne5
	return render(request, 'Main/cif.html', {'d1':d1, 'd2':d2, 'd3':d3, 'd4':d4, 'd5':d5, 'd6':d6})