import re
from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .models import *


def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    
    return redirect("/login")
    

def login(request):
    if request.method == "POST":
        print(request.POST)
        user = User.objects.filter(email=request.POST['email'])
        if user:
            log_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):

                user = {
                    "id" : log_user.id,
                    "name": f"{log_user}",
                    "email": log_user.email,
                    "role": log_user.role
                }

                request.session['usuario'] = user
                messages.success(request, "Logueado correctamente.")
                return redirect("/")
            else:
                messages.error(request, "Password o Email  incorrectos.")
        else:
            messages.error(request, "Email o password incorrectos.")



        return redirect("/login")
    else:
        return render(request, 'login.html')


def registro(request):
    if request.method == "POST":

        errors = User.objects.validador_basico(request.POST)
        # print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                # print("DESDE EL FOR: ",key, value)
            
            request.session['register_name'] =  request.POST['name']
            request.session['register_email'] =  request.POST['email']

        else:
            request.session['register_name'] = ""
            request.session['register_email'] = ""

            password_encryp = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 

            usuario_nuevo = User.objects.create(
                name = request.POST['name'],
                email=request.POST['email'],
                password=password_encryp,
                role=request.POST['role']
            )

            messages.success(request, "El usuario fue agregado con exito.")
            

            user = {
                "id" : usuario_nuevo.id,
                "name": f"{usuario_nuevo}",
                "email": usuario_nuevo.email,
                "role": usuario_nuevo.role
            }

            request.session['usuario'] = user
            return redirect("/")

        return redirect("/registro")
    else:
        return render(request, 'registro.html')

def wall(request):
    print("hola")

def post_message(request):
    message=Message.objects.create(
        message=request.POST['message'], 
        user=User.objects.get(id=request.session['usuario']['id']))
    return redirect("/")

def add_comment(request):
    comment=Comment.objects.create(
        comment_u=request.POST['tcomment'], 
        user=User.objects.get(id=request.session['usuario']['id']),
        message=Message.objects.get(id=request.POST['comment_id']))
    return redirect("/")