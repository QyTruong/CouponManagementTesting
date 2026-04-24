def stats_cart(cart, coupon=None):
    total_quantity = 0
    total_price = 0
    discount_value = 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_price += c['price'] * c['quantity']

    final_price = total_price

    if coupon:
        if coupon['coupon_type']==1:
            discount_value = coupon['value']
        elif coupon['coupon_type']==2:
            discount_value = (final_price * (coupon['value']/100))
        final_price -= discount_value


    final_price = final_price if final_price >= 0 else 0

    return {
        'total_quantity': total_quantity,
        'total_price': total_price,
        'final_price': final_price,
        'discount_value': discount_value
    }




