def stats_cart(cart):
    total_quantity = 0
    total_price = 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_price += c['price'] * c['quantity']

    return {
        'total_quantity': total_quantity,
        'total_price': total_price
    }




