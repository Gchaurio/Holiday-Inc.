from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from login.auth import login_required
from login.auth import root_required
from login.db import get_db
from login.auth import manager_required
from .functions import logger_register
from login.auth import analist_required
import re

bp = Blueprint('start', __name__)
@bp.route('/start/admin/approve', methods=('POST', 'GET'))
@login_required
@root_required
def index():
    db = get_db()

    if request.method == 'POST':
        if 'approve' in request.form:
            # action of aprove button
            id = request.form['approve']
            db.execute(
                'UPDATE user SET verified = 1 WHERE id = ?',
                (id,)
            )
            db.commit()
            logger_register(f'User with id "{id}", approved.', g.user['username'])
        elif 'reject' in request.form:
            # action of reject button
            id = request.form['reject']
            db.execute(
                'DELETE FROM user WHERE id = ?',
                (id,)
            )
            db.commit()
            logger_register(f'User with id "{id}", rejected.', g.user['username'])
        elif 'assign_project' in request.form:
            project_description = request.form['project']
            user_id = request.form['assign_project']
            project = db.execute(
                'SELECT id FROM project WHERE description = ?',
                (project_description,)
            ).fetchone()
            if project is not None:
                db.execute(
                    'UPDATE user SET project = ? WHERE id = ?',
                    (project['id'], user_id)
                )
                db.commit()
                logger_register(f'Project "{project_description}", assigned to user id: {user_id}.', g.user['username'])
            
    db = get_db()
    users = db.execute(
        'SELECT * FROM user'
    ).fetchall()
    projects = db.execute(
        'SELECT * FROM project'
    ).fetchall()
    

    return render_template('/start/admin/approve.html', users=users, projects=projects)

@bp.route('/start/user/index.html', methods=('POST', 'GET'))
@login_required
def user_view():
    if (g.user['role'] == 'admin') or (g.user['role'] == 'Gerente de Operaciones'):
       return redirect(url_for('auth.login'))
    else:
        return render_template('/start/user/index.html')

@bp.route('/start/admin/create_project', methods=('POST', 'GET'))
@login_required
@root_required
def create_project():

    db = get_db()
    error = None

    if request.method == 'POST':
        if 'description' in request.form:
            description = request.form['description']
            init_date = request.form['init']
            end_date = request.form['end']

            if init_date > end_date:
                error = f"Init date cant be after End date."
                flash(error)
                db = get_db()
                projects = db.execute(
                    'SELECT * FROM project'
                ).fetchall()
                return render_template('/start/admin/create_project.html', projects=projects)


            try:
                db.execute(
                    "INSERT INTO project (description, init, end, status) VALUES (?, ?, ?, ?)", 
                    (description, init_date, end_date, 0),
                )
                db.commit()
                logger_register(f'Project "{description}", created.', g.user['username'])
            except db.IntegrityError:
                error = f"Project {description} is already created."
                flash(error)

        elif 'activate' in request.form:
            id = request.form['activate']
            db.execute(
                'UPDATE project SET status = 1 WHERE id = ?',
                (id,)
            )
            db.commit()
            logger_register(f'Project with id "{id}", activated.', g.user['username'])
        elif 'deactivate' in request.form:
            id = request.form['deactivate']
            db.execute(
                'UPDATE project SET status = 0 WHERE id = ?',
                (id,)
            )
            db.commit()
            logger_register(f'Project with id "{id}", deactivated.', g.user['username'])
        elif 'delete' in request.form:
            id = request.form['delete']
            db.execute(
                'DELETE FROM project WHERE id = ?',
                (id,)
            )
            db.execute(
                'UPDATE user SET project = -2 WHERE project = ?',
                (id,)
            )
            db.execute(
                'DELETE FROM project_info WHERE project_id = ?',
                (id,)
            )
            db.commit()
            logger_register(f'Project with id "{id}", deleted.', g.user['username'])
            logger_register(f'All users related to project with id "{id}", has been asigned with no projects.', g.user['username'])
            logger_register(f'All sub-projects related to project with id "{id}", has been deleted.', g.user['username'])

    db = get_db()
    projects = db.execute(
        'SELECT * FROM project'
    ).fetchall()
    return render_template('/start/admin/create_project.html', projects=projects)

@bp.route('/start/admin/create_departments.html', methods=('POST', 'GET'))
@login_required
@root_required
def create_department():

    db = get_db()
    error = None

    if request.method == 'POST':
        if 'department' in request.form:
            name = request.form['department']
            try:
                db.execute(
                    "INSERT INTO department (name) VALUES (?)", 
                    (name,)
                )
                db.commit()
                logger_register(f'Department "{name}", created.', g.user['username'])
            except db.IntegrityError:
                error = f"Department {name} is already created."
                flash(error)

        elif 'delete' in request.form:
            id = request.form['delete']
            db.execute(
                'DELETE FROM department WHERE id = ?',
                (id,)
            )
            '''db.execute(
                'UPDATE user SET project = -2 WHERE project = ?',
                (id,)
            )'''
            db.commit()
            logger_register(f'Department with id "{id}", deleted.', g.user['username'])
            #logger_register(f'All users related to project with id "{id}", has been asigned with no projects.', g.user['username'])

    db = get_db()
    departments = db.execute(
        'SELECT * FROM department'
    ).fetchall()
    return render_template('/start/admin/create_departments.html', departments=departments)

@bp.route('/start/admin/modify_departments.html', methods=('POST', 'GET'))
@login_required
@root_required
def modify_departments():

    db = get_db()
    error = None
    dep_id = request.args.get('id')
    if dep_id is None:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        if 'description' in request.form:
            name = request.form['description']
            try:
                db.execute(
                    'UPDATE department SET name = ? WHERE id = ?',
                    (name, dep_id),
                )
                db.commit()
                logger_register(f"Department name with id {dep_id} updated in database.", g.user['username'])
                db = get_db()
                if g.user['role'] == 'admin':
                    return redirect(url_for('start.create_department'))
            except db.IntegrityError:
                error = f"Department with id {dep_id} could not be updated in database."
                flash(error)
    
    department = db.execute(
        'SELECT * FROM department WHERE id = ?', (dep_id,)
    ).fetchall()
    return render_template('/start/admin/modify_departments.html', department=department)


@bp.route('/start/manager/modify_project.html', methods=('POST', 'GET'))
@login_required
@manager_required
def modify_project():

    db = get_db()
    error = None
    project_id = request.args.get('id')
    father_proj_id = request.args.get('project_id')

    if project_id is None:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        if 'modify_project_detail' in request.form:
            car_id = request.form['car']
            department = request.form['department']
            manager = request.form['manager']
            problem = request.form['problem']
            solution = request.form['solution']
            amount = request.form['amount']
            obs = request.form['obs']
            try:
                db.execute(
                    'UPDATE project_info SET car_id = ?, department = ?, manager = ?, problem = ?, solution = ?, ammount = ?, obs = ? WHERE id = ?',
                    (car_id, department, manager, problem, solution, amount, obs,project_id)
                )
                db.commit()
                logger_register(f"Project Details with id {project_id} updated in database.", g.user['username'])
                db = get_db()
                return redirect(url_for('start.project_details',id= father_proj_id,project_id=father_proj_id))
            except db.IntegrityError:
                error = f"Project Details with id {project_id} could not be updated in database."
                flash(error)

    cars = db.execute(
        'SELECT * FROM car'
    ).fetchall()
    
    departments = db.execute(
        'SELECT * FROM department'
    ).fetchall()
    

    managers = db.execute(
        "SELECT * FROM user WHERE role != 'admin' and project = ?", (father_proj_id,)
    ) .fetchall()

    project_info = db.execute(
        'SELECT * FROM project_info WHERE id = ?', (project_id,)
    ).fetchall()
    
    return render_template('/start/manager/modify_project.html',  project_id=project_id, cars=cars, project_info=project_info, departments=departments, managers=managers )

@bp.route('/start/manager/project_details.html', methods=('POST', 'GET'))
@login_required
@manager_required
def project_details():

    db = get_db()
    error = None
    project_id = request.args.get('id')
    if project_id is None:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        if 'add_project' in request.form:
            car_id = request.form['car']
            department = request.form['department']
            manager = request.form['manager']
            problem = request.form['problem']
            solution = request.form['solution']
            amount = request.form['amount']
            obs = request.form['obs']
            try:
                db.execute(
                    'INSERT INTO project_info (project_id, car_id, department, manager, problem, solution, ammount, obs) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (project_id, car_id, department, manager, problem, solution, amount, obs)
                )
                db.commit()
                logger_register(f"Project part for the car with plaque {car_id} added to database.", g.user['username'])
                return redirect(url_for('start.project_details',id = project_id,project_id=project_id))
            except db.IntegrityError:
                error = f"Project part for the car with plaque {car_id} could not be added to database."
                flash(error)
        elif 'delete' in request.form:
            project_info_id = request.form['delete']
            db.execute(
                'DELETE FROM project_info WHERE id = ?',
                (project_info_id,)
            )
            db.commit()
            logger_register(f'Project with id "{project_info_id}", deleted.', g.user['username'])
        else:
            error = "Invalid action"
            flash(error)

    cars = db.execute(
        'SELECT * FROM car'
    ).fetchall()
    
    departments = db.execute(
        'SELECT * FROM department'
    ).fetchall()
    
    project = db.execute(
        'SELECT * FROM project WHERE id = ?', (project_id,)
    ).fetchall()

    managers = db.execute(
        "SELECT * FROM user WHERE role != 'admin' and project = ?", (project_id,)
    ) .fetchall()

    project_info = db.execute(
        'SELECT * FROM project_info WHERE project_id = ?', (project_id,)
    ).fetchall()
    return render_template('/start/manager/project_details.html', project=project, project_id=project_id, cars=cars, project_info=project_info, departments=departments, managers=managers )

@bp.route('/start/manager/modify_father_project.html', methods=('POST', 'GET'))
@login_required
@manager_required
def modify_father_project():

    db = get_db()
    error = None
    project_id = request.args.get('id')
    if project_id is None:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        if 'description' in request.form:
            description = request.form['description']
            init_date = request.form['init']
            end_date = request.form['end']
            try:
                db.execute(
                    'UPDATE project SET description = ?, init = ?, end = ? WHERE id = ?',
                    (description, init_date, end_date, project_id)
                )
                db.commit()
                logger_register(f"Project with id {project_id} updated in database.", g.user['username'])
                db = get_db()
                if g.user['role'] == 'admin':
                    return redirect(url_for('start.create_project'))
                else:
                    return redirect(url_for('start.manager_project'))
            except db.IntegrityError:
                error = f"Project with id {project_id} could not be updated in database."
                flash(error)
    
    project = db.execute(
        'SELECT * FROM project WHERE id = ?', (project_id,)
    ).fetchall()
    return render_template('/start/manager/modify_father_project.html', project=project)

@bp.route('/start/manager/manager_project.html', methods=('POST', 'GET'))
@login_required
@manager_required
def manager_project():

    if (g.user['role'] != 'Gerente de Operaciones'):
       return redirect(url_for('auth.login'))
    
    db = get_db()
    error = None

    if request.method == 'POST':
        if 'description' in request.form:
            description = request.form['description']
            init_date = request.form['init']
            end_date = request.form['end']

            if init_date > end_date:
                error = f"Init date cant be after End date."
                flash(error)
                db = get_db()
                projects = db.execute(
                    'SELECT * FROM project'
                ).fetchall()
                return render_template('/start/manager/manager_project.html', projects=projects)


            try:
                db.execute(
                    "INSERT INTO project (description, init, end, status) VALUES (?, ?, ?, ?)", 
                    (description, init_date, end_date, 0),
                )
                db.commit()
                logger_register(f'Project "{description}", created.', g.user['username'])
            except db.IntegrityError:
                error = f"Project {description} is already created."
                flash(error)

        elif 'activate' in request.form:
            id = request.form['activate']
            db.execute(
                'UPDATE project SET status = 1 WHERE id = ?',
                (id,)
            )
            db.commit()
            logger_register(f'Project with id "{id}", activated.', g.user['username'])
        elif 'deactivate' in request.form:
            id = request.form['deactivate']
            db.execute(
                'UPDATE project SET status = 0 WHERE id = ?',
                (id,)
            )
            db.commit()
            logger_register(f'Project with id "{id}", deactivated.', g.user['username'])
        elif 'delete' in request.form:
            id = request.form['delete']
            db.execute(
                'DELETE FROM project WHERE id = ?',
                (id,)
            )
            db.execute(
                'UPDATE user SET project = -2 WHERE project = ?',
                (id,)
            )
            db.commit()
            logger_register(f'Project with id "{id}", deleted.', g.user['username'])
            logger_register(f'All users related to project with id "{id}", has been asigned with no projects.', g.user['username'])

    db = get_db()
    projects = db.execute(
        'SELECT * FROM project'
    ).fetchall()
    return render_template('/start/manager/manager_project.html', projects=projects)


@bp.route('/start/admin/create_user', methods=('POST', 'GET'))
@login_required
@root_required
def create_user():

    db = get_db()
    error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        role = request.form['role']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        if not firstname:
            error = 'First name is required.'
        elif not lastname:
            error = 'Last name is required.'
        elif not role:
            error = 'Role is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, firstname, lastname, project, role, verified) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (username, generate_password_hash(password), firstname, lastname, -2, role, 1),
                )
                db.commit()
                logger_register(f'User with username "{username}", created.', g.user['username'])
            except db.IntegrityError:
                error = f"User {username} is already registered."
                flash(error)

    db = get_db()
    users = db.execute(
        'SELECT * FROM user'
    ).fetchall()
    projects = db.execute(
        'SELECT * FROM project'
    ).fetchall()
    

    return render_template('/start/admin/create_user.html', users=users, projects=projects)

@bp.route('/start/admin/modify_users.html', methods=('POST', 'GET'))
@login_required
@root_required
def modify_user():
    db = get_db()
    error = None
    
    if request.method == 'POST':
        if 'change' in request.form:
            user_id = request.form['change']
            new_role = request.form[f'role_{user_id}']
            new_project = request.form[f'project_{user_id}']
            
            db.execute(
                'UPDATE user SET role = ?, project = ? WHERE id = ?',
                (new_role, new_project, user_id)
            )
            db.commit()
            logger_register(f'User with id "{user_id}" has now role "{new_role}" and is assigned to project "new_project".', g.user['username'])
        elif 'delete' in request.form:
            id = request.form['delete']
            db.execute(
                'DELETE FROM user WHERE id = ?',
                (id,)
            )
            db.commit()
            logger_register(f'User with id "{id}"has been deleted.', g.user['username'])

    db = get_db()
    users = db.execute(
        'SELECT * FROM user'
    ).fetchall()
    projects = db.execute(
        'SELECT * FROM project'
    ).fetchall()

    # Only show one user at a time
    if request.args.get('id'):
        user_id = request.args.get('id')
        user = db.execute(
            'SELECT * FROM user WHERE id = ?',
            (user_id,)
        ).fetchone()
        if user:
            return render_template('/start/admin/modify_user.html', user=user, projects=projects)
        else:
            flash('User not found.', 'error')
    
    return render_template('/start/admin/modify_users.html', users=users, projects=projects)


@bp.route('/start/admin/logger.html', methods=('POST', 'GET'))
@login_required
@root_required
def logger_index():
    db = get_db()
    logger = db.execute(
        'SELECT * FROM logger'
    ).fetchall()

    return render_template('/start/admin/logger.html', logger = logger)

@bp.route('/start/analist/client_register.html', methods=('POST', 'GET'))
@login_required
@analist_required
def client_list():
    db = get_db()
    if 'dni' in request.form:
        err = 0
        dni = request.form['dni']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        birthdate = request.form['birthdate']
        phone = request.form['phone'].replace(' ','')
        email = request.form['email']
        address = request.form['address']

        if re.match(r"^(V|J|E)-\d+$", dni):
            pass
        else:
            error = f"DNI not valid, must start with V-, E- or J-, followed up by the corresponding numbers."
            flash(error)
            err = 1
        if re.match(r'^[\d()+-]+$', phone):
            pass
        else:
            error = f"Phone number not valid."
            flash(error)
            err = 1
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            pass
        else:
            error = f"Email not valid."
            flash(error)
            err = 1

        if err == 0:
            try:
                db.execute(
                    "INSERT INTO client (dni, firstname, lastname, birthdate, phone, email, address) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                    (dni, firstname, lastname, birthdate, phone, email, address),
                )
                db.commit()
                logger_register(f'Client "{firstname}'+' '+'{lastname}", created.', g.user['username'])
            except db.IntegrityError:
                error = f"Client with dni {dni} is already created."
                flash(error)

            db = get_db()
            clients = db.execute(
                'SELECT * FROM client'
            ).fetchall()

            return render_template('/start/analist/client_register.html', clients=clients)
        
    elif 'delete' in request.form:
        client_id = request.form['delete']
        # Retrieve the DNI of the client that has been deleted
        client = db.execute(
            'SELECT dni FROM client WHERE id = ?',
            (client_id,)
        ).fetchone()
        if client:
            dni = client['dni']
            # Delete all cars belonging to this client
            try:
                db.execute(
                    'DELETE FROM car WHERE owner = ?',
                    (dni,)
                )
                db.execute(
                    'DELETE FROM client WHERE id = ?',
                    (client_id,)
                )
                db.commit()
                logger_register(f'Client with id "{client_id}" and all its cars have been deleted.', g.user['username'])
            except db.IntegrityError:
                error = f"There was an error deleting the user and its car from database."
                flash(error)
        else:
            error = f"Client with id {client} does not exist."
            flash(error)


    db = get_db()
    clients = db.execute(
        'SELECT * FROM client'
    ).fetchall()

    return render_template('/start/analist/client_register.html', clients=clients)

@bp.route('/start/analist/car_register.html', methods=('POST', 'GET'))
@login_required
@analist_required
def car_list():
    db = get_db()
    owner = request.args.get('dni')
    if owner is None:
        return redirect(url_for("auth.login"))
    if request.method == 'POST':
        if 'plaque' in request.form:
            plaque = request.form['plaque']
            brand = request.form['brand']
            model = request.form['model']
            year = request.form['year']
            serial_car = request.form['serial_car']
            serial_mot = request.form['serial_mot']
            color = request.form['color']
            issue = request.form['issue']
            owner = request.args.get('dni')
            try:
                db.execute(
                    'INSERT INTO car (plaque, brand, model, year, serial_car, serial_mot, color, issue, owner) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (plaque, brand, model, year, serial_car, serial_mot, color, issue, owner)
                )
                db.commit()
                logger_register(f'Car with plaque "{plaque}" was registered to owner "{owner}".', g.user['username'])
            except db.IntegrityError:
                error = f"Car with plaque {plaque} is already registered, check plaque and serials."
                flash(error)

        elif 'delete' in request.form:
            id = request.form['delete']
            try:
                db.execute(
                    'DELETE FROM car WHERE id = ?',
                    (id,)
                )
                db.commit()
                logger_register(f"Car with id {id} was delete from registry.", g.user['username'])
            except:
                error = f"Car with id {id} is not in car database."
                flash(error)
        

    db = get_db()
    client = db.execute(
        'SELECT * FROM client WHERE dni = ?', (owner,)
    ).fetchall()
    cars = db.execute(
        'SELECT * FROM car WHERE owner = ?', (owner,)
    ).fetchall()

    return render_template('/start/analist/car_register.html', client=client, cars=cars)

@bp.route('/start/analist/car_modify.html', methods=('POST', 'GET'))
@login_required
@analist_required
def car_modify():
    db = get_db()
    car_id = request.args.get('car_id')
    owner = request.args.get('owner')
    if (car_id is None) or (owner is None):
        return redirect(url_for("auth.login"))
    if request.method == 'POST':
        if 'suelte' in request.form:
            plaque = request.form['plaque']
            brand = request.form['brand']
            model = request.form['model']
            year = request.form['year']
            serial_car = request.form['serial_car']
            serial_mot = request.form['serial_mot']
            color = request.form['color']
            issue = request.form['issue']
            try:
                db.execute(
                    'UPDATE car SET plaque = ?, brand = ?, model = ?, year = ?, serial_car = ?, serial_mot = ?, color = ?, issue = ?, owner = ? WHERE id = ?',
                    (plaque, brand, model, year, serial_car, serial_mot, color, issue, owner, car_id)
                )
                db.commit()
                logger_register(f"Car with plaque {plaque} updated in database.", g.user['username'])
                db = get_db()
                return redirect(url_for('start.car_list', dni=owner))
            except db.IntegrityError:
                error = f"Car with plaque {plaque} could not be updated in database."
                flash(error)

    db = get_db()
    client = db.execute(
        'SELECT * FROM client WHERE dni = ?', (owner,)
    ).fetchall()
    car = db.execute(
        'SELECT * FROM car WHERE id = ?', (car_id,)
    ).fetchall()

    return render_template('/start/analist/car_modify.html', client=client, car=car)

@bp.route('/start/admin/create_metrics.html', methods=('POST', 'GET'))
@login_required
@root_required
def create_metrics():

    db = get_db()
    error = None

    if request.method == 'POST':
        if 'unit' in request.form:
            dimentions = request.form['dimentions']
            units = request.form['unit']
            try:
                db.execute(
                    "INSERT INTO metrics (dimentions,units) VALUES (?,?)", 
                    (dimentions,units,)
                )
                db.commit()
                logger_register(f'Metrics "{dimentions + units}", created.', g.user['username'])
            except db.IntegrityError:
                error = f"Unexpected error."
                flash(error)

        elif 'delete' in request.form:
            id = request.form['delete']
            db.execute(
                'DELETE FROM metrics WHERE id = ?',
                (id,)
            )
            db.commit()
            logger_register(f'Metrics with id "{id}", deleted.', g.user['username'])
            #logger_register(f'All users related to project with id "{id}", has been asigned with no projects.', g.user['username'])

    db = get_db()
    metrics = db.execute(
        'SELECT * FROM metrics'
    ).fetchall()
    return render_template('/start/admin/create_metrics.html', metrics=metrics)

@bp.route('/start/admin/modify_metrics.html', methods=('POST', 'GET'))
@login_required
@root_required
def modify_metrics():

    db = get_db()
    error = None
    id = request.args.get('id')
    if id is None:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        if 'unit' in request.form:
            dimentions = request.form['dimentions']
            units = request.form['unit']
            try:
                db.execute('UPDATE metrics SET dimentions = ?, units = ? WHERE id = ?', (dimentions, units, id))
                db.commit()
                logger_register(f"Metrics with id {id} updated in database.", g.user['username'])
                db = get_db()
                if g.user['role'] == 'admin':
                    return redirect(url_for('start.create_metrics'))
            except db.IntegrityError:
                error = f"Metrics with id {id} could not be updated in database."
                flash(error)
    
    metric = db.execute(
        'SELECT * FROM metrics WHERE id = ?', (id,)
    ).fetchall()
    return render_template('/start/admin/modify_metrics.html', metric=metric)

@bp.route('/start/manager/action_plan.html', methods=('POST', 'GET'))
@login_required
@manager_required
def action_plan():

    db = get_db()
    error = None
    project_detail_id = request.args.get('project_detail_id')
    project_id = request.args.get('project_id')
    if project_id is None or project_detail_id is None:
        return redirect(url_for('auth.login'))

    if request.method == 'POST' and 'add_action_plan' in request.form:
        action = request.form['action']
        activity = request.form['activity']
        init = request.form['init']
        end = request.form['end']
        category = request.form['category']
        material = request.form['material']
        material_quantity = request.form['material_quantity']
        metric = request.form['metric']
        material_cost = request.form['material_cost']
        responsable = request.form['responsable']
        human_quantity = request.form['human_quantity']
        hours_quantity = request.form['hours_quantity']
        payment_per_hour = request.form['human_amount']
        human_amount = (int(hours_quantity))*int(payment_per_hour)*int(human_quantity)
        material_amount = int(metric)*int(material_cost)*int(material_quantity)

        try:
            db.execute(
                'INSERT INTO action_plan (project_info_id, action, activity, init, end, category, material, metric, human_quantity, hours_quantity, material_quantity, responsable, human_ammount, material_ammount) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (project_detail_id, action, activity, init, end, category, material, metric, human_quantity, hours_quantity, material_quantity, responsable, human_amount, material_amount)
            )
            db.commit()
            flash('Action Plan added successfully.', 'success')
        except:
            error = 'An error occurred while adding the action plan.'
            flash(error)
    elif 'delete' in request.form:
        action_plan_id = request.form['delete']
        db.execute(
            'DELETE FROM action_plan WHERE id = ?',
            (action_plan_id,)
        )
        db.commit()
        logger_register(f'Action Plan with id "{action_plan_id}", deleted.', g.user['username'])

    
    project = db.execute(
        'SELECT * FROM project WHERE id = ?', (project_id,)
    ).fetchall()

    managers = db.execute(
        "SELECT * FROM user WHERE role != 'admin' and project = ?", (project_id,)
    ) .fetchall()

    project_info = db.execute(
        'SELECT * FROM project_info WHERE project_id = ?', (project_detail_id,)
    ).fetchall()

    action_plans = db.execute(
        'SELECT * FROM action_plan WHERE project_info_id = ?', (project_detail_id,)
    ).fetchall()

    metrics = db.execute(
        'SELECT * FROM metrics'
    ).fetchall()

    total_human = 0
    total_material = 0
    for action_plan in action_plans:
        total_human += action_plan[13]
        total_material += action_plan[14]
    total = total_human + total_material

    return render_template('/start/manager/action_plan.html', project=project, project_id=project_id, project_info=project_info, managers=managers, action_plans = action_plans, metrics=metrics, total_amount=total, total_amount_material = total_material, total_amount_human = total_human )

@bp.route('/start/manager/action_plan_modify_general.html', methods=('POST', 'GET'))
@login_required
@manager_required
def action_plan_modify_general():
    db = get_db()
    action_plan_id = request.args.get('id')
    action_plan_project_detail_id = request.args.get('action_project_id')
    project_id = request.args.get('project_id')
    if (action_plan_id is None) or (action_plan_project_detail_id is None) or (project_id is None):
        return redirect(url_for("auth.login"))

    if request.method == 'POST':
        if 'update_general' in request.form:
            action = request.form['action']
            activity = request.form['activity']
            init = request.form['init']
            end = request.form['end']
            category = request.form['category']
            material = request.form['material']
            material_quantity = request.form['material_quantity']
            metric = request.form['metric']
            material_cost = request.form['material_cost']
            responsable = request.form['responsable']
            human_quantity = request.form['human_quantity']
            hours_quantity = request.form['hours_quantity']
            payment_per_hour = request.form['human_amount']
            human_amount = (int(hours_quantity))*int(payment_per_hour)*int(human_quantity)
            material_amount = int(metric)*int(material_cost)*int(material_quantity)

            try:
                db.execute(
                    'UPDATE action_plan SET action = ?, activity = ?, init = ?, end = ?, category = ?, material = ?, material_quantity = ?, metric = ?, material_ammount = ?, responsable = ?, human_quantity = ?, hours_quantity = ?, human_ammount = ? WHERE id = ?',
                    (action, activity, init, end, category, material, material_quantity, metric, material_amount, responsable, human_quantity, hours_quantity, human_amount, action_plan_id))
                db.commit()
                logger_register(f"Action plan with id {action_plan_id} updated in database.", g.user['username'])
                flash("Action Plan updated successfully!", "success")
                return redirect(url_for("start.action_plan", project_id=project_id, project_detail_id=action_plan_project_detail_id))

            except Exception as e:
                db.rollback()
                logger_register(f"Error updating action plan with id {action_plan_id} in database: {e}", g.user['username'])
                flash("An error occurred while updating the Action Plan.", "danger")

    action_plan = db.execute(
        'SELECT * FROM action_plan WHERE id = ?',
        (action_plan_id,)
    ).fetchone()

    metrics = db.execute(
        'SELECT * FROM metrics'
    ).fetchall()

    managers = db.execute(
    "SELECT * FROM user WHERE role != 'admin' and project = ?", (project_id,)
    ).fetchall()

    return render_template("/start/manager/action_plan_modify_general.html", action_plan=action_plan, metrics=metrics, managers=managers)

@bp.route('/start/manager/action_plan_modify_human.html', methods=('POST', 'GET'))
@login_required
@manager_required
def action_plan_modify_human():
    db = get_db()
    action_plan_id = request.args.get('id')
    action_plan_project_detail_id = request.args.get('action_project_id')
    project_id = request.args.get('project_id')
    if (action_plan_id is None) or (action_plan_project_detail_id is None) or (project_id is None):
        return redirect(url_for("auth.login"))

    if request.method == 'POST':
        if 'update_human' in request.form:
            action = request.form['action']
            activity = request.form['activity']
            responsable = request.form['responsable']
            human_quantity = request.form['human_quantity']
            hours_quantity = request.form['hours_quantity']
            payment_per_hour = request.form['human_amount']
            human_amount = (int(hours_quantity))*int(payment_per_hour)*int(human_quantity)

            try:
                db.execute(
                    'UPDATE action_plan SET action = ?, activity = ?, responsable = ?, human_quantity = ?, hours_quantity = ?, human_ammount = ? WHERE id = ?',
                    (action, activity, responsable, human_quantity, hours_quantity, human_amount, action_plan_id))
                db.commit()
                logger_register(f"Action plan (Human Talent) with id {action_plan_id} updated in database.", g.user['username'])
                flash("Action Plan updated successfully!", "success")
                return redirect(url_for("start.action_plan", project_id=project_id, project_detail_id=action_plan_project_detail_id))

            except Exception as e:
                db.rollback()
                logger_register(f"Error updating action plan with id {action_plan_id} in database: {e}", g.user['username'])
                flash("An error occurred while updating the Action Plan.", "danger")

    action_plan = db.execute(
        'SELECT * FROM action_plan WHERE id = ?',
        (action_plan_id,)
    ).fetchone()

    metrics = db.execute(
        'SELECT * FROM metrics'
    ).fetchall()

    managers = db.execute(
    "SELECT * FROM user WHERE role != 'admin' and project = ?", (project_id,)
    ).fetchall()

    return render_template("/start/manager/action_plan_modify_human.html", action_plan=action_plan, metrics=metrics, managers=managers)

@bp.route('/start/manager/action_plan_modify_material.html', methods=('POST', 'GET'))
@login_required
@manager_required
def action_plan_modify_material():
    db = get_db()
    action_plan_id = request.args.get('id')
    action_plan_project_detail_id = request.args.get('action_project_id')
    project_id = request.args.get('project_id')
    if (action_plan_id is None) or (action_plan_project_detail_id is None) or (project_id is None):
        return redirect(url_for("auth.login"))

    if request.method == 'POST':
        if 'update_material' in request.form:
            action = request.form['action']
            activity = request.form['activity']
            category = request.form['category']
            material = request.form['material']
            material_quantity = request.form['material_quantity']
            metric = request.form['metric']
            material_cost = request.form['material_cost']
            responsable = request.form['responsable']
            material_amount = int(metric)*int(material_cost)*int(material_quantity)

            try:
                db.execute(
                    'UPDATE action_plan SET action = ?, activity = ?, category = ?, material = ?, material_quantity = ?, metric = ?, material_ammount = ?, responsable = ? WHERE id = ?',
                    (action, activity, category, material, material_quantity, metric, material_amount, responsable, action_plan_id))
                db.commit()
                logger_register(f"Action plan with id {action_plan_id} updated in database.", g.user['username'])
                flash("Action Plan (Material) updated successfully!", "success")
                return redirect(url_for("start.action_plan", project_id=project_id, project_detail_id=action_plan_project_detail_id))

            except Exception as e:
                db.rollback()
                logger_register(f"Error updating action plan with id {action_plan_id} in database: {e}", g.user['username'])
                flash("An error occurred while updating the Action Plan.", "danger")

    action_plan = db.execute(
        'SELECT * FROM action_plan WHERE id = ?',
        (action_plan_id,)
    ).fetchone()

    metrics = db.execute(
        'SELECT * FROM metrics'
    ).fetchall()

    managers = db.execute(
    "SELECT * FROM user WHERE role != 'admin' and project = ?", (project_id,)
    ).fetchall()

    return render_template("/start/manager/action_plan_modify_material.html", action_plan=action_plan, metrics=metrics, managers=managers)
