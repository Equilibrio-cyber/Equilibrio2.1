from flask import session
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Paciente, Profesional, Pago, Evolucion, Cita
from . import db
from datetime import datetime
from datetime import date
from . import db
from flask import make_response, send_file
from xhtml2pdf import pisa
from io import BytesIO
import pandas as pd
import os
from werkzeug.utils import secure_filename
from app.models import Pago
from flask import send_file
from matplotlib.figure import Figure
import base64
import io
from collections import defaultdict


main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        if usuario == "EQUILIBRIO" and clave == "123456":
            session['usuario'] = usuario
            return redirect(url_for('main.dashboard'))
        else:
            flash('Usuario o clave incorrectos', 'error')
    return render_template("login.html")

@main.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@main.route('/registrar_paciente', methods=['GET', 'POST'])
def registrar_paciente():
    if request.method == 'POST':
        rut = request.form['rut']
        nombre = request.form['nombre']
        fecha_nacimiento = request.form['fecha_nacimiento']
        edad = datetime.now().year - int(fecha_nacimiento.split('-')[0])
        direccion = request.form['direccion']
        comuna = request.form['comuna']
        genero = request.form['genero']
        prevision = request.form['prevision']
        ocupacion = request.form['ocupacion']
        correo = request.form['correo']
        contacto = request.form['contacto']
        fecha_ingreso = request.form['fecha_ingreso']
        rut_apoderado = request.form['rut_apoderado']
        nombre_apoderado = request.form['nombre_apoderado']
        correo_apoderado = request.form['correo_apoderado']
        contacto_apoderado = request.form['contacto_apoderado']

        nuevo = Paciente(
            rut=rut,
            nombre=nombre,
            fecha_nacimiento=fecha_nacimiento,
            edad=edad,
            direccion=direccion,
            comuna=comuna,
            genero=genero,
            prevision=prevision,
            ocupacion=ocupacion,
            correo=correo,
            contacto=contacto,
            fecha_ingreso=fecha_ingreso,
            rut_apoderado=rut_apoderado,
            nombre_apoderado=nombre_apoderado,
            correo_apoderado=correo_apoderado,
            contacto_apoderado=contacto_apoderado
        )

        db.session.add(nuevo)
        db.session.commit()
        flash("✅ Paciente registrado exitosamente.")
        return redirect(url_for('main.registrar_paciente'))

    return render_template("registro_paciente.html")

@main.route('/visualizar_pacientes')
def visualizar_pacientes():
    pacientes = Paciente.query.all()
    return render_template('ver_pacientes.html', pacientes=pacientes)

@main.route('/editar_paciente/<int:id>', methods=['GET', 'POST'])
def editar_paciente(id):
    paciente = Paciente.query.get_or_404(id)

    if request.method == 'POST':
        paciente.rut = request.form['rut']
        paciente.nombre = request.form['nombre']
        paciente.fecha_nacimiento = request.form['fecha_nacimiento']
        paciente.edad = datetime.now().year - int(paciente.fecha_nacimiento.split('-')[0])
        paciente.direccion = request.form['direccion']
        paciente.comuna = request.form['comuna']
        paciente.genero = request.form['genero']
        paciente.prevision = request.form['prevision']
        paciente.ocupacion = request.form['ocupacion']
        paciente.correo = request.form['correo']
        paciente.contacto = request.form['contacto']
        paciente.fecha_ingreso = request.form['fecha_ingreso']
        paciente.rut_apoderado = request.form['rut_apoderado']
        paciente.nombre_apoderado = request.form['nombre_apoderado']
        paciente.correo_apoderado = request.form['correo_apoderado']
        paciente.contacto_apoderado = request.form['contacto_apoderado']

        db.session.commit()
        flash('✅ Paciente actualizado correctamente.')
        return redirect(url_for('main.visualizar_pacientes'))

    return render_template('editar_paciente.html', paciente=paciente)

@main.route('/eliminar_paciente/<int:id>')
def eliminar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    flash('🗑️ Paciente eliminado correctamente.')
    return redirect(url_for('main.visualizar_pacientes'))



@main.route('/exportar_pdf')
def exportar_pdf():
    pacientes = Paciente.query.all()
    html = render_template("pdf_pacientes.html", pacientes=pacientes)
    result = BytesIO()
    pisa.CreatePDF(html, dest=result)
    result.seek(0)
    return send_file(result, download_name="pacientes.pdf", as_attachment=True)

@main.route('/exportar_excel')
def exportar_excel():
    pacientes = Paciente.query.all()
    data = [{
        "RUT": p.rut,
        "Nombre": p.nombre,
        "Edad": p.edad,
        "Correo": p.correo,
        "Contacto": p.contacto,
        "Fecha Ingreso": p.fecha_ingreso
    } for p in pacientes]
    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    return send_file(output, download_name="pacientes.xlsx", as_attachment=True)

@main.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('main.login'))



# Ruta absoluta a la carpeta /uploads fuera de /app
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))

@main.route('/registrar_pago', methods=['GET', 'POST'])
def registrar_pago():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))

    
    pacientes = Paciente.query.all()

    if request.method == 'POST':
        paciente_id = request.form['paciente_id']
        tipo_pago = request.form['tipo_pago']
        fecha_pago = request.form['fecha_pago']
        monto = int(request.form['monto'])  # 👈 IMPORTANTE

        respaldo = request.files['respaldo']
        nombre_archivo = None
        if respaldo and respaldo.filename != '':
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            nombre_archivo = secure_filename(respaldo.filename)
            respaldo.save(os.path.join(UPLOAD_FOLDER, nombre_archivo))

        nuevo_pago = Pago(
            paciente_id=paciente_id,
            tipo_pago=tipo_pago,
            fecha_pago=fecha_pago,
            respaldo_archivo=nombre_archivo,
            monto=monto  # 👈 AQUÍ SE GUARDA
        )
        print(f"💰 Monto ingresado: {monto}")

        db.session.add(nuevo_pago)
        db.session.commit()
        flash("✅ Pago registrado correctamente.")
        return redirect(url_for('main.registrar_pago'))

    return render_template("registro_pago.html", pacientes=pacientes)



@main.route('/ver_pagos')
def ver_pagos():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))
    pagos = Pago.query.all()
    return render_template('ver_pagos.html', pagos=pagos)

@main.route('/exportar_pagos_pdf')
def exportar_pagos_pdf():
    pagos = Pago.query.all()
    html = render_template("pdf_pagos.html", pagos=pagos)
    result = BytesIO()
    pisa.CreatePDF(html, dest=result)
    result.seek(0)
    return send_file(result, download_name="pagos.pdf", as_attachment=True)

@main.route('/exportar_pagos_excel')
def exportar_pagos_excel():
    pagos = Pago.query.all()
    data = [{
        "Paciente": p.paciente.nombre,
        "Tipo de Pago": p.tipo_pago,
        "Fecha de Pago": p.fecha_pago,
        "Respaldo": p.respaldo_archivo or "Sin respaldo",
        "Monto (CLP)": p.monto
    } for p in pagos]
    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    return send_file(output, download_name="pagos.xlsx", as_attachment=True)

@main.route('/descargar_respaldo/<archivo>')
def descargar_respaldo(archivo):
    ruta = os.path.join(UPLOAD_FOLDER, archivo)
    if os.path.exists(ruta):
        return send_file(ruta, as_attachment=True)
    else:
        flash("❌ Archivo no encontrado.")
        return redirect(url_for('main.ver_pagos'))

    
@main.route('/reporte_pagos')
def reporte_pagos():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))

    pagos = Pago.query.all()
    resumen = defaultdict(lambda: {
        'total': 0,
        'Transferencia': 0,
        'Débito': 0,
        'Crédito': 0,
        'Efectivo': 0,
        'monto_total': 0
    })

    for pago in pagos:
        fecha = datetime.strptime(pago.fecha_pago, "%Y-%m-%d")
        clave = f"{fecha.month:02d}/{fecha.year}"
        resumen[clave]['total'] += 1
        resumen[clave][pago.tipo_pago] += 1
        resumen[clave]['monto_total'] += pago.monto or 0

    resumen_ordenado = dict(sorted(resumen.items(), key=lambda x: datetime.strptime(x[0], "%m/%Y"), reverse=True))

    return render_template("reporte_mensual.html", resumen=resumen_ordenado)

@main.route('/exportar_reporte_mensual_pdf')
def exportar_reporte_mensual_pdf():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))

    pagos = Pago.query.all()
    resumen = defaultdict(lambda: {
        'total': 0,
        'Transferencia': 0,
        'Débito': 0,
        'Crédito': 0,
        'Efectivo': 0,
        'monto_total': 0
    })

    for pago in pagos:
        fecha = datetime.strptime(pago.fecha_pago, "%Y-%m-%d")
        clave = f"{fecha.month:02d}/{fecha.year}"
        resumen[clave]['total'] += 1
        resumen[clave][pago.tipo_pago] += 1
        resumen[clave]['monto_total'] += pago.monto or 0

    resumen_ordenado = dict(sorted(resumen.items(), key=lambda x: datetime.strptime(x[0], "%m/%Y"), reverse=True))

    html = render_template("pdf_reporte_mensual.html", resumen=resumen_ordenado)
    result = BytesIO()
    pisa.CreatePDF(html, dest=result)
    result.seek(0)
    return send_file(result, download_name="reporte_mensual_pagos.pdf", as_attachment=True)

@main.route('/exportar_reporte_mensual_excel')
def exportar_reporte_mensual_excel():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))

    pagos = Pago.query.all()
    resumen = defaultdict(lambda: {
        'total': 0,
        'Transferencia': 0,
        'Débito': 0,
        'Crédito': 0,
        'Efectivo': 0,
        'monto_total': 0
    })

    for pago in pagos:
        fecha = datetime.strptime(pago.fecha_pago, "%Y-%m-%d")
        clave = f"{fecha.month:02d}/{fecha.year}"
        resumen[clave]['total'] += 1
        resumen[clave][pago.tipo_pago] += 1
        resumen[clave]['monto_total'] += pago.monto or 0

    # Convertir resumen a DataFrame
    data = []
    for mes, datos in resumen.items():
        data.append({
            'Mes/Año': mes,
            'Total Pagos': datos['total'],
            'Transferencia': datos['Transferencia'],
            'Débito': datos['Débito'],
            'Crédito': datos['Crédito'],
            'Efectivo': datos['Efectivo'],
            'Total CLP': datos['monto_total']
        })

    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    return send_file(output, download_name="reporte_mensual_pagos.xlsx", as_attachment=True)

# 🗑️ Eliminar pago
@main.route('/eliminar_pago/<int:id>', methods=['POST'])
def eliminar_pago(id):
    pago = Pago.query.get_or_404(id)
    db.session.delete(pago)
    db.session.commit()
    flash("🗑️ Pago eliminado.")
    return redirect(url_for('main.ver_pagos'))

# ✏️ Editar pago
@main.route('/editar_pago/<int:id>', methods=['GET', 'POST'])
def editar_pago(id):
    pago = Pago.query.get_or_404(id)
    pacientes = Paciente.query.all()

    if request.method == 'POST':
        pago.paciente_id = request.form['paciente_id']
        pago.tipo_pago = request.form['tipo_pago']
        pago.fecha_pago = request.form['fecha_pago']
        pago.monto = int(request.form['monto'])

        db.session.commit()
        flash("✏️ Pago editado correctamente.")
        return redirect(url_for('main.ver_pagos'))

    return render_template("editar_pago.html", pago=pago, pacientes=pacientes)

@main.route('/registrar_profesional', methods=['GET', 'POST'])
def registrar_profesional():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        especialidad = request.form['especialidad']
        rut = request.form['rut']
        correo = request.form['correo']
        telefono = request.form['telefono']
        fecha_ingreso = request.form['fecha_ingreso']

        profesional = Profesional(
            nombre=nombre,
            especialidad=especialidad,
            rut=rut,
            correo=correo,
            telefono=telefono,
            fecha_ingreso=fecha_ingreso
        )
        db.session.add(profesional)
        db.session.commit()
        flash("✅ Profesional registrado correctamente.")
        return redirect(url_for('main.ver_profesionales'))

    return render_template("registrar_profesional.html")

@main.route('/ver_profesionales')
def ver_profesionales():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))

    profesionales = Profesional.query.all()
    return render_template('ver_profesionales.html', profesionales=profesionales)

@main.route('/eliminar_profesional/<int:id>', methods=['POST'])
def eliminar_profesional(id):
    profesional = Profesional.query.get_or_404(id)
    db.session.delete(profesional)
    db.session.commit()
    flash("🗑️ Profesional eliminado correctamente.")
    return redirect(url_for('main.ver_profesionales'))

@main.route('/editar_profesional/<int:id>', methods=['GET', 'POST'])
def editar_profesional(id):
    profesional = Profesional.query.get_or_404(id)

    if request.method == 'POST':
        profesional.nombre = request.form['nombre']
        profesional.especialidad = request.form['especialidad']
        profesional.rut = request.form['rut']
        profesional.correo = request.form['correo']
        profesional.telefono = request.form['telefono']
        profesional.fecha_ingreso = request.form['fecha_ingreso']

        db.session.commit()
        flash("✏️ Profesional actualizado correctamente.")
        return redirect(url_for('main.ver_profesionales'))

    return render_template("editar_profesional.html", profesional=profesional)

@main.route('/exportar_profesionales_pdf')
def exportar_profesionales_pdf():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))

    profesionales = Profesional.query.all()
    html = render_template("pdf_profesionales.html", profesionales=profesionales)

    result = BytesIO()
    pisa.CreatePDF(html, dest=result)
    result.seek(0)
    return send_file(result, download_name="profesionales.pdf", as_attachment=True)

@main.route('/exportar_profesionales_excel')
def exportar_profesionales_excel():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))

    profesionales = Profesional.query.all()
    data = [{
        "Nombre": p.nombre,
        "Especialidad": p.especialidad,
        "RUT": p.rut,
        "Correo": p.correo,
        "Teléfono": p.telefono,
        "Fecha Ingreso": p.fecha_ingreso
    } for p in profesionales]

    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    return send_file(output, download_name="profesionales.xlsx", as_attachment=True)

@main.route('/seleccionar_paciente_ficha', methods=['GET', 'POST'])
def seleccionar_paciente_ficha():
    pacientes = Paciente.query.all()

    if request.method == 'POST':
        paciente_id = request.form['paciente_id']
        return redirect(url_for('main.ficha_clinica', id=paciente_id))

    return render_template('seleccionar_paciente_ficha.html', pacientes=pacientes)



@main.route('/ficha_clinica/<int:id>', methods=['GET', 'POST'])
def ficha_clinica(id):
    paciente = Paciente.query.get_or_404(id)

    if request.method == 'POST':
        fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
        anotacion = request.form['anotacion']
        estado_paciente = int(request.form['estado_paciente'])

        nueva_evolucion = Evolucion(
            paciente_id=id,
            anotacion=anotacion,
            fecha=fecha,
            estado_paciente=estado_paciente
        )
        db.session.add(nueva_evolucion)
        db.session.commit()
        flash("📝 Evolución registrada correctamente.")
        return redirect(url_for('main.ficha_clinica', id=id))

    evoluciones = Evolucion.query.filter_by(paciente_id=id).order_by(Evolucion.fecha.desc()).all()
    return render_template('ficha_clinica.html', paciente=paciente, evoluciones=evoluciones)


@main.route('/ver_ficha_clinica')
def ver_ficha_clinica():
    pacientes = Paciente.query.all()
    return render_template('ver_ficha_clinica.html', pacientes=pacientes)

@main.route('/exportar_ficha_pdf/<int:id>')
def exportar_ficha_pdf(id):
    paciente = Paciente.query.get_or_404(id)
    evoluciones = Evolucion.query.filter_by(paciente_id=id).order_by(Evolucion.fecha.desc()).all()
    html = render_template('pdf_ficha_clinica.html', paciente=paciente, evoluciones=evoluciones)
    result = BytesIO()
    pisa.CreatePDF(html, dest=result)
    result.seek(0)
    return send_file(result, download_name=f"ficha_clinica_{paciente.nombre}.pdf", as_attachment=True)

@main.route('/exportar_ficha_excel/<int:id>')
def exportar_ficha_excel(id):
    paciente = Paciente.query.get_or_404(id)
    evoluciones = Evolucion.query.filter_by(paciente_id=id).order_by(Evolucion.fecha.desc()).all()

    data = [{
        "Fecha": evo.fecha,
        "Estado (1-10)": evo.estado_paciente,
        "Anotación": evo.anotacion
    } for evo in evoluciones]

    df = pd.DataFrame(data)
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    return send_file(output, download_name=f"ficha_clinica_{paciente.nombre}.xlsx", as_attachment=True)

@main.route('/estadisticas_clinicas/<int:id>')
def estadisticas_clinicas(id):
    paciente = Paciente.query.get_or_404(id)
    evoluciones = Evolucion.query.filter_by(paciente_id=id).order_by(Evolucion.fecha).all()

    datos = [{
        'fecha': evo.fecha,
        'estado': evo.estado_paciente
    } for evo in evoluciones]

    return render_template("estadisticas_clinicas.html", paciente=paciente, datos=datos)

@main.route('/registrar_cita', methods=['GET', 'POST'])
def registrar_cita():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))

    pacientes = Paciente.query.all()
    profesionales = Profesional.query.all()

    if request.method == 'POST':
        paciente_id = request.form['paciente_id']
        profesional_id = request.form['profesional_id']
        fecha = request.form['fecha']
        motivo = request.form['motivo']
        estado = request.form['estado']


        nueva_cita = Cita(
            paciente_id=paciente_id,
            profesional_id=profesional_id,
            fecha=fecha,
            motivo=motivo,
            estado=estado,
        )
        db.session.add(nueva_cita)
        db.session.commit()
        
        flash("✅ Cita registrada correctamente.")
        return redirect(url_for('main.registrar_cita'))

    return render_template('registro_cita.html', pacientes=pacientes, profesionales=profesionales)

@main.route('/ver_citas')
def ver_citas():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))

    citas = Cita.query.order_by(Cita.fecha.desc()).all()

    return render_template("ver_citas.html", citas=citas)

@main.route('/seleccionar_historial_citas', methods=['GET', 'POST'])
def seleccionar_historial_citas():
    if 'usuario' not in session:
        return redirect(url_for('main.login'))

    pacientes = Paciente.query.all()

    if request.method == 'POST':
        paciente_id = request.form['paciente_id']
        return redirect(url_for('main.historial_citas', id=paciente_id))

    return render_template('seleccionar_historial_citas.html', pacientes=pacientes)

@main.route('/historial_citas/<int:id>')
def historial_citas(id):
    paciente = Paciente.query.get_or_404(id)
    citas = Cita.query.filter_by(paciente_id=id).order_by(Cita.fecha.desc()).all()
    return render_template("historial_citas.html", paciente=paciente, citas=citas)



@main.route('/reporte_ficha_clinica/<int:id>')
def reporte_ficha_clinica(id):
    paciente = Paciente.query.get_or_404(id)
    evoluciones = Evolucion.query.filter_by(paciente_id=id).order_by(Evolucion.fecha).all()

    # Crear gráfico con matplotlib
    fig = Figure()
    ax = fig.subplots()

    fechas = [ev.fecha.strftime("%d/%m/%Y") for ev in evoluciones]
    estados = [ev.estado_paciente for ev in evoluciones]

    ax.plot(fechas, estados, marker='o', linestyle='-', color='blue')
    ax.set_title('Evolución del Paciente')
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Estado (1-10)')
    ax.grid(True)
    fig.autofmt_xdate()

    # Convertir gráfico a imagen en base64 para insertar en HTML
    
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render_template('reporte_ficha_clinica.html', paciente=paciente, evoluciones=evoluciones, grafico=img_base64)

@main.route('/reporte_ficha_pdf/<int:id>')
def reporte_ficha_pdf(id):
    paciente = Paciente.query.get_or_404(id)
    evoluciones = Evolucion.query.filter_by(paciente_id=id).order_by(Evolucion.fecha.asc()).all()
    html = render_template("pdf_ficha_clinica.html", paciente=paciente, evoluciones=evoluciones)
    result = BytesIO()
    pisa.CreatePDF(html, dest=result)
    result.seek(0)
    return send_file(result, download_name=f"ficha_clinica_{paciente.nombre}.pdf", as_attachment=True)

@main.route('/seleccionar_paciente_contrato', methods=['GET', 'POST'])
def seleccionar_paciente_contrato():
    pacientes = Paciente.query.all()

    if request.method == 'POST':
        paciente_id = request.form['paciente_id']
        return redirect(url_for('main.ver_contrato_paciente', id=paciente_id))

    return render_template('seleccionar_paciente_contrato.html', pacientes=pacientes)

@main.route('/ver_contrato_paciente/<int:id>')
def ver_contrato_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    return render_template('contrato_paciente.html', paciente=paciente, date=date)  # ⬅️ AQUI

@main.route('/descargar_contrato/<int:id>')
def descargar_contrato(id):
    paciente = Paciente.query.get_or_404(id)
    html = render_template("contrato_paciente_pdf.html", paciente=paciente, date=date)  # ⬅️ AQUI TAMBIÉN
    result = BytesIO()
    pisa.CreatePDF(html, dest=result)
    result.seek(0)
    return send_file(result, download_name=f"Contrato_{paciente.nombre}.pdf", as_attachment=True)
