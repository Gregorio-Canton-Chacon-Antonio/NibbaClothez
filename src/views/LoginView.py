import flet as ft
import re


def LoginView(page: ft.Page, auth_controller):

    def mostrar_password(e):
        password_field.password = not password_field.password
        password_field.update()

    def notificar(texto):
        snackbar = ft.SnackBar(ft.Text(texto, color=ft.Colors.WHITE), bgcolor="#333333", open=True)
        page.overlay.append(snackbar)
        page.update()

    def validar_email(valor):
        return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", valor)) and len(valor) <= 30

    def validar_password(valor):
        return len(valor) >= 8 and len(valor) <= 30 and any(c.isupper() for c in valor) and any(c.islower() for c in valor)

    email_field = ft.TextField(
        label="Correo", border_radius=10, filled=True,
        bgcolor="#F5F5F5", border_color="#CCCCCC",
        focused_border_color="#000000",
        label_style=ft.TextStyle(color="#666666"), color="#000000",
        max_length=30,
    )
    password_field = ft.TextField(
        label="Contraseña", password=True, border_radius=10, filled=True,
        bgcolor="#F5F5F5", border_color="#CCCCCC",
        focused_border_color="#000000",
        label_style=ft.TextStyle(color="#666666"), color="#000000",
        max_length=30,
        suffix=ft.IconButton(icon=ft.Icons.VISIBILITY_OUTLINED, icon_color="#666666", on_click=mostrar_password),
    )

    error_email = ft.Text("", size=11, color="#CC0000")
    error_password = ft.Text("", size=11, color="#CC0000")

    def on_email_change(e):
        v = email_field.value
        if v and len(v) > 30:
            error_email.value = "El correo no puede superar 30 caracteres"
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
        if v and len(v) > 30:
            error_password.value = "La contraseña no puede superar 30 caracteres"
            password_field.border_color = "#CC0000"
        elif v and not validar_password(v):
            error_password.value = "Mínimo 8 caracteres, una mayúscula y una minúscula"
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
                page.go("/dashboard")
            else:
                notificar(msg)
        except Exception as error:
            notificar(f"Error: {str(error)}")

    return ft.View(
        route="/",
        bgcolor="#FFFFFF",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                width=360, padding=35, border_radius=16,
                bgcolor="#FFFFFF", border=ft.border.all(1, "#E0E0E0"),
                shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color=ft.Colors.with_opacity(0.1, "#000000"), offset=ft.Offset(0, 4)),
                content=ft.Column(
                    tight=True, spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=64, height=64, border_radius=32,
                            bgcolor="#F0F0F0", border=ft.border.all(1, "#DDDDDD"),
                            content=ft.Icon(ft.Icons.CHECKROOM_ROUNDED, size=36, color="#000000"),
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
                        ft.TextButton("¿Sin cuenta? Regístrate", style=ft.ButtonStyle(color="#000000"), on_click=lambda _: page.go("/registro")),
                    ],
                ),
            )
        ],
    )
