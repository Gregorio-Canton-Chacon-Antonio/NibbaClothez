import flet as ft


CONDICION_LABELS = {
    "nuevo": "Nuevo",
    "como_nuevo": "Como nuevo",
    "usado_excelente": "Usado - Excelente",
    "usado_buen_estado": "Usado - Buen estado",
    "usado_aceptable": "Usado - Aceptable",
}

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
            # Imagen Principal (Estilo Marketplace)
            ft.Container(
                height=400,
                bgcolor="#F5F5F5",
                content=ft.Image(
                    src=prenda["foto"],
                    fit="contain",
                    width=page.window.width
                ) if prenda.get("foto") else ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED_ROUNDED, size=100, color="#CCCCCC")
            ),
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