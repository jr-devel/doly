import os
from flask import request, Blueprint, render_template, redirect, url_for, flash, session, Response
from flask_login import login_required
from datetime import datetime
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
import re
from app.database import db
from app.models.Persona import Persona
from app.models.UserAccount import UserAccount
from app.models.ClientType import ClientType
from app.models.Client import Client
from app.models.Employee import Employee
import app.log_control as log

# Define the Blueprint for authentication routes
bp = Blueprint('auth', __name__, url_prefix='/auth')

def form_validation_signup(form:dict) -> list:
    errors = []
    if not form['full_name'] or len(form['full_name']) < 3 or len(form['full_name']) > 100:
        errors.append("El nombre completo debe tener entre 3 y 100 caracteres.")
    if not form['birth_date']:
        errors.append("La fecha de nacimiento es obligatoria.")
    else:
        try:
            birth_date = datetime.strptime(form['birth_date'], '%Y-%m-%d').date()
            if birth_date > datetime.now().date():
                errors.append("La fecha de nacimiento no puede ser en el futuro.")
        except ValueError:
            errors.append("La fecha de nacimiento no es válida.")
    if not form['email'] or not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', form['email']):
        errors.append("El correo electrónico no es válido.")
    if not form['phone'] or len(form['phone']) < 7 or len(form['phone']) > 15:
        errors.append("El número de teléfono debe tener entre 7 y 15 caracteres.")
    if not form['username'] or len(form['username']) < 3 or len(form['username']) > 50 or not re.match(r'^[A-Za-z0-9_]+$', form['username']):
        errors.append("El nombre de usuario debe tener entre 3 y 50 caracteres.")
    if not form['password'] or len(form['password']) < 8:
        errors.append("La contraseña debe tener al menos 8 caracteres.")
    passformat = re.compile(r"^[^'\";\\<>]*$")
    if not passformat.match(form['password']):
        errors.append("La contraseña contiene caracteres no permitidos.")
    if form['role'] not in ['client', 'employee', 'company_admin', 'sys_admin', 'audit_admin', 'support_staff']:
        errors.append("El rol seleccionado no es válido.")
    return errors

@bp.route('/signup', methods=['GET', 'POST'])
def signup() -> Response:
    """Registers a new user as Client/Employee/Company/Admin/.../ based on the form input."""
    if request.method == 'POST':
        log.log_info("Processing signup form submission.")
        errors = []
        form = {
            'full_name': request.form.get('full_name', '').strip(),
            'birth_date': request.form.get('birth_date', '').strip(),
            'email': request.form.get('email', '').strip(),
            'phone': request.form.get('phone', '').strip(),
            'username': request.form.get('username', '').strip(),
            'password': request.form.get('password', '').strip(),
            'role': request.form.get('role', '').strip()
        }
        # ------------ Input validation --------------
        errors = form_validation_signup(form)
        if errors:
            for error in errors:
                flash(error, "warning")
                log.log_warning(error)
            return render_template('auth/signup.html', errors=errors, **form)
        # -------------- Create Persona ---------------#
        try:
            persona = Persona(
                full_name=form['full_name'],
                birth_date=form['birth_date'],
                email=form['email'],
                phone=form['phone']
            )
            db.session.add(persona)
            db.session.flush()  # To get persona.id_persona
            log.log_info("persona created successfully.")
        except Exception as e:
            db.session.rollback()
            log.log_error(f"Error al crear persona: {e}")
            flash(f"Error al crear persona", "danger")
            return render_template('auth/signup.html', errors=[f"Conjunto de datos ya existentes"], **form)
        # -------------- Create UserAccount ---------------#
        try:
            user_account = UserAccount(
                username=form['username'],
                password=generate_password_hash(form['password']),
                role=form['role'],
                persona_id=persona.id_persona
            )
            db.session.add(user_account)
            db.session.flush()  # To get user_account.id_user
            log.log_info("user created successfully.")
        except Exception as e:
            db.session.rollback()
            log.log_error(f"Error al crear cuenta de usuario: {e}")
            flash(f"Error al crear cuenta de usuario: {e}", "danger")
            return render_template('auth/signup.html', errors=[f"Error al crear cuenta de usuario: {e}"], **form)
        # -------------- Create UserAccount ---------------#
        try:
            if form['role'] == 'client':
                client = Client(
                    user_id=user_account.id_user,
                    ine=False,
                    client_type=None,
                    license_number=None,
                    message_permission=False,
                    terms_agreement=True
                )
                db.session.add(client)
            # elif form['role'] == 'employee':
            #     employee = Employee(
            #         user_id=user_account.id_user,
            #         employee_type_id=None
            #     )
            #     db.session.add(employee)
            # elif form['role'] in ['company_admin', 'sys_admin', 'audit_admin', 'support_staff']:
            #     # Additional logic for other roles can be added here
            #     pass
            # # -------------- Redirect to login ---------------#
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                log.log_error(f"Error al guardar en la base de datos: {e}")
            flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for('auth.login'))  # 201 Created
        except Exception as e:
            db.session.rollback()
            flash(f"Error al crear el usuario: {e}", "danger")
            log.log_error(f"Error al crear el usuario: {e}")
            return render_template('auth/signup.html', errors=[f"Error al crear el usuario: {e}"], **form)
    return render_template('auth/signup.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Validates user credentials and logs the user by type."""
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        # ------------ Input validation --------------
        if not username or not password:
            flash("Por favor, complete todos los campos.", "warning") #400 Bad Request
            log.log_warning("Campos incompletos en el intento de inicio de sesión. 400 Bad Request.")
            return render_template('auth/login.html')
        try:
            # query the UserAccount table to find username match
            user = UserAccount.query.filter_by(username=username).first()
            if user is None or not check_password_hash(user.password, password):
                flash("Nombre de usuario o contraseña incorrectos.", "danger")
                log.log_warning("Intento de inicio de sesión fallido por credenciales incorrectas. 401 Unauthorized.")
                return render_template('auth/login.html', errors=["Nombre de usuario o contraseña incorrectos."])
            session.clear() # Prevent session fixation
            session['user_id'] = user.id_user
            session['username'] = user.username
            session['role'] = user.role
            # ------------- Redirect to dashboard --------------- #
            flash("Inicio de sesión exitoso.", "success")
            log.log_info(f"Usuario {username} inició sesión exitosamente. 200 OK.")
            return redirect(url_for('views_client.dashboard')) # 200 OK
        except Exception as e:
            flash("Nombre de usuario o contraseña incorrectos.", "danger") #500 Internal Server Error
            log.log_error(f"Error durante el inicio de sesión: {e}. 500 Internal Server Error.")
            return render_template('auth/login.html')
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Has cerrado sesión exitosamente.", "success")
    log.log_info("Usuario cerró sesión exitosamente. 200 OK.")
    return redirect(url_for('views.index')) # 200 OK