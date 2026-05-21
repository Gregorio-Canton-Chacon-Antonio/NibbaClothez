import flet as ft


def VistaDeCasa(page: ft.Page):

    navbar = ft.Row(
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        controls=[
            ft.Container(
                width=40, height=40, border_radius=8,
                bgcolor="#F0F0F0", border=ft.border.all(1, "#DDDDDD"),
                content=ft.Icon(ft.Icons.CHECKROOM_ROUNDED, size=22, color="#000000"),
            ),
            ft.ElevatedButton(
                "Iniciar sesión", height=40,
                style=ft.ButtonStyle(
                    bgcolor="#000000", color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                on_click=lambda _: page.go("/"),
            ),
            ft.OutlinedButton(
                "Registrarse", height=40,
                style=ft.ButtonStyle(
                    side=ft.BorderSide(1, "#000000"), color="#000000",
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                on_click=lambda _: page.go("/registro"),
            ),
        ],
    )

    return ft.View(
        route="/casa",
        bgcolor="#FFFFFF",
        padding=ft.padding.symmetric(horizontal=16, vertical=16),
        controls=[navbar],
    )
