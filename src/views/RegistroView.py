import flet as ft
import re


def RegistroView(page: ft.Page, auth_controller):

    def toggle_pass(e):
        password_input.password = not password_input.password
        password_input.update()

    def notificar(texto):
        page.snack_bar = ft.SnackBar(ft.Text(texto, color=ft.Colors.WHITE), bgcolor="#333333")
        page.snack_bar.open = True
        page.update()

    def validar_email(valor):
        return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", valor)) and len(valor) <= 150

    def validar_password(valor):
        return (
            8 <= len(valor) <= 100
            and any(c.isupper() for c in valor)
            and any(c.islower() for c in valor)
            and any(c.isdigit() for c in valor)
        )

    nombre_input = ft.TextField(
        label="Nombre", border_radius=10, filled=True,
        bgcolor="#F5F5F5", border_color="#CCCCCC",
        focused_border_color="#000000",
        label_style=ft.TextStyle(color="#666666"), color="#000000",
        max_length=30,
    )
    email_input = ft.TextField(
        label="Correo", border_radius=10, filled=True,
        bgcolor="#F5F5F5", border_color="#CCCCCC",
        focused_border_color="#000000",
        label_style=ft.TextStyle(color="#666666"), color="#000000",
        max_length=150,
    )
    password_input = ft.TextField(
        label="Contraseña", password=True, border_radius=10, filled=True,
        bgcolor="#F5F5F5", border_color="#CCCCCC",
        focused_border_color="#000000",
        label_style=ft.TextStyle(color="#666666"), color="#000000",
        max_length=100,
        suffix=ft.IconButton(icon=ft.Icons.VISIBILITY_OUTLINED, icon_color="#666666", on_click=toggle_pass),
    )

    error_nombre = ft.Text("", size=11, color="#CC0000")
    error_email = ft.Text("", size=11, color="#CC0000")
    error_password = ft.Text("", size=11, color="#CC0000")

    def req_row(texto, cumple):
        return ft.Row(
            spacing=6,
            controls=[
                ft.Icon(
                    ft.Icons.CHECK_CIRCLE if cumple else ft.Icons.RADIO_BUTTON_UNCHECKED,
                    size=14,
                    color="#22AA44" if cumple else "#AAAAAA",
                ),
                ft.Text(texto, size=11, color="#22AA44" if cumple else "#AAAAAA"),
            ],
        )

    requisitos = ft.Column(spacing=2, visible=False)

    def actualizar_requisitos(v):
        requisitos.controls = [
            req_row("Mínimo 8 caracteres", len(v) >= 8),
            req_row("Al menos una mayúscula", any(c.isupper() for c in v)),
            req_row("Al menos una minúscula", any(c.islower() for c in v)),
            req_row("Al menos un número", any(c.isdigit() for c in v)),
        ]
        requisitos.visible = bool(v)
        requisitos.update()

    def on_nombre_change(e):
        v = nombre_input.value
        if v and len(v.strip()) < 2:
            error_nombre.value = "El nombre debe tener al menos 2 caracteres"
            nombre_input.border_color = "#CC0000"
        elif v and len(v) > 30:
            error_nombre.value = "El nombre no puede superar 30 caracteres"
            nombre_input.border_color = "#CC0000"
        else:
            error_nombre.value = ""
            nombre_input.border_color = "#CCCCCC"
        nombre_input.update()
        error_nombre.update()

    def on_email_change(e):
        v = email_input.value
        if v and len(v) > 30:
            error_email.value = "El correo no puede superar 30 caracteres"
            email_input.border_color = "#CC0000"
        elif v and not validar_email(v):
            error_email.value = "Ingresa un correo válido (ejemplo@dominio.com)"
            email_input.border_color = "#CC0000"
        else:
            error_email.value = ""
            email_input.border_color = "#CCCCCC"
        email_input.update()
        error_email.update()

    def on_password_change(e):
        v = password_input.value
        actualizar_requisitos(v)
        if v and len(v) > 30:
            password_input.border_color = "#CC0000"
        elif v and not validar_password(v):
            password_input.border_color = "#CC0000"
        else:
            error_password.value = ""
            password_input.border_color = "#CCCCCC"
        password_input.update()
        error_password.update()

    nombre_input.on_change = on_nombre_change
    email_input.on_change = on_email_change
    password_input.on_change = on_password_change

    def crear_usuario(e):
        nombre = nombre_input.value.strip()
        email = email_input.value.strip()
        password = password_input.value

        if not nombre or not email or not password:
            notificar("Completa todos los campos")
            return
        if len(nombre) < 2:
            notificar("El nombre es muy corto")
            return
        if len(nombre) > 30:
            notificar("El nombre es demasiado largo")
            return
        if not validar_email(email):
            notificar("El correo no es válido")
            return
        if not validar_password(password):
            notificar("La contraseña no cumple los requisitos")
            return
        try:
            resultado, mensaje = auth_controller.registrar_Usuario(nombre, email, password)
            if resultado:
                user, _ = auth_controller.login(email, password)
                if user:
                    page.user_data = user
                page.go("/casa")
            else:
                notificar(mensaje)
        except Exception as ex:
            notificar(f"Error: {str(ex)}")

    return ft.View(
        route="/registro",
        bgcolor="#FFFFFF",
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                padding=ft.padding.only(top=50, left=25, right=25, bottom=60),
                bgcolor="#FFFFFF", border=ft.border.all(1, "#E0E0E0"),
                shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color=ft.Colors.with_opacity(0.1, "#000000"), offset=ft.Offset(0, 4)),
                content=ft.Column(
                    tight=True, spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=60, height=60, border_radius=30,
                            bgcolor="#F0F0F0", border=ft.border.all(1, "#DDDDDD"),
                            content=ft.Icon(ft.Icons.PERSON_ADD_ROUNDED, size=35, color="#000000"),
                        ),
                        ft.Text("Crear cuenta", size=22, weight="bold", color="#000000"),
                        ft.Divider(height=2, color=ft.Colors.TRANSPARENT),
                        nombre_input,
                        error_nombre,
                        email_input,
                        error_email,
                        password_input,
                        requisitos,
                        error_password,
                        ft.ElevatedButton(
                            "Registrarse", width=290, height=45,
                            style=ft.ButtonStyle(bgcolor="#000000", color="#FFFFFF", shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=crear_usuario,
                        ),
                        ft.TextButton("Ya tengo cuenta", style=ft.ButtonStyle(color="#000000"), on_click=lambda _: page.go("/")),
                        ft.TextButton("← Volver al inicio", style=ft.ButtonStyle(color="#888888"), on_click=lambda _: page.go("/casa")),
                    ],
                ),
            )
        ],
    )
