# Run: python manage.py shell < part4_practice.py
import django.db
from django.db import connection
from django.db.models import Q, F
from core.models import Employee, Course

print("\n===== Task 4.1: Q objects =====")
query_or = Employee.objects.filter(Q(department__code="IT") | Q(salary__gt=70000))
print("OR Query Results:", list(query_or))
print("SQL:", query_or.query)

query_not = Employee.objects.filter(Q(first_name__icontains="John") & ~Q(department__code="HR"))
print("AND NOT Query Results:", list(query_not))
print("SQL:", query_not.query)

print("\n===== Task 4.2: F expressions =====")
Employee.objects.filter(department__code="IT").update(salary=F('salary') * 1.10)
for emp in Employee.objects.filter(department__code="IT"):
    print(f"{emp.first_name} New Salary: {emp.salary}")


print("\n===== Task 4.3: N+1 problem =====")
django.db.reset_queries()
for emp in Employee.objects.all():
    print(f"Employee: {emp.first_name}, Department: {emp.department.name}")

print(f"Total Queries Executed (Unoptimized): {len(connection.queries)}")

django.db.reset_queries()
for emp in Employee.objects.select_related('department').all():
    print(f"Employee: {emp.first_name}, Department: {emp.department.name}")

print(f"Total Queries with select_related: {len(connection.queries)}")

django.db.reset_queries()
for course in Course.objects.prefetch_related('attendees').all():
    names = [emp.first_name for emp in course.attendees.all()]
    print(f"Course: {course.code}, Attendees: {', '.join(names)}")

print(f"Total Queries with prefetch_related: {len(connection.queries)}")
