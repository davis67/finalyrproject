from flask import request, flash, abort, url_for, redirect, render_template, jsonify
from flask_login import current_user, login_required
from .forms import LoginForm, AddPoliceStationForm, RegistrationForm
from ..model import Police, User, Category, CrimeScene
from .. import db
from . import home
from ..PlotData import (showmap)
from datetime import datetime as dt


@home.route('/', methods=['GET', 'POST'])
def homepage():
    """
    Render the home page on / route
    """
    form = LoginForm()

    # policestations = Police.query.all()
    return render_template('home/index.html', title="welcome",
                           form=form, methods=['GET', 'POST'])

# add admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    # if not current_user.is_admin:
    #     abort(403)
    uncategorized = showmap()
    return render_template('home/admin_dashboard.html', title="dashboard", uncategorized=uncategorized)


@home.route('/admin/policestation', methods=['POST', 'GET'])
@login_required
def police_station_data():
    if not current_user.is_admin:
        abort(403)
    form = AddPoliceStationForm()
    if form.validate_on_submit():
        police_station = Police(StationName=form.StationName.data,
                                division=form.division.data)
        db.session.add(police_station)
        db.session.commit()
        flash("You have successfully added a Police Station.")
    police_stations = Police.query.all()
    return render_template('home/police_index.html',
                           title="PoliceStation",
                           police_stations=police_stations,
                           form=form)


@home.route('/admin/policestation/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_police(id):
    if not current_user.is_admin:
        abort(403)
    add_police = False
    police = Police.query.get_or_404(id)
    form = AddPoliceStationForm(obj=police)
    if form.validate_on_submit():
        police.StationName = form.StationName.data
        division = form.division.data
        db.session.commit()
        flash('You have successfully edited a police station')
        return redirect(url_for('home.police_station_data'))
    police_stations = Police.query.all()
    return render_template('home/police_index.html',
                           title="PoliceStation",
                           police_stations=police_stations,
                           form=form)


@home.route('/admin/policestation/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_police(id):
    if not current_user.is_admin:
        abort(403)
    police = Police.query.get_or_404(id)
    db.session.delete(police)
    db.session.commit()
    flash('You have successfully deleted the Police Station.')
    return redirect(url_for('home.police_station_data'))


@home.route('/admin/register_user', methods=['GET', 'POST'])
@login_required
def register_user():
    if not current_user.is_admin:
        abort(403)
    """
    Handle requests for to the database through the registration form

    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            full_names=form.full_names.data,
            telephone=form.telephone.data,
            password=form.password.data
        )
        # add employee to the database
        db.session.add(user)
        db.session.commit()
        flash('You have successively registered! You may now login.')

    # redirect to the login page
    return render_template('home/register.html', title="Register User",
                           form=form)


@home.route('/web/PathFinder/v1.0/data/to-day')
@login_required
def collect_data():
    # datemask = '%m/%d/%Y'
    # today = datetime.datetime.strftime(datetime.datetime.today(),datemask)
    # today_cases = CaseFile.query.filter_by(date_posted = today)
    year = dt.strftime(dt.today(), '%Y')
    labels, actual_data, category_colors = category_crimes_data_of_year(year)
    crimesdata = {
        'labels': labels,
        'data': actual_data,
        'year': year,
        'category_colors': category_colors
    }
    print('request made.............\n ')
    return jsonify({'crimesdata': crimesdata})


@home.route('/web/PathFinder/v1.0/data/')
@login_required
def collect_summary_data():
    casesData = {
        'thefty': len(Category.query.filter_by(violet_type='Thefty').first().crimescene),
        'murder': len(Category.query.filter_by(violet_type='murder').first().crimescene),
        'kidnap': len(Category.query.filter_by(violet_type='kidnap').first().crimescene),
        'robbery': len(Category.query.filter_by(violet_type='robbery').first().crimescene)
    }
    return jsonify({'casesData': casesData})

    """
    returns the taple of categories list the count of crimes count
    list
    """


def category_crimes_data_of_year(year):
    crime_categories = []
    crime_categories_count = []
    cat_colors = []
    for category in Category.query.all():
        crime_categories.append(category.violet_type)
        cat_colors.append(category.category_color)
        #
        count = 0
        for crimescene in category.crimescene.all():
            """
            get crimes of the current year
            """
            crimescene_year = dt.strftime(crimescene.date_posted, '%Y')
            if crimescene_year == year:
                count = count + 1
        crime_categories_count.append(count)
    return crime_categories, crime_categories_count, cat_colors


@home.route('/admin/dashboard/crimes/comp_vis/', methods=['GET', 'POST'])
@login_required
def crime_comparision_view():
    if not current_user.is_admin:
        abort(403)
    return render_template('home/compare_categories.html', title="Compare Crime Categories")


@home.route('/categories/data/line', methods=['GET'])
@login_required
def get_categories_data():
    date_mask = '%Y'
    labels = []
    category_datasets = []
    plot_dataset = []
    for category in Category.query.all():
        dataset = {'data': {}, 'label': '', 'borderColor': ''}
        dataset['label'] = category.violet_type
        dataset['borderColor'] = category.category_color
        category_crimes = category.crimescene
        """
        find the crimes count of this category in each year
        """
        # map crimes count to years
        years_data = {}
        for category_crime in category_crimes:
            year_of_analysis = dt.strftime(
                category_crime.date_posted, date_mask)
            years_data[year_of_analysis] = years_data[year_of_analysis] + \
                1 if year_of_analysis in years_data.keys() else 1
        dataset['data'] = years_data
        category_datasets.append(dataset)

    # create labels
    for dataset in category_datasets:
        for year in dataset['data'].keys():
            if year not in labels:
                labels.append(year)

    # sort labels(ascending order)
    labels.sort()

    # build the plot dataset
    for dataset in category_datasets:
        label = dataset['label']
        borderColor = dataset['borderColor']
        data = []
        for year in labels:
            try:
                count = dataset['data'][year]
            except KeyError:
                count = 0
            finally:
                data.append(count)
        plot_dataset.append({'data': data,
                             'label': label,
                             'borderColor': borderColor
                             }
                            )
    return jsonify({'data': plot_dataset, 'labels': labels})


@home.route('/admin/dashboard/crime/analysis/', methods=['POST'])
@login_required
def analyze_crimes():
    if not current_user.is_admin:
        abort(403)
    """
    create map showing crime category scenes in a period
    """
    category_post = request.form['category']
    from_period = request.form['from_date']
    to_period = request.form['to_date'] if request.form['to_date'] is not None else dt.today(
    )
    print(request.form['to_date'])
    category = Category.query.filter_by(violet_type=category_post).first()
    outputname = f"{category_post}_{from_period}_{to_period}"
    crimescenes = get_crime_scenes_over_period(
        category, from_period, to_period)
    uncategorized = showmap(outputname, crimescenes)
    return render_template('home/categoryanalsis.html', map_name=outputname, category=category_post, from_period=from_period, to_period=to_period, title="Analyze Crime Category", uncategorized=uncategorized)


@home.route('/admin/dashboard/crime/analysis/data', methods=['POST'])
@login_required
def analyze_crimes_data():
    if not current_user.is_admin:
        abort(403)
    """
     api for crime data
    """
    month_mask = "%B-%Y"
    """
    month:count 
    """
    graph_dataset = {}
    category_post = request.form['category_post']
    from_period = request.form['from_period']
    to_period = request.form['to_period'] if request.form['to_period'] is not None else dt.today(
    )
    category = Category.query.filter_by(violet_type=category_post).first()
    # filter scenes in the required period
    category_scenes = get_crime_scenes_over_period(
        category, from_period, to_period)
    # create dataset
    for crime_scene in category_scenes:
        dt_posted = crime_scene.date_posted
        month_year = dt.strftime(dt_posted, month_mask)
        graph_dataset[month_year] = (
            graph_dataset[month_year]+1) if month_year in graph_dataset.keys() else 1

    return jsonify({'labels': list(graph_dataset.keys()), 'data': list(graph_dataset.values())})


def get_crime_scenes_over_period(category, from_date, to_date):
    return category.crimescene.filter(CrimeScene.date_posted >= from_date).filter(CrimeScene.date_posted <= to_date).order_by(CrimeScene.date_posted.asc()).all() if category is not None else []
