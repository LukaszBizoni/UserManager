from django.urls import path

from app_cad_usuarios import views


urlpatterns = [
    path("", views.home, name="home"),
    path("usuarios/", views.usuarios, name="listagem_usuarios"),
    path(
        "usuarios/<int:id_usuario>/editar/",
        views.editar_usuario,
        name="editar_usuario",
    ),
    path(
        "usuarios/<int:id_usuario>/excluir/",
        views.excluir_usuario,
        name="excluir_usuario",
    ),
]
