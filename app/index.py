from datetime import datetime
from flask import render_template, request
from app import app, dao, utils, db
from app.dao import create_coupon
from app.models import CouponType, UserRole


if __name__ == '__main__':
    from app.admin import admin

    app.run(debug=True)
    # with app.app_context():
    #     try:
    #         create_coupon({
    #             'code': 'SALE10',
    #             'value': 10000,
    #             'coupon_type': CouponType.FIXED,
    #             'availability_count': 300,
    #             'expiry_date': datetime(2026, 8, 21, 10, 0, 0),
    #         }, role=UserRole.ADMIN)
    #     except Exception as ex:
    #         print(ex)