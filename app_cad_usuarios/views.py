from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import UsuarioForm
from .models import Usuario


@require_http_methods(["GET"])
def home(request):
    return render(request, "usuarios/home.html", {"form": UsuarioForm()})


@require_http_methods(["GET", "POST"])
def usuarios(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário cadastrado com sucesso.")
            return redirect("listagem_usuarios")

        messages.error(request, "Não foi possível cadastrar o usuário. Revise os campos.")
        return render(request, "usuarios/home.html", {"form": form}, status=400)

    usuarios_cadastrados = Usuario.objects.order_by("id_usuario")
    return render(
        request,
        "usuarios/usuarios.html",
        {"usuarios": usuarios_cadastrados},
    )


@require_http_methods(["GET", "POST"])
def editar_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)

    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso.")
            return redirect("listagem_usuarios")

        messages.error(request, "Não foi possível atualizar o usuário. Revise os campos.")
    else:
        form = UsuarioForm(instance=usuario)

    return render(
        request,
        "usuarios/usuario_form.html",
        {"form": form, "usuario": usuario},
        status=400 if request.method == "POST" else 200,
    )


@require_http_methods(["GET", "POST"])
def excluir_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)

    if request.method == "POST":
        nome_usuario = usuario.nome
        usuario.delete()
        messages.success(request, f'Usuário "{nome_usuario}" excluído com sucesso.')
        return redirect("listagem_usuarios")

    return render(
        request,
        "usuarios/usuario_confirmar_exclusao.html",
        {"usuario": usuario},
    )
