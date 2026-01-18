from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

@login_required(login_url='/')
def home(request):
    """Vista del home"""

    # productos = Producto.objects.all()
    return render(request, 'index.html')

def login_view(request):
    """Vista para acceder con el usuario en el login"""

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

@login_required(login_url='/')
def logout_view(request):
    """Vista para cerrar sesion"""

    logout(request)
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('login')