from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.messages import get_messages
from django.contrib.staticfiles import finders
from django.test import Client, TestCase
from django.urls import reverse

from .models import Usuario


class UsuarioCrudTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin_teste",
            password="senha-forte-de-teste",
            is_superuser=True,
        )
        self.client.force_login(self.user)
        self.usuario = Usuario.objects.create(nome="Ana", idade=29)

    def test_home_exibe_formulario_de_cadastro(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cadastro de usuários")
        self.assertContains(response, 'name="nome"')
        self.assertContains(response, 'name="idade"')
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_cria_usuario_valido(self):
        response = self.client.post(
            reverse("listagem_usuarios"),
            {"nome": "Bruno", "idade": 34},
            follow=True,
        )

        self.assertRedirects(response, reverse("listagem_usuarios"))
        self.assertTrue(Usuario.objects.filter(nome="Bruno", idade=34).exists())
        self.assertContains(response, "Usuário cadastrado com sucesso.")

    def test_rejeita_cadastro_invalido(self):
        response = self.client.post(
            reverse("listagem_usuarios"),
            {"nome": "", "idade": -1},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Usuario.objects.count(), 1)
        self.assertContains(response, "Informe o nome do usuário.", status_code=400)
        self.assertContains(response, "A idade não pode ser negativa.", status_code=400)

    def test_lista_usuarios(self):
        response = self.client.get(reverse("listagem_usuarios"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ana")
        self.assertContains(response, "29")

    def test_edita_usuario(self):
        url = reverse("editar_usuario", args=[self.usuario.id_usuario])
        response = self.client.post(
            url,
            {"nome": "Ana Maria", "idade": 30},
            follow=True,
        )

        self.assertRedirects(response, reverse("listagem_usuarios"))
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.nome, "Ana Maria")
        self.assertEqual(self.usuario.idade, 30)
        self.assertContains(response, "Usuário atualizado com sucesso.")

    def test_rejeita_edicao_invalida(self):
        url = reverse("editar_usuario", args=[self.usuario.id_usuario])
        response = self.client.post(url, {"nome": "A", "idade": 200})

        self.assertEqual(response.status_code, 400)
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.nome, "Ana")
        self.assertEqual(self.usuario.idade, 29)

    def test_edicao_de_usuario_inexistente_retorna_404(self):
        response = self.client.get(reverse("editar_usuario", args=[999999]))

        self.assertEqual(response.status_code, 404)

    def test_confirmacao_nao_exclui_usuario(self):
        response = self.client.get(
            reverse("excluir_usuario", args=[self.usuario.id_usuario])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Usuario.objects.filter(pk=self.usuario.pk).exists())
        self.assertContains(response, "Confirmar exclusão")
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_exclui_usuario_com_post(self):
        response = self.client.post(
            reverse("excluir_usuario", args=[self.usuario.id_usuario]),
            follow=True,
        )

        self.assertRedirects(response, reverse("listagem_usuarios"))
        self.assertFalse(Usuario.objects.filter(pk=self.usuario.pk).exists())
        self.assertContains(response, "excluído com sucesso")

    def test_exclusao_de_usuario_inexistente_retorna_404(self):
        response = self.client.post(reverse("excluir_usuario", args=[999999]))

        self.assertEqual(response.status_code, 404)

    def test_operacoes_de_escrita_exigem_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)

        create_response = client.post(
            reverse("listagem_usuarios"),
            {"nome": "Bruno", "idade": 34},
        )
        update_response = client.post(
            reverse("editar_usuario", args=[self.usuario.id_usuario]),
            {"nome": "Ana Maria", "idade": 30},
        )
        delete_response = client.post(
            reverse("excluir_usuario", args=[self.usuario.id_usuario])
        )

        self.assertEqual(create_response.status_code, 403)
        self.assertEqual(update_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.nome, "Ana")

    def test_mensagem_de_erro_e_registrada(self):
        response = self.client.post(
            reverse("listagem_usuarios"),
            {"nome": "", "idade": "inválida"},
        )

        mensagens = [str(message) for message in get_messages(response.wsgi_request)]
        self.assertIn(
            "Não foi possível cadastrar o usuário. Revise os campos.",
            mensagens,
        )


class InterfaceTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="interface_teste",
            password="senha-forte-de-teste",
            is_superuser=True,
        )
        self.client.force_login(self.user)

    def test_template_base_configura_tema_e_arquivos_estaticos(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, 'data-bs-theme="dark"')
        self.assertContains(response, 'id="theme-toggle"')
        self.assertContains(response, "usuarios/css/style.css")
        self.assertContains(response, "usuarios/js/theme.js")
        self.assertContains(response, 'href="/"')

    def test_script_de_tema_alterna_e_persiste_preferencia(self):
        script_path = finders.find("usuarios/js/theme.js")
        self.assertIsNotNone(script_path)

        script = Path(script_path).read_text(encoding="utf-8")
        self.assertIn("window.localStorage.getItem(storageKey)", script)
        self.assertIn("window.localStorage.setItem(storageKey, theme)", script)
        self.assertIn('currentTheme === "dark" ? "light" : "dark"', script)
        self.assertIn('root.setAttribute("data-bs-theme", selectedTheme)', script)

    def test_animacoes_sao_sutis_e_respeitam_movimento_reduzido(self):
        stylesheet_path = finders.find("usuarios/css/style.css")
        self.assertIsNotNone(stylesheet_path)

        stylesheet = Path(stylesheet_path).read_text(encoding="utf-8")
        self.assertIn("@keyframes page-enter", stylesheet)
        self.assertIn("@keyframes alert-enter", stylesheet)
        self.assertIn("transform: translateY(0.5rem)", stylesheet)
        self.assertIn("@media (prefers-reduced-motion: reduce)", stylesheet)
        self.assertIn("transition-duration: 0.01ms !important", stylesheet)

    def test_paleta_verde_esta_configurada_nos_dois_temas(self):
        stylesheet_path = finders.find("usuarios/css/style.css")
        self.assertIsNotNone(stylesheet_path)

        stylesheet = Path(stylesheet_path).read_text(encoding="utf-8")
        self.assertIn("--app-background: #0b0d0a", stylesheet)
        self.assertIn("--app-accent: #596422", stylesheet)
        self.assertIn("--app-background: #f7f9f5", stylesheet)
        self.assertIn("--app-accent: #3f6b3a", stylesheet)
        self.assertIn("--bs-btn-bg: var(--app-accent)", stylesheet)

    def test_respostas_incluem_content_security_policy(self):
        response = self.client.get(reverse("home"))

        policy = response.headers["Content-Security-Policy"]
        self.assertIn("default-src 'self'", policy)
        self.assertIn("object-src 'none'", policy)
        self.assertIn("frame-ancestors 'none'", policy)


class ControleDeAcessoTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(nome="Ana", idade=29)
        self.user = get_user_model().objects.create_user(
            username="usuario_limitado",
            password="senha-forte-de-teste",
        )

    def test_visitante_e_redirecionado_para_login(self):
        urls = (
            reverse("home"),
            reverse("listagem_usuarios"),
            reverse("editar_usuario", args=[self.usuario.pk]),
            reverse("excluir_usuario", args=[self.usuario.pk]),
        )

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(
                    response,
                    f"{reverse('login')}?next={url}",
                )

    def test_usuario_sem_permissoes_recebe_403(self):
        self.client.force_login(self.user)

        urls = (
            reverse("home"),
            reverse("listagem_usuarios"),
            reverse("editar_usuario", args=[self.usuario.pk]),
            reverse("excluir_usuario", args=[self.usuario.pk]),
        )

        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 403)

        create_response = self.client.post(
            reverse("listagem_usuarios"),
            {"nome": "Sem permissão", "idade": 20},
        )
        self.assertEqual(create_response.status_code, 403)
        self.assertFalse(Usuario.objects.filter(nome="Sem permissão").exists())

    def test_visitante_nao_consegue_modificar_registros(self):
        create_response = self.client.post(
            reverse("listagem_usuarios"),
            {"nome": "Intruso", "idade": 20},
        )
        edit_response = self.client.post(
            reverse("editar_usuario", args=[self.usuario.pk]),
            {"nome": "Alterada", "idade": 30},
        )
        delete_response = self.client.post(
            reverse("excluir_usuario", args=[self.usuario.pk])
        )

        self.assertEqual(create_response.status_code, 302)
        self.assertEqual(edit_response.status_code, 302)
        self.assertEqual(delete_response.status_code, 302)
        self.assertFalse(Usuario.objects.filter(nome="Intruso").exists())
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.nome, "Ana")

    def test_permissao_de_visualizacao_nao_autoriza_alteracoes(self):
        view_permission = Permission.objects.get(
            content_type__app_label="app_cad_usuarios",
            codename="view_usuario",
        )
        self.user.user_permissions.add(view_permission)
        self.client.force_login(self.user)

        list_response = self.client.get(reverse("listagem_usuarios"))
        edit_response = self.client.post(
            reverse("editar_usuario", args=[self.usuario.pk]),
            {"nome": "Alterada", "idade": 30},
        )
        delete_response = self.client.post(
            reverse("excluir_usuario", args=[self.usuario.pk])
        )

        self.assertEqual(list_response.status_code, 200)
        self.assertNotContains(list_response, ">Editar<")
        self.assertNotContains(list_response, ">Excluir<")
        self.assertEqual(edit_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.nome, "Ana")

    def test_login_e_logout(self):
        permissions = Permission.objects.filter(
            content_type__app_label="app_cad_usuarios",
            content_type__model="usuario",
        )
        self.user.user_permissions.set(permissions)

        login_response = self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": "senha-forte-de-teste"},
        )

        self.assertRedirects(login_response, reverse("listagem_usuarios"))
        self.assertIn("_auth_user_id", self.client.session)

        logout_response = self.client.post(reverse("logout"))

        self.assertRedirects(logout_response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)
