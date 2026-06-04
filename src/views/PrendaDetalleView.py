import flet as ft


CONDICION_LABELS = {
    "nuevo": "Nuevo",
    "como_nuevo": "Como nuevo",
    "usado_excelente": "Usado - Excelente",
    "usado_buen_estado": "Usado - Buen estado",
    "usado_aceptable": "Usado - Aceptable",
}

def _build_carrusel(page, prenda):
    fotos = [f for f in (prenda.get("foto") or "").split("|") if f]
    if not fotos:
        return ft.Container(
            height=400, bgcolor="#F5F5F5",
            content=ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED_ROUNDED, size=100, color="#CCCCCC"),
            alignment=ft.alignment.Alignment(0, 0),
        )

    idx_state = {"i": 0}
    img_widget = ft.Image(src=fotos[0], fit="contain", width=page.window.width, height=400)
    counter = ft.Text(f"1 / {len(fotos)}", size=12, color="white") if len(fotos) > 1 else ft.Text("")

    def nav(delta):
        def handler(_):
            idx_state["i"] = (idx_state["i"] + delta) % len(fotos)
            img_widget.src = fotos[idx_state["i"]]
            counter.value = f"{idx_state['i'] + 1} / {len(fotos)}"
            img_widget.update()
            counter.update()
        return handler

    btn_style = ft.ButtonStyle(
        bgcolor=ft.Colors.with_opacity(0.55, "black"),
        shape=ft.CircleBorder(),
        padding=ft.padding.all(6),
    )

    stack_controls = [
        ft.Container(height=400, bgcolor="#F5F5F5", content=img_widget),
        ft.Container(
            bottom=8, right=12,
            bgcolor=ft.Colors.with_opacity(0.5, "black"),
            border_radius=10,
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            content=counter,
        ),
    ]

    if len(fotos) > 1:
        stack_controls += [
            ft.Container(
                left=8, top=175,
                content=ft.IconButton(ft.Icons.CHEVRON_LEFT, icon_color="white", icon_size=28, style=btn_style, on_click=nav(-1))
            ),
            ft.Container(
                right=8, top=175,
                content=ft.IconButton(ft.Icons.CHEVRON_RIGHT, icon_color="white", icon_size=28, style=btn_style, on_click=nav(1))
            ),
        ]

    return ft.Stack(height=400, controls=stack_controls)


def PrendaDetalleView(page: ft.Page):
    prenda = getattr(page, "selected_prenda", None)
    
    if not prenda:
        return ft.View(route="/prenda", controls=[ft.Text("Producto no encontrado")])

    def info_item(label, value, icon):
        return ft.Row(
            controls=[
                ft.Icon(icon, size=20, color="#555555"),
                ft.Column(
                    spacing=0,
                    controls=[
                        ft.Text(label, size=12, color="#888888"),
                        ft.Text(value, size=16, weight="w500", color="#000000"),
                    ]
                )
            ]
        )

    return ft.View(
        route="/prenda",
        bgcolor="#FFFFFF",
        scroll=ft.ScrollMode.AUTO,
        padding=0,
        controls=[
            # Barra Superior con botón de regreso
            ft.Container(
                padding=ft.padding.only(left=10, top=10, bottom=10),
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                        icon_color="#000000",
                        on_click=lambda _: page.go("/casa")
                    ),
                    ft.Text("Detalles del artículo", size=18, weight="bold", color="#000000")
                ])
            ),
            # Imagen Principal con carrusel
            _build_carrusel(page, prenda),
            # Información del Producto
            ft.Container(
                padding=20,
                content=ft.Column(
                    spacing=15,
                    controls=[
                        ft.Text(prenda["titulo"], size=24, weight="bold", color="#000000"),
                        ft.Text(f"${prenda['precio']}", size=22, weight="bold", color="#22AA44"),
                        ft.Divider(height=1, color="#EEEEEE"),
                        ft.Text("Detalles", size=18, weight="bold", color="#000000"),
                        ft.ResponsiveRow(
                            controls=[
                                ft.Column(col=6, controls=[info_item("Estado", CONDICION_LABELS.get(prenda.get("condicion"), "—"), ft.Icons.INFO_OUTLINED)]),
                                ft.Column(col=6, controls=[info_item("Talla", prenda["talla"], ft.Icons.STRAIGHTEN_ROUNDED)]),
                                ft.Column(col=6, controls=[info_item("Marca", prenda.get("marca", "Sin marca"), ft.Icons.LABEL_OUTLINED)]),
                            ]
                        ),
                        ft.Divider(height=1, color="#EEEEEE"),
                        ft.Text("Descripción", size=18, weight="bold", color="#000000"),
                        ft.Text(prenda.get("descripcion") or "Sin descripción proporcionada.", size=16, color="#444444"),
                        ft.Container(height=40),
                    ]
                )
            )
        ]
    )
