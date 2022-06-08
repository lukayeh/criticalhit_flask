# app/booker/routes.py
# this is where you can put all your booker routes
from flask import Blueprint
from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
from application.companies import companies_blueprint
from flask import render_template
import utils # import utils!

###############################################
#          Module Level Variables             #
###############################################
my_company=2

###############################################
#          Render companies page              #
###############################################
@companies_blueprint.route('/companies')
def companies():
    conn = utils.get_db_connection()
    companies = conn.execute('SELECT * FROM companies').fetchall()
    conn.close()
    return render_template('companies.html', title='Companies', companies=companies)
