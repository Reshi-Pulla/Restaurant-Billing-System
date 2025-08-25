def calculate_total(order_items, menu):
    subtotal = 0
    for item in menu:
        if item[0] in order_items:
            subtotal += order_items[item[0]] * item[3] * (1 + item[4] / 100)
    return round(subtotal, 2)