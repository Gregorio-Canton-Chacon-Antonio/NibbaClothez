import flet as ft


def PerfilView(page, auth_controller):
    datos = getattr(page, "user_data", None) or {}

    def campo_dato(etiqueta, valor, icono):
        return ft.Container(
            padding=16, border_radius=12, bgcolor="#FFFFFF",
            border=ft.border.all(1, "#E0E0E0"),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.with_opacity(0.08, "#000000"), offset=ft.Offset(0, 2)),
            content=ft.Row(
                spacing=12,
                controls=[
                    ft.Container(
                        width=40, height=40, border_radius=20,
                        bgcolor="#F0F0F0", border=ft.border.all(1, "#DDDDDD"),
                        content=ft.Icon(icono, size=22, color="#000000"),
                    ),
                    ft.Column(
                        spacing=2, expand=True,
                        controls=[
                            ft.Text(etiqueta, size=11, color="#888888"),
                            ft.Text(str(valor) if valor else "—", size=14, color="#000000", weight="w500"),
                        ],
                    ),
                ],
            ),
        )

    encabezado = ft.Container(
        padding=ft.padding.only(left=16, right=16, top=12, bottom=8),
        bgcolor="#FFFFFF",
        border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0")),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("Mi perfil", size=18, weight="bold", color="#000000"),
                ft.Row(
                    spacing=4,
                    controls=[
                ft.IconButton(ft.Icons.HOME_ROUNDED, icon_color="#000000", on_click=lambda _: page.go("/casa")),
                ft.IconButton(ft.Icons.CHECKROOM_ROUNDED, icon_color="#000000", on_click=lambda _: page.go("/dashboard")),
                        ft.IconButton(ft.Icons.LOGOUT_ROUNDED, icon_color="#000000", on_click=lambda _: [setattr(page, "user_data", None), page.go("/")][1]),
                    ],
                ),
            ],
        ),
    )

    tarjeta_perfil = ft.Container(
        padding=20, border_radius=16, bgcolor="#FFFFFF",
        border=ft.border.all(1, "#E0E0E0"),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=12, color=ft.Colors.with_opacity(0.08, "#000000"), offset=ft.Offset(0, 2)),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8,
            controls=[
                ft.Container(
                    width=80, height=80, border_radius=40,
                    bgcolor="#F0F0F0", border=ft.border.all(1, "#DDDDDD"),
                    content=ft.Icon(ft.Icons.PERSON_ROUNDED, size=45, color="#000000"),
                ),
                ft.Text(datos.get("nombre", "Usuario"), size=22, weight="bold", color="#000000"),
                ft.Text(datos.get("email", ""), size=13, color="#888888"),
            ],
        ),
    )

    return ft.View(
        route="/perfil",
        bgcolor="#F7F7F7",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            encabezado,
            ft.Container(
                padding=20,
                content=ft.Column(
                    spacing=12,
                    controls=[
                        tarjeta_perfil,
                        campo_dato("Correo", datos.get("email"), ft.Icons.EMAIL_ROUNDED),
                        campo_dato("Fecha de registro", datos.get("fecha_registro"), ft.Icons.CALENDAR_TODAY_ROUNDED),
                    ],
                ),
            ),
        ],
    )
