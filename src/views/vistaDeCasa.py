import flet as ft


def VistaDeCasa(page: ft.Page):

    drawer_panel = ft.Container(
        visible=False,
        width=220,
        bgcolor="#F8F8F8",
        border=ft.border.only(right=ft.BorderSide(1, "#DDDDDD")),
        expand_loose=True,
        content=ft.Column(
            spacing=0,
            controls=[
                ft.Container(height=16),
            ],
        ),
    )

    def toggle_drawer(_):
        drawer_panel.visible = not drawer_panel.visible
        page.update()

    sesion_activa = getattr(page, "user_data", None)

    if sesion_activa:
        botones_auth = [
            ft.Container(
                width=32, height=32, border_radius=8,
                bgcolor="#F0F0F0", border=ft.border.all(1, "#DDDDDD"),
                content=ft.Icon(ft.Icons.PERSON_ROUNDED, size=18, color="#000000"),
                on_click=lambda _: page.go("/perfil"),
            ),
            ft.ElevatedButton(
                "Vender", height=30,
                style=ft.ButtonStyle(
                    bgcolor="#000000", color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=8),
                    text_style=ft.TextStyle(size=11),
                    padding=ft.padding.symmetric(horizontal=10),
                ),
                on_click=lambda _: page.go("/dashboard"),
            ),
        ]
    else:
        botones_auth = [
            ft.OutlinedButton(
                "Iniciar sesión", height=30,
                style=ft.ButtonStyle(
                    side=ft.BorderSide(1, "#000000"), color="#000000",
                    shape=ft.RoundedRectangleBorder(radius=8),
                    text_style=ft.TextStyle(size=11),
                    padding=ft.padding.symmetric(horizontal=10),
                ),
                on_click=lambda _: page.go("/"),
            ),
            ft.OutlinedButton(
                "Registrarse", height=30,
                style=ft.ButtonStyle(
                    side=ft.BorderSide(1, "#000000"), color="#000000",
                    shape=ft.RoundedRectangleBorder(radius=8),
                    text_style=ft.TextStyle(size=11),
                    padding=ft.padding.symmetric(horizontal=10),
                ),
                on_click=lambda _: page.go("/registro"),
            ),
            ft.ElevatedButton(
                "Vender", height=30,
                style=ft.ButtonStyle(
                    bgcolor="#000000", color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=8),
                    text_style=ft.TextStyle(size=11),
                    padding=ft.padding.symmetric(horizontal=10),
                ),
                on_click=lambda _: [setattr(page, "redirect_after_login", "/dashboard"), page.go("/")][1],
            ),
        ]

    navbar = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=6,
        controls=[
            ft.Row(
                spacing=6,
                controls=[
                    ft.Container(
                        width=32, height=32, border_radius=8,
                        bgcolor="#F0F0F0", border=ft.border.all(1, "#DDDDDD"),
                        content=ft.Icon(ft.Icons.MENU_ROUNDED, size=18, color="#000000"),
                        on_click=toggle_drawer,
                    ),
                    ft.Container(
                        width=32, height=32, border_radius=8,
                        bgcolor="#F0F0F0", border=ft.border.all(1, "#DDDDDD"),
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        content=ft.Image(src="Nibbaz.jpeg", fit="cover"),
                    ),
                ],
            ),
            ft.Row(spacing=6, controls=botones_auth),
        ],
    )

    return ft.View(
        route="/casa",
        bgcolor="#FFFFFF",
        padding=ft.padding.symmetric(horizontal=16, vertical=16),
        controls=[
            navbar,
            ft.TextField(
                hint_text="Buscar...",
                height=38,
                border_radius=10,
                filled=True,
                bgcolor="#F0F0F0",
                border_color="#DDDDDD",
                focused_border_color="#000000",
                hint_style=ft.TextStyle(color="#AAAAAA", size=13),
                text_style=ft.TextStyle(color="#000000", size=13),
                prefix_icon=ft.Icons.SEARCH_ROUNDED,
                content_padding=ft.padding.symmetric(horizontal=10, vertical=6),
            ),
            ft.Row(
                spacing=0,
                expand=True,
                controls=[drawer_panel],
            ),
        ],
    )
