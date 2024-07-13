from django.shortcuts import get_object_or_404
from ninja import Router
from .schemas import TypeUserSchema
from .models import User
from django.contrib.auth.hashers import make_password
from rolepermissions.roles import assign_role
from django.forms.models import model_to_dict

users_router = Router()

@users_router.get('/')
def get_all_users(request):
    users = User.objects.all()
    response = [{"id": u.id, "username": u.username, "first_name": u.first_name\
                 , "last_name": u.last_name, "cpf": u.cpf, "email": u.email, "amount": u.amount\
                    } for u in users]
    return response

@users_router.post('/', response={200: dict, 400: dict, 500: dict})
def create_user(request, type_user_schema:TypeUserSchema):
    print(type_user_schema.dict())
    user = User(**type_user_schema.user.dict())
    user.password = make_password(type_user_schema.user.password)
    try:
        user.save()
        assign_role(user, type_user_schema.type_user.type)
    except Exception as e:
        return 500, {"errors": "Erro interno do servidor"}
    return {"username": user.username}

"""
{
  "username": "josesilva",
  "first_name": "Jośe Raimundo",
  "last_name": "Silva",
  "cpf": "78429081230",
  "email": "josersilva@gmail.com",
  "password": "1234"
}
"""