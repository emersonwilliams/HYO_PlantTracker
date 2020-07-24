from . import models

pers1 = models.User(user_id = 1, user_name = "Test1", passwd = "1234")
pers2 = models.User(user_id = 2, user_name = "Test2", passwd = "1234")

pers1.save()
pers2.save()

user_dict = {}
for obj in models.User.objects.all():
    print(obj)
    user_dict[obj.user_name] = obj.passwd

def check_login(usrnm, psswd):
    try:
        return user_dict[usrnm] == psswd
    except:
        return False
