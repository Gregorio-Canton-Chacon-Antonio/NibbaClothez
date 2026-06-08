import flet as ft
import re


def LoginView(page: ft.Page, auth_controller):

    def mostrar_password(e):
        password_field.password = not password_field.password
        password_field.update()

    def notificar(texto):
        page.snack_bar = ft.SnackBar(ft.Text(texto, color=ft.Colors.WHITE), bgcolor="#333333")
        page.snack_bar.open = True
        page.update()

    def validar_email(valor):
        return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", valor)) and len(valor) <= 150

    def validar_password(valor):
        return len(valor) >= 4

    email_field = ft.TextField(
        label="Correo", border_radius=10, filled=True,
        bgcolor="#F5F5F5", border_color="#CCCCCC",
        focused_border_color="#000000",
        label_style=ft.TextStyle(color="#666666"), color="#000000",
        max_length=150,
    )
    password_field = ft.TextField(
        label="Contraseña", password=True, border_radius=10, filled=True,
        bgcolor="#F5F5F5", border_color="#CCCCCC",
        focused_border_color="#000000",
        label_style=ft.TextStyle(color="#666666"), color="#000000",
        max_length=100,
        suffix=ft.IconButton(icon=ft.Icons.VISIBILITY_OUTLINED, icon_color="#666666", on_click=mostrar_password),
    )

    error_email = ft.Text("", size=11, color="#CC0000")
    error_password = ft.Text("", size=11, color="#CC0000")

    def on_email_change(e):
        v = email_field.value
        if v and len(v) > 150:
            error_email.value = "El correo es demasiado largo"
            email_field.border_color = "#CC0000"
        elif v and not validar_email(v):
            error_email.value = "Ingresa un correo válido (ejemplo@dominio.com)"
            email_field.border_color = "#CC0000"
        else:
            error_email.value = ""
            email_field.border_color = "#CCCCCC"
        email_field.update()
        error_email.update()

    def on_password_change(e):
        v = password_field.value
        if v and not validar_password(v):
            error_password.value = "La contraseña es demasiado corta"
            password_field.border_color = "#CC0000"
        else:
            error_password.value = ""
            password_field.border_color = "#CCCCCC"
        password_field.update()
        error_password.update()

    email_field.on_change = on_email_change
    password_field.on_change = on_password_change

    def hacer_login(e):
        email_field.value = email_field.value.strip()
        if not email_field.value or not password_field.value:
            notificar("Completa todos los campos")
            return
        if not validar_email(email_field.value):
            notificar("El correo no es válido")
            return
        if not validar_password(password_field.value):
            notificar("La contraseña no cumple los requisitos")
            return
        try:
            usuario, msg = auth_controller.login(email_field.value, password_field.value)
            if usuario:
                page.user_data = usuario
                destino = getattr(page, "redirect_after_login", None) or "/casa"
                page.redirect_after_login = None
                page.go(destino)
            else:
                notificar(msg)
        except Exception as error:
            notificar(f"Error: {str(error)}")

    return ft.View(
        route="/",
        bgcolor="#FFFFFF",
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                padding=ft.padding.only(top=60, left=25, right=25, bottom=60),
                bgcolor="#FFFFFF", border=ft.border.all(1, "#E0E0E0"),
                shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color=ft.Colors.with_opacity(0.1, "#000000"), offset=ft.Offset(0, 4)),
                content=ft.Column(
                    tight=True, spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=64, height=64, border_radius=0,
                            bgcolor="#F0F0F0", border=ft.border.all(1, "#DDDDDD"),
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            content=ft.Image(src="assets/img/Nibbaz.jpeg", fit="cover"),
                        ),
                        ft.Text("Nibba Clothez", size=24, weight="bold", color="#000000"),
                        ft.Text("Inicia sesión", size=13, color="#888888"),
                        ft.Divider(height=4, color=ft.Colors.TRANSPARENT),
                        email_field,
                        error_email,
                        password_field,
                        error_password,
                        ft.ElevatedButton(
                            "Entrar", width=290, height=45,
                            style=ft.ButtonStyle(bgcolor="#000000", color="#FFFFFF", shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=hacer_login,
                        ),
                        ft.TextButton("¿Olvidaste tu contraseña?", style=ft.ButtonStyle(color="#666666"), on_click=lambda _: page.go("/recuperar")),
                        ft.TextButton("¿Sin cuenta? Regístrate", style=ft.ButtonStyle(color="#000000"), on_click=lambda _: page.go("/registro")),
                        ft.TextButton("← Volver al inicio", style=ft.ButtonStyle(color="#888888"), on_click=lambda _: page.go("/casa")),
                    ],
                ),
            )
        ],
    )
