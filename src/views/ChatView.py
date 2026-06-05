import flet as ft

def ChatView(page: ft.Page, mensaje_controller):
    usuario_actual = getattr(page, "user_data", None)
    receptor = getattr(page, "chat_receptor", None)

    if not usuario_actual or not receptor:
        return ft.View(route="/chat", controls=[ft.Text("Error al abrir el chat")])

    id_yo = usuario_actual["id_usuario"]
    id_receptor = receptor["id_usuario"]

    def build_burbuja(m):
        es_mio = m["id_emisor"] == id_yo
        return ft.Row(
            alignment=ft.MainAxisAlignment.END if es_mio else ft.MainAxisAlignment.START,
            controls=[
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    border_radius=ft.border_radius.only(
                        top_left=14, top_right=14,
                        bottom_left=0 if es_mio else 14,
                        bottom_right=14 if es_mio else 0,
                    ),
                    bgcolor="#000000" if es_mio else "#F0F0F0",
                    content=ft.Text(m["contenido"], size=14, color="#FFFFFF" if es_mio else "#000000"),
                )
            ],
        )

    mensajes_iniciales = [
        build_burbuja(m)
        for m in mensaje_controller.obtener_conversacion(id_yo, id_receptor)
    ]

    lista = ft.Column(spacing=8, controls=mensajes_iniciales)

    campo = ft.TextField(
        hint_text="Escribe un mensaje...",
        expand=True, border_radius=20, filled=True,
        bgcolor="#F0F0F0", border_color="transparent",
        focused_border_color="#000000",
        hint_style=ft.TextStyle(color="#AAAAAA", size=13),
        text_style=ft.TextStyle(color="#000000", size=13),
        content_padding=ft.padding.symmetric(horizontal=14, vertical=10),
    )

    def enviar(_):
        texto = campo.value.strip()
        if not texto:
            return
        mensaje_controller.enviar(id_yo, id_receptor, texto)
        m = {"id_emisor": id_yo, "contenido": texto}
        lista.controls.append(build_burbuja(m))
        campo.value = ""
        page.update()

    foto = receptor.get("foto_perfil")
    avatar = ft.Container(
        width=34, height=34, border_radius=17,
        bgcolor="#F0F0F0", clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Image(src=foto, fit="cover", width=34, height=34)
        if foto else ft.Icon(ft.Icons.PERSON_ROUNDED, size=20, color="#000000"),
    )

    return ft.View(
        route="/chat",
        bgcolor="#FFFFFF",
        scroll=ft.ScrollMode.AUTO,
        padding=0,
        controls=[
            ft.Container(
                padding=ft.padding.only(left=6, right=16, top=8, bottom=8),
                bgcolor="#FFFFFF",
                border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0")),
                content=ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=8,
                    controls=[
                        ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, icon_color="#000000", on_click=lambda _: page.go("/mensajes")),
                        avatar,
                        ft.Text(receptor["nombre"], size=16, weight="bold", color="#000000"),
                    ]
                )
            ),
            ft.Container(
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                content=lista,
            ),
            ft.Container(
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
                bgcolor="#FFFFFF",
                border=ft.border.only(top=ft.BorderSide(1, "#E0E0E0")),
                content=ft.Row(
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        campo,
                        ft.IconButton(
                            ft.Icons.SEND_ROUNDED, icon_color="#000000",
                            style=ft.ButtonStyle(bgcolor="#F0F0F0", shape=ft.CircleBorder()),
                            on_click=enviar,
                        ),
                    ]
                )
            ),
        ]
    )
