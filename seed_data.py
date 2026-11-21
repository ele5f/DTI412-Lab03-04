# Run: python manage.py shell < seed_data.py
from core.models import Department, Employee, Course, TrainingRecord, Category, Product

hr = Department.objects.create(name="Human Resources", code="HR")
it = Department.objects.create(name="Information Technology", code="IT")
fin = Department.objects.create(name="Finance", code="FIN")

e1 = Employee.objects.create(employee_code="EMP001", first_name="John", last_name="Doe", email="john@example.com", salary=65000.00, department=it)
e2 = Employee.objects.create(employee_code="EMP002", first_name="Jane", last_name="Smith", email="jane@example.com", salary=75000.00, department=it)
e3 = Employee.objects.create(employee_code="EMP003", first_name="Alice", last_name="Johnson", email="alice@example.com", salary=55000.00, department=hr)
e4 = Employee.objects.create(employee_code="EMP004", first_name="Bob", last_name="Brown", email="bob@example.com", salary=60000.00, department=fin)

c1 = Course.objects.create(code="SEC101", title="Cybersecurity Essentials", capacity=25)
c2 = Course.objects.create(code="DEV201", title="Advanced Django ORM", capacity=30)

TrainingRecord.objects.create(employee=e1, course=c1, completion_status="COMPLETED", score=88.50)
TrainingRecord.objects.create(employee=e1, course=c2, completion_status="IN_PROGRESS")
TrainingRecord.objects.create(employee=e2, course=c2, completion_status="COMPLETED", score=95.00)
TrainingRecord.objects.create(employee=e3, course=c1, completion_status="REGISTERED")

# Part 6 sample data
elec = Category.objects.create(name="Electronics")
gad = Category.objects.create(name="Gadgets")
Product.objects.create(name="Laptop", category=elec, price=25000, max_allowed_price=30000, stock_quantity=5, reorder_level=10, status="NORMAL", warehouse_country="Japan")
Product.objects.create(name="Phone", category=elec, price=9000, max_allowed_price=12000, stock_quantity=50, reorder_level=10, status="DISCOUNTED", warehouse_country="China")
Product.objects.create(name="Headset", category=elec, price=3000, max_allowed_price=4000, stock_quantity=30, reorder_level=10, status="DISCOUNTED", warehouse_country="Vietnam")
Product.objects.create(name="Smart Watch", category=gad, price=1000, max_allowed_price=1100, stock_quantity=15, reorder_level=10, is_promotional=True, status="NORMAL", warehouse_country="China")
Product.objects.create(name="Drone", category=gad, price=2000, max_allowed_price=3000, stock_quantity=8, reorder_level=10, status="NORMAL", warehouse_country="Thailand")
print("Seeded.")
