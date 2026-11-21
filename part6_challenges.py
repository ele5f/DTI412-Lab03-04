# Run: python manage.py shell < part6_challenges.py
from decimal import Decimal
from django.db.models import Q, F, Case, When, Value, DecimalField, ExpressionWrapper
from core.models import Product

# ---------- Challenge 1 ----------
# (Electronics AND price > 10000) OR (DISCOUNTED AND NOT China)
c1 = Product.objects.filter(
    (Q(category__name="Electronics") & Q(price__gt=10000))
    | (Q(status="DISCOUNTED") & ~Q(warehouse_country="China"))
)
print("Challenge 1:", [p.name for p in c1])
# Explanation: Q objects allow nested AND (&) / OR (|) / NOT (~) in one WHERE clause;
# parentheses control precedence, and everything runs inside the database.

# ---------- Challenge 2 ----------
# stock <= reorder_level OR (promotional AND stock < reorder_level * 2)
c2 = Product.objects.filter(
    Q(stock_quantity__lte=F('reorder_level'))
    | Q(is_promotional=True, stock_quantity__lt=F('reorder_level') * 2)
)
print("Challenge 2:", [p.name for p in c2])
# Explanation: F() compares two columns of the same row, so each product uses its own
# threshold instead of a hard-coded number.

# ---------- Challenge 3 ----------
# +15% for 'Gadgets', capped at max_allowed_price, entirely in SQL
new_price = ExpressionWrapper(F('price') * Decimal('1.15'), output_field=DecimalField(max_digits=10, decimal_places=2))
Product.objects.filter(category__name="Gadgets").update(
    price=Case(
        When(max_allowed_price__lt=new_price, then=F('max_allowed_price')),
        default=new_price,
        output_field=DecimalField(max_digits=10, decimal_places=2),
    )
)
print("Challenge 3:", [(p.name, p.price) for p in Product.objects.filter(category__name="Gadgets")])
# Explanation: one UPDATE statement; Case/When picks the capped value when the new price
# would exceed max_allowed_price. No Python loop, no race condition.


# ---------- Challenge 4 ----------
def purchase(product_id, qty):
    updated = Product.objects.filter(pk=product_id, stock_quantity__gte=qty).update(
        stock_quantity=F('stock_quantity') - qty,
        total_sold=F('total_sold') + qty,
        total_revenue=F('total_revenue') + F('price') * qty,
    )
    return updated == 1  # 0 rows updated => not enough stock => purchase failed


pid = Product.objects.get(name="Laptop").pk  # stock = 5
print("Challenge 4: buy 3 ->", purchase(pid, 3))    # True
print("Challenge 4: buy 3 again ->", purchase(pid, 3))  # False (only 2 left)
p = Product.objects.get(pk=pid)
print("Laptop stock/sold/revenue:", p.stock_quantity, p.total_sold, p.total_revenue)
# Explanation: the stock check is in the WHERE clause of a single atomic UPDATE, so two
# concurrent buyers can never both succeed when stock is insufficient.
