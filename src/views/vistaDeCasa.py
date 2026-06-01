import flet as ft


def VistaDeCasa(page: ft.Page):

    subcategorias = ["Ropa Superior", "Ropa Inferior", "Ropa Exterior", "Ropa Interior"]

    def make_subcategoria_btn(nombre, genero):
        return ft.Container(
            padding=ft.padding.only(left=20, top=7, bottom=7),
            border_radius=6,
            ink=True,
            content=ft.Text(nombre, size=12, color="#444444"),
            on_click=lambda _: page.go(f"/categoria/{genero}/{nombre}"),
        )

    def make_categoria_item(nombre):
        sub_col = ft.Column(
            visible=False,
            spacing=0,
            controls=[make_subcategoria_btn(s, nombre) for s in subcategorias],
        )

        def toggle_sub(_):
            sub_col.visible = not sub_col.visible
            page.update()

        arrow = ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED, size=16, color="#555555")

        header = ft.Container(
            padding=ft.padding.symmetric(horizontal=8, vertical=10),
            border_radius=8,
            ink=True,
            on_click=toggle_sub,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[ft.Text(nombre, size=13, color="#222222"), arrow],
            ),
        )
        return ft.Column(spacing=0, controls=[header, sub_col])

    items_menu = [
        ft.Text("Categorías", size=13, weight="bold", color="#000000"),
        ft.Divider(height=8, color="#DDDDDD"),
        make_categoria_item("Hombres"),
        make_categoria_item("Mujeres"),
    ]

    drawer_panel = ft.Container(
        visible=False,
        width=220,
        bgcolor="#F8F8F8",
        border=ft.border.only(right=ft.BorderSide(1, "#DDDDDD")),
        padding=ft.padding.symmetric(horizontal=12, vertical=16),
        content=ft.Column(spacing=4, controls=items_menu),
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

    precio_label = ft.Text("Cualquiera", size=11, color="#444444")

    min_input = ft.TextField(
        label="Mínimo", width=110, height=42, border_radius=8,
        filled=True, bgcolor="#F5F5F5", border_color="#CCCCCC",
        focused_border_color="#000000",
        label_style=ft.TextStyle(color="#666666", size=11),
        text_style=ft.TextStyle(color="#000000", size=12),
        keyboard_type=ft.KeyboardType.NUMBER,
        content_padding=ft.padding.symmetric(horizontal=8, vertical=4),
    )
    max_input = ft.TextField(
        label="Máximo", width=110, height=42, border_radius=8,
        filled=True, bgcolor="#F5F5F5", border_color="#CCCCCC",
        focused_border_color="#000000",
        label_style=ft.TextStyle(color="#666666", size=11),
        text_style=ft.TextStyle(color="#000000", size=12),
        keyboard_type=ft.KeyboardType.NUMBER,
        content_padding=ft.padding.symmetric(horizontal=8, vertical=4),
    )

    def aplicar_precio(e):
        mn = min_input.value.strip()
        mx = max_input.value.strip()
        if mn or mx:
            precio_label.value = f"${mn or '0'} - ${mx or '∞'}" 
        else:
            precio_label.value = "Cualquiera"
        precio_label.update()
        dialogo_precio.open = False
        page.update()

    def limpiar_precio(e):
        min_input.value = ""
        max_input.value = ""
        precio_label.value = "Cualquiera"
        precio_label.update()
        dialogo_precio.open = False
        page.update()

    dialogo_precio = ft.AlertDialog(
        modal=True,
        title=ft.Text("Rango de precio", size=15, weight="bold", color="#000000"),
        content=ft.Row(spacing=8, controls=[min_input, ft.Text("-", color="#888888"), max_input]),
        actions=[
            ft.TextButton("Limpiar", style=ft.ButtonStyle(color="#888888"), on_click=limpiar_precio),
            ft.ElevatedButton(
                "Aplicar",
                style=ft.ButtonStyle(
                    bgcolor="#000000", color="#FFFFFF",
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                on_click=aplicar_precio,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.overlay.append(dialogo_precio)

    def abrir_precio(_):
        dialogo_precio.open = True
        page.update()

    precio_btn = ft.Container(
        height=38,
        border_radius=10,
        bgcolor="#F0F0F0",
        border=ft.border.all(1, "#DDDDDD"),
        padding=ft.padding.symmetric(horizontal=10),
        ink=True,
        on_click=abrir_precio,
        content=ft.Row(
            spacing=4,
            tight=True,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.ATTACH_MONEY_ROUNDED, size=14, color="#555555"),
                precio_label,
                ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED, size=14, color="#555555"),
            ],
        ),
    )

    barra_busqueda = ft.Row(
        spacing=8,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.TextField(
                hint_text="Buscar...",
                height=38,
                border_radius=10,
                filled=True,
                expand=True,
                bgcolor="#F0F0F0",
                border_color="#DDDDDD",
                focused_border_color="#000000",
                hint_style=ft.TextStyle(color="#AAAAAA", size=13),
                text_style=ft.TextStyle(color="#000000", size=13),
                prefix_icon=ft.Icons.SEARCH_ROUNDED,
                content_padding=ft.padding.symmetric(horizontal=10, vertical=6),
            ),
            precio_btn,
        ],
    )

    return ft.View(
        route="/casa",
        bgcolor="#FFFFFF",
        scroll=ft.ScrollMode.AUTO,
        padding=ft.padding.symmetric(horizontal=16, vertical=16),
        controls=[
            navbar,
            barra_busqueda,
            drawer_panel,
        ],
    )
