# Copyright 2022 Wahinipa LLC
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static',
)


@home_bp.route('/')
def base():
    if current_user:
        return redirect(url_for('home_bp.home'))
    else:
        return redirect(url_for('people_bp.login'))


@home_bp.route('/home')
@login_required
def home():
    return render_template('home.html')


