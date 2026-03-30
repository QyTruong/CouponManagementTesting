def stats_cart(cart, coupon=None):
    total_quantity = 0
    total_price = 0
    discount_value = 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_price += c['price'] * c['quantity']

    base_price = total_price

    if coupon:
        if coupon['coupon_type']==1:
            discount_value = coupon['value']
        elif coupon['coupon_type']==2:
            discount_value = (total_price * (coupon['value']/100))
        total_price -= discount_value


    total_price = total_price if total_price >= 0 else 0

    return {
        'total_quantity': total_quantity,
        'base_price': base_price,
        'total_price': total_price,
        'discount_value': discount_value
    }




