import flet as ft

CONDICION_LABELS = {
    "nuevo": "Nuevo",
    "como_nuevo": "Como nuevo",
    "usado_excelente": "Usado - Excelente",
    "usado_buen_estado": "Usado - Buen estado",
    "usado_aceptable": "Usado - Aceptable",
}


def PerfilVendedorView(page: ft.Page, prenda_controller):
    vendedor = getattr(page, "selected_vendedor", None)

    if not vendedor:
        return ft.View(route="/perfil_vendedor", controls=[ft.Text("Perfil no encontrado")])

    prendas = prenda_controller.obtener_lista(vendedor["id_usuario"])

    foto = vendedor.get("foto_perfil")
    avatar = ft.Container(
        width=80, height=80, border_radius=40,
        bgcolor="#F0F0F0", border=ft.border.all(1, "#DDDDDD"),
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Image(src=foto, fit="cover", width=80, height=80)
        if foto else ft.Icon(ft.Icons.PERSON_ROUNDED, size=45, color="#000000"),
    )

    tarjeta_perfil = ft.Container(
        padding=20, border_radius=16, bgcolor="#FFFFFF",
        border=ft.border.all(1, "#E0E0E0"),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=12, color=ft.Colors.with_opacity(0.08, "black"), offset=ft.Offset(0, 2)),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8,
            controls=[
                avatar,
                ft.Text(vendedor.get("nombre", "Usuario"), size=22, weight="bold", color="#000000"),
                ft.Text(vendedor.get("email", ""), size=13, color="#888888"),
            ],
        ),
    )

    def mostrar_prenda(p):
        page.selected_prenda = p
        page.go("/prenda")

    grid = ft.ResponsiveRow(spacing=12, run_spacing=12)
    for p in prendas:
        fotos = [f for f in (p.get("foto") or "").split("|") if f]
        grid.controls.append(
            ft.Container(
                col={"xs": 6},
                padding=10, border_radius=12, bgcolor="#FFFFFF",
                border=ft.border.all(1, "#F0F0F0"),
                ink=True,
                on_click=lambda _, item=p: mostrar_prenda(item),
                shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.with_opacity(0.05, "black")),
                content=ft.Column(
                    spacing=6,
                    controls=[
                        ft.Container(
                            height=130, border_radius=8, bgcolor="#F5F5F5",
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            content=ft.Image(src=fotos[0], fit="cover", width=float("inf"), height=130)
                            if fotos else ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED_ROUNDED, color="#CCCCCC"),
                        ),
                        ft.Text(p["titulo"], size=13, weight="bold", max_lines=1, overflow=ft.TextOverflow.ELLIPSIS, color="#000000"),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(f"${p['precio']}", size=12, weight="bold", color="#22AA44"),
                                ft.Text(p["talla"], size=11, color="#666666"),
                            ]
                        ),
                    ]
                )
            )
        )

    return ft.View(
        route="/perfil_vendedor",
        bgcolor="#F7F7F7",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Container(
                padding=ft.padding.only(left=10, top=10, bottom=10),
                bgcolor="#FFFFFF",
                border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0")),
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                        icon_color="#000000",
                        on_click=lambda _: page.go("/prenda"),
                    ),
                    ft.Text("Perfil del vendedor", size=18, weight="bold", color="#000000"),
                ]),
            ),
            ft.Container(
                padding=20,
                content=ft.Column(
                    spacing=16,
                    controls=[
                        tarjeta_perfil,
                        ft.Text("Publicaciones", size=16, weight="bold", color="#000000"),
                        grid if prendas else ft.Text("Este vendedor no tiene publicaciones.", size=13, color="#888888"),
                    ]
                )
            ),
        ],
    )
