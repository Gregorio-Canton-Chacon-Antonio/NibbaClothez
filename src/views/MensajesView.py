import flet as ft

def MensajesView(page: ft.Page, mensaje_controller):
    usuario_actual = getattr(page, "user_data", None)

    if not usuario_actual:
        page.go("/")
        return ft.View(route="/mensajes", controls=[])

    lista = ft.Column(spacing=8)

    convs = mensaje_controller.obtener_conversaciones(usuario_actual["id_usuario"])

    if not convs:
        lista.controls.append(ft.Text("No tienes conversaciones aún.", size=14, color="#888888"))
    else:
        for c in convs:
            foto = c.get("foto_perfil")
            avatar = ft.Container(
                width=48, height=48, border_radius=24,
                bgcolor="#F0F0F0", clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=ft.Image(src=foto, fit="cover", width=48, height=48)
                if foto else ft.Icon(ft.Icons.PERSON_ROUNDED, size=26, color="#000000"),
            )

            def abrir_chat(_, contacto=c):
                page.chat_receptor = {
                    "id_usuario": contacto["id_usuario"],
                    "nombre": contacto["nombre"],
                    "foto_perfil": contacto.get("foto_perfil"),
                }
                page.go("/chat")

            lista.controls.append(
                ft.Container(
                    padding=12, border_radius=12, bgcolor="#FFFFFF",
                    border=ft.border.all(1, "#E0E0E0"), ink=True,
                    on_click=abrir_chat,
                    content=ft.Row(
                        spacing=12,
                        controls=[
                            avatar,
                            ft.Column(
                                spacing=2, expand=True,
                                controls=[
                                    ft.Text(c["nombre"], size=14, weight="bold", color="#000000"),
                                    ft.Text(c["ultimo_mensaje"] or "", size=12, color="#888888",
                                            max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                                ]
                            )
                        ]
                    )
                )
            )

    return ft.View(
        route="/mensajes",
        bgcolor="#F7F7F7",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Container(
                padding=ft.padding.only(left=10, right=16, top=10, bottom=10),
                bgcolor="#FFFFFF",
                border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0")),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(controls=[
                            ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, icon_color="#000000", on_click=lambda _: page.go("/casa")),
                            ft.Text("Mensajes", size=18, weight="bold", color="#000000"),
                        ]),
                    ]
                )
            ),
            ft.Container(padding=16, content=lista),
        ]
    )
