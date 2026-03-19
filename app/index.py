from flask import render_template, request
from app import app, dao, utils, db




if __name__ == '__main__':
    from app.admin import admin

    app.run(debug=True)