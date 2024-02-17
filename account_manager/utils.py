from .models import Person


def register(line_user_id, employee_id, name, corporation):
    person, created = Person.objects.update_or_create(defaults={
        'line_user_id': line_user_id,
        'employee_id': employee_id,
        'name': name,
        'corporation': corporation
    }, line_user_id=line_user_id)
    return person, created


def get_user_info(line_user_id) -> Person:
    p = Person.objects.get(line_user_id=line_user_id)
    return p
