import flet as ft


def VistaDeCasa(page: ft.Page):

    navbar = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=6,
        controls=[
            ft.Container(
                width=32, height=32, border_radius=8,
                bgcolor="#F0F0F0", border=ft.border.all(1, "#DDDDDD"),
                content=ft.Icon(ft.Icons.CHECKROOM_ROUNDED, size=18, color="#000000"),
            ),
            ft.ElevatedButton(
                "Iniciar sesión", height=30,
                style=ft.ButtonStyle(
                    bgcolor="#000000", color="#FFFFFF",
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
                on_click=lambda _: page.go("/dashboard") if getattr(page, "user_data", None) else page.go("/registro"),
            ),
        ],
    )

    return ft.View(
        route="/casa",
        bgcolor="#FFFFFF",
        padding=ft.padding.symmetric(horizontal=16, vertical=16),
        controls=[
            navbar,
        ],
    )
