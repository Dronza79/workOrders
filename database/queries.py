def get_all_workers():
    from .models import Person
    return list(Person.select())


def get_all_tasks():
    from .models import WorkTask
    return list(WorkTask.select())
