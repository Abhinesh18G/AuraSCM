"""
Sample module: order_service.py (Branch B - feature/percentage-discount)
This branch changes calculate_total() to use a PERCENTAGE discount instead
of a flat amount -- a semantic conflict that plain text diff/Git would
often merge silently if the surrounding lines don't overlap.
"""


"""
Sample module: order_service.py (Branch A - feature/discount-fix)
This branch changes the signature and logic of calculate_total().
"""


def calculate_total(price, quantity, discount=0):
    """Branch A: discount applied as a flat amount."""
    subtotal = price * quantity
    total = subtotal - discount
    return total


def apply_tax(total, tax_rate=0.18):
    return total + (total * tax_rate)


def get_order_summary(price, quantity, discount=0):
    total = calculate_total(price, quantity, discount)
    final = apply_tax(total)
    return {"subtotal": price * quantity, "discount": discount, "final": final}
