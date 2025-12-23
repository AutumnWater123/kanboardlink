from backend.services.StudentService import StudentService
from backend.services.AdminService import AdminService

def test_list_students(db):
    AdminService.add_user(db, "s1", "S1", "pwd")
    AdminService.add_user(db, "s2", "S2", "pwd")
    students = StudentService.list_all(db)
    assert len(students) >= 2
    usernames = {s.username for s in students}
    assert "s1" in usernames
    assert "s2" in usernames