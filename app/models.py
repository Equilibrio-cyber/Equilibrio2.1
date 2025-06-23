from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.String(20), nullable=False)
    edad = db.Column(db.Integer)
    direccion = db.Column(db.String(100))
    comuna = db.Column(db.String(50))
    genero = db.Column(db.String(20))
    prevision = db.Column(db.String(20))
    ocupacion = db.Column(db.String(50))
    correo = db.Column(db.String(100))
    contacto = db.Column(db.String(20))
    fecha_ingreso = db.Column(db.String(20))
    rut_apoderado = db.Column(db.String(20))
    nombre_apoderado = db.Column(db.String(100))
    correo_apoderado = db.Column(db.String(100))
    contacto_apoderado = db.Column(db.String(20))

class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    tipo_pago = db.Column(db.String(50))
    fecha_pago = db.Column(db.String(20))
    respaldo_archivo = db.Column(db.String(100))
    monto = db.Column(db.Integer)  # 💰 Monto en pesos CLP
    paciente = db.relationship('Paciente', backref='pagos')

class Profesional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.String(20), nullable=False, unique=True)
    correo = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    fecha_ingreso = db.Column(db.String(10), nullable=False)

class Evolucion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    fecha = db.Column(db.String(10), nullable=False)
    anotacion = db.Column(db.Text, nullable=False)
    paciente = db.relationship('Paciente', backref='evoluciones')
    estado_paciente = db.Column(db.Integer, nullable=True)




from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.String(20), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.String(200))
    comuna = db.Column(db.String(100))
    genero = db.Column(db.String(20))
    prevision = db.Column(db.String(50))
    ocupacion = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    contacto = db.Column(db.String(20))
    fecha_ingreso = db.Column(db.String(20))
    rut_apoderado = db.Column(db.String(20))
    nombre_apoderado = db.Column(db.String(100))
    correo_apoderado = db.Column(db.String(100))
    contacto_apoderado = db.Column(db.String(20))


class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    tipo_pago = db.Column(db.String(50), nullable=False)
    fecha_pago = db.Column(db.String(20), nullable=False)
    respaldo_archivo = db.Column(db.String(200))
    monto = db.Column(db.Integer)

    paciente = db.relationship('Paciente', backref='pagos')


class Profesional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100))
    rut = db.Column(db.String(20), unique=True)
    correo = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    fecha_ingreso = db.Column(db.String(20))


class Evolucion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    anotacion = db.Column(db.String(500), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    estado_paciente = db.Column(db.Integer, nullable=False)

    paciente = db.relationship('Paciente', backref='evoluciones')


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.String(20), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.String(200))
    comuna = db.Column(db.String(100))
    genero = db.Column(db.String(20))
    prevision = db.Column(db.String(50))
    ocupacion = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    contacto = db.Column(db.String(20))
    fecha_ingreso = db.Column(db.String(20))
    rut_apoderado = db.Column(db.String(20))
    nombre_apoderado = db.Column(db.String(100))
    correo_apoderado = db.Column(db.String(100))
    contacto_apoderado = db.Column(db.String(20))


class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    tipo_pago = db.Column(db.String(50), nullable=False)
    fecha_pago = db.Column(db.String(20), nullable=False)
    respaldo_archivo = db.Column(db.String(200))
    monto = db.Column(db.Integer)

    paciente = db.relationship('Paciente', backref='pagos')


class Profesional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100))
    rut = db.Column(db.String(20), unique=True)
    correo = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    fecha_ingreso = db.Column(db.String(20))


class Evolucion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    anotacion = db.Column(db.String(500), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    estado_paciente = db.Column(db.Integer, nullable=False)

    paciente = db.relationship('Paciente', backref='evoluciones')

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.String(20), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.String(200))
    comuna = db.Column(db.String(100))
    genero = db.Column(db.String(20))
    prevision = db.Column(db.String(50))
    ocupacion = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    contacto = db.Column(db.String(20))
    fecha_ingreso = db.Column(db.String(20))
    rut_apoderado = db.Column(db.String(20))
    nombre_apoderado = db.Column(db.String(100))
    correo_apoderado = db.Column(db.String(100))
    contacto_apoderado = db.Column(db.String(20))


class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    tipo_pago = db.Column(db.String(50), nullable=False)
    fecha_pago = db.Column(db.String(20), nullable=False)
    respaldo_archivo = db.Column(db.String(200))
    monto = db.Column(db.Integer)

    paciente = db.relationship('Paciente', backref='pagos')


class Profesional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100))
    rut = db.Column(db.String(20), unique=True)
    correo = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    fecha_ingreso = db.Column(db.String(20))


class Evolucion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    anotacion = db.Column(db.String(500), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    estado_paciente = db.Column(db.Integer, nullable=False)

    paciente = db.relationship('Paciente', backref='evoluciones')


class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    profesional_id = db.Column(db.Integer, db.ForeignKey('profesional.id'), nullable=False)
    fecha = db.Column(db.String, nullable=False)  # <- Aquí está el campo correcto
    motivo = db.Column(db.String(200), nullable=False)

    paciente = db.relationship('Paciente', backref='citas')
    profesional = db.relationship('Profesional', backref='citas')
    estado = db.Column(db.String(50), default='Pendiente')







