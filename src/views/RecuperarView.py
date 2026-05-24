import flet as ft
import re


def RecuperarView(page: ft.Page, auth_controller):
    estado = {"id_usuario": None, "paso": 1}

    def notificar(texto):
        snackbar = ft.SnackBar(ft.Text(texto, color=ft.Colors.WHITE), bgcolor="#333333", open=True)
        page.overlay.append(snackbar)
        page.update()

    def validar_email(valor):
        return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", valor))

    def validar_password(valor):
        return len(valor) >= 8 and len(valor) <= 30 and any(c.isupper() for c in valor) and any(c.islower() for c in valor)


    email_field = ft.TextField(
        label="Correo registrado", border_radius=10, filled=True,
        bgcolor="#F5F5F5", border_color="#CCCCCC", focused_border_color="#000000",
        label_style=ft.TextStyle(color="#666666"), color="#000000", max_length=150,
    )

    def enviar_codigo(e):
        email = email_field.value.strip()
        if not email or not validar_email(email):
            notificar("Ingresa un correo válido")
            return
        notificar("Enviando código...")
        ok, id_usuario, msg = auth_controller.solicitar_recuperacion(email)
        print(f"[DEBUG] solicitar_recuperacion -> ok={ok}, id={id_usuario}, msg={msg}")
        if ok:
            estado["id_usuario"] = id_usuario
            estado["paso"] = 2
            construir_vista()
        else:
            notificar(f"Error: {msg}")

    paso1 = ft.Column(
        tight=True, spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Recuperar contraseña", size=20, weight="bold", color="#000000"),
            ft.Text("Te enviaremos un código de 6 dígitos a tu correo", size=12, color="#888888", text_align=ft.TextAlign.CENTER),
            ft.Divider(height=4, color=ft.Colors.TRANSPARENT),
            email_field,
            ft.ElevatedButton(
                "Enviar código", width=290, height=45,
                style=ft.ButtonStyle(bgcolor="#000000", color="#FFFFFF", shape=ft.RoundedRectangleBorder(radius=10)),
                on_click=enviar_codigo,
            ),
        ],
    )


    token_field = ft.TextField(
        label="Código de 6 dígitos", border_radius=10, filled=True,
        bgcolor="#F5F5F5", border_color="#CCCCCC", focused_border_color="#000000",
        label_style=ft.TextStyle(color="#666666"), color="#000000",
        max_length=6, keyboard_type=ft.KeyboardType.NUMBER,
        text_align=ft.TextAlign.CENTER,
    )

    def verificar_codigo(e):
        token = token_field.value.strip()
        if len(token) != 6 or not token.isdigit():
            notificar("Ingresa el código de 6 dígitos")
            return
        ok, msg = auth_controller.verificar_token(estado["id_usuario"], token)
        if ok:
            estado["paso"] = 3
            construir_vista()
        else:
            notificar(msg)

    paso2 = ft.Column(
        tight=True, spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Ingresa el código", size=20, weight="bold", color="#000000"),
            ft.Text("Revisa tu correo y escribe el código que recibiste", size=12, color="#888888", text_align=ft.TextAlign.CENTER),
            ft.Divider(height=4, color=ft.Colors.TRANSPARENT),
            token_field,
            ft.ElevatedButton(
                "Verificar", width=290, height=45,
                style=ft.ButtonStyle(bgcolor="#000000", color="#FFFFFF", shape=ft.RoundedRectangleBorder(radius=10)),
                on_click=verificar_codigo,
            ),
        ],
    )


    def mostrar_nueva(e):
        nueva_field.password = not nueva_field.password
        nueva_field.update()

    def mostrar_confirmar(e):
        confirmar_field.password = not confirmar_field.password
        confirmar_field.update()

    nueva_field = ft.TextField(
        label="Nueva contraseña", password=True, border_radius=10, filled=True,
        bgcolor="#F5F5F5", border_color="#CCCCCC", focused_border_color="#000000",
        label_style=ft.TextStyle(color="#666666"), color="#000000", max_length=30,
        suffix=ft.IconButton(icon=ft.Icons.VISIBILITY_OUTLINED, icon_color="#666666", on_click=mostrar_nueva),
    )
    confirmar_field = ft.TextField(
        label="Confirmar contraseña", password=True, border_radius=10, filled=True,
        bgcolor="#F5F5F5", border_color="#CCCCCC", focused_border_color="#000000",
        label_style=ft.TextStyle(color="#666666"), color="#000000", max_length=30,
        suffix=ft.IconButton(icon=ft.Icons.VISIBILITY_OUTLINED, icon_color="#666666", on_click=mostrar_confirmar),
    )

    def cambiar_password(e):
        nueva = nueva_field.value
        confirmar = confirmar_field.value
        if not validar_password(nueva):
            notificar("Mínimo 8 caracteres, una mayúscula y una minúscula")
            return
        if nueva != confirmar:
            notificar("Las contraseñas no coinciden")
            return
        ok, msg = auth_controller.cambiar_password(estado["id_usuario"], nueva)
        if ok:
            notificar("¡Contraseña actualizada correctamente!")
            page.go("/")
        else:
            notificar(msg)

    paso3 = ft.Column(
        tight=True, spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Nueva contraseña", size=20, weight="bold", color="#000000"),
            ft.Text("Elige una contraseña segura", size=12, color="#888888"),
            ft.Divider(height=4, color=ft.Colors.TRANSPARENT),
            nueva_field,
            confirmar_field,
            ft.ElevatedButton(
                "Guardar contraseña", width=290, height=45,
                style=ft.ButtonStyle(bgcolor="#000000", color="#FFFFFF", shape=ft.RoundedRectangleBorder(radius=10)),
                on_click=cambiar_password,
            ),
        ],
    )

    contenido = ft.Ref[ft.Column]()

    def construir_vista():
        pasos = {1: paso1, 2: paso2, 3: paso3}
        contenido.current.controls[-1] = pasos[estado["paso"]]
        page.update()

    return ft.View(
        route="/recuperar",
        bgcolor="#FFFFFF",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Container(
                width=360, padding=35, border_radius=16,
                bgcolor="#FFFFFF", border=ft.border.all(1, "#E0E0E0"),
                shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color=ft.Colors.with_opacity(0.1, "#000000"), offset=ft.Offset(0, 4)),
                content=ft.Column(
                    ref=contenido,
                    tight=True, spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="#000000", on_click=lambda _: page.go("/")),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        paso1,
                    ],
                ),
            )
        ],
    )
