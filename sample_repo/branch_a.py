"""
Sample module: order_service.py (Branch B - feature/percentage-discount)
This branch changes calculate_total() to use a PERCENTAGE discount instead
of a flat amount -- a semantic conflict that plain text diff/Git would
often merge silently if the surrounding lines don't overlap.
"""


def calculate_total(price, quantity, discount=0):
    """Branch B: discount applied as a percentage (0-100)."""
    subtotal = price * quantity
    total = subtotal - (subtotal * (discount / 100))
    return total


def apply_tax(total, tax_rate=0.18):
    return total + (total * tax_rate)


def get_order_summary(price, quantity, discount=0):
    total = calculate_total(price, quantity, discount)
    final = apply_tax(total)
    return {"subtotal": price * quantity, "discount": discount, "final": final}
