from flask import Blueprint, render_template, redirect, url_for, flash, request, g

from flask_login import login_user, logout_user, login_required, current_user

from models import User, Invoice, Entity
from forms import LoginForm, InvoiceForm

bp = Blueprint('main_pages', __name__, template_folder='templates')

@bp.route('/')
def index():
    return render_template('home.html')



@bp.route('/login', methods=['GET', 'POST'])
def login():
    if g.user.is_authenticated:
       return redirect(url_for('main_pages.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main_pages.invoice_list'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    from app import db
    if g.user.is_authenticated:
        return redirect(url_for('main_pages.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.create(
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash('Invoice created successfully!', 'success')
        login_user(user)
        return redirect(url_for('main_pages.index'))
    return render_template('register.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('main_pages.login'))


@bp.route('/invoices')
@login_required
def invoice_list():
    user = g.user
    invoices = Invoice.query.all()
    return render_template('invoice_list.html', invoices=invoices, user=user)

@bp.route('/invoice/<int:id>')
@login_required
def invoice_detail(id):
    invoice = Invoice.query.get_or_404(id)
    return render_template('invoice_detail.html', invoice=invoice)


@bp.route('/invoice/new', methods=['GET', 'POST'])
@login_required
def invoice_create():
    from app import db
    form = InvoiceForm()

    if form.validate_on_submit():
        try:
            invoice = Invoice(
                number=form.number.data,
                title=form.title.data,
                customer=form.customer.data,
                description=form.description.data
            )
            db.session.add(invoice)
            db.session.flush()

            for entity_data in form.entities.data:
                entity = Entity(
                    description=entity_data['description'],
                    qty=entity_data['qty'],
                    fee=entity_data['fee'],
                    discount=entity_data.get('discount') or 0,
                    invoice_id=invoice.id
                )
                db.session.add(entity)

            db.session.commit()
            flash('Invoice created!', 'success')
            return redirect(url_for('main_pages.invoice_list'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error creating invoice: {e}', 'danger')

    return render_template('invoice_form.html', form=form)
