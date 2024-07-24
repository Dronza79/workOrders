def get_all_workers():
    from .models import Person
    return list(Person.select())
