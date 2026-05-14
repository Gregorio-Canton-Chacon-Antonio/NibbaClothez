import flet as ft

CONDICION_LABELS = {
    "nuevo": "Nuevo",
    "como_nuevo": "Como nuevo",
    "usado_excelente": "Usado - Excelente",
    "usado_buen_estado": "Usado - Buen estado",
    "usado_aceptable": "Usado - Aceptable",
}


def DashboardView(page, prenda_controller):
    usuario_actual = getattr(page, "user_data", None)
    lista_prendas = ft.Column(scroll=ft.ScrollMode.ALWAYS, expand=True, spacing=10)

    def notificar(texto):
        notif = ft.SnackBar(ft.Text(texto, color=ft.Colors.WHITE), bgcolor="#333333", open=True)
        page.overlay.append(notif)
        page.update()

    def borrar(id_prenda):
        exito, mensaje = prenda_controller.eliminar_prenda(id_prenda)
        if exito:
            cargar_prendas()
        else:
            notificar(mensaje)

    def cargar_prendas():
        if not (usuario_actual and "id_usuario" in usuario_actual):
            return
        lista_prendas.controls.clear()
        prendas = prenda_controller.obtener_lista(usuario_actual["id_usuario"])
        for prenda in prendas:
            lista_prendas.controls.append(
                ft.Container(
                    padding=14, border_radius=12, bgcolor="#FFFFFF",
                    border=ft.border.all(1, "#E0E0E0"),
                    shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.with_opacity(0.08, "#000000"), offset=ft.Offset(0, 2)),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                spacing=4, expand=True,
                                controls=[
                                    ft.Text(prenda["titulo"], weight="bold", size=14, color="#000000"),
                                    ft.Text(f"${prenda['precio']} · Talla: {prenda['talla']}", size=12, color="#666666"),
                                    ft.Row(
                                        spacing=6,
                                        controls=[
                                            ft.Container(
                                                padding=ft.padding.symmetric(horizontal=8, vertical=3),
                                                border_radius=8, bgcolor="#F0F0F0",
                                                border=ft.border.all(1, "#CCCCCC"),
                                                content=ft.Text(CONDICION_LABELS.get(prenda.get("condicion", ""), prenda.get("condicion", "")), size=10, color="#333333", weight="bold"),
                                            ),
                                            ft.Container(
                                                padding=ft.padding.symmetric(horizontal=8, vertical=3),
                                                border_radius=8, bgcolor="#F0F0F0",
                                                border=ft.border.all(1, "#CCCCCC"),
                                                content=ft.Text(prenda.get("marca", "Sin marca"), size=10, color="#333333", weight="bold"),
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_ROUNDED, icon_color="#999999", icon_size=22,
                                on_click=lambda e, id=prenda["id_prenda"]: borrar(id),
                            ),
                        ],
                    ),
                )
            )
        page.update()

    cargar_prendas()

    def campo(label, expand=False, width=None, keyboard_type=None):
        return ft.TextField(
            label=label, expand=expand, width=width, border_radius=10, filled=True,
            bgcolor="#F5F5F5", border_color="#CCCCCC", focused_border_color="#000000",
            label_style=ft.TextStyle(color="#666666"), color="#000000",
            keyboard_type=keyboard_type,
        )

    input_titulo = campo("Título", expand=True)
    input_precio = campo("Precio", width=100, keyboard_type=ft.KeyboardType.NUMBER)
    input_talla = campo("Talla", width=80)
    input_marca = campo("Marca", expand=True)
    input_descripcion = campo("Descripción", expand=True)

    select_condicion = ft.Dropdown(
        label="Condición", width=160, border_radius=10,
        bgcolor="#F5F5F5", border_color="#CCCCCC", focused_border_color="#000000",
        label_style=ft.TextStyle(color="#666666"), color="#000000",
        options=[ft.dropdown.Option(k, text=v) for k, v in CONDICION_LABELS.items()],
        value="nuevo",
    )

    def nueva_prenda(e):
        if not (usuario_actual and input_titulo.value and input_precio.value and input_talla.value):
            notificar("Título, precio y talla son obligatorios")
            return
        exito, mensaje = prenda_controller.guardar_nueva(
            usuario_actual["id_usuario"], input_titulo.value, input_precio.value,
            input_talla.value, select_condicion.value,
            input_marca.value or "Sin marca", input_descripcion.value or ""
        )
        if exito:
            input_titulo.value = input_precio.value = input_talla.value = input_marca.value = input_descripcion.value = ""
            select_condicion.value = "nuevo"
            cargar_prendas()
        else:
            notificar(mensaje)

    nombre_usuario = usuario_actual["nombre"] if usuario_actual else "Usuario"

    barra_superior = ft.Container(
        padding=ft.padding.only(left=16, right=16, top=12, bottom=8),
        bgcolor="#FFFFFF",
        border=ft.border.only(bottom=ft.BorderSide(1, "#E0E0E0")),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text(f"Hola, {nombre_usuario} 👋", size=18, weight="bold", color="#000000"),
                ft.Row(
                    spacing=4,
                    controls=[
                        ft.IconButton(ft.Icons.PERSON_ROUNDED, icon_color="#000000", on_click=lambda _: page.go("/perfil")),
                        ft.IconButton(ft.Icons.LOGOUT_ROUNDED, icon_color="#000000", on_click=lambda _: page.go("/")),
                    ],
                ),
            ],
        ),
    )

    formulario_prenda = ft.Container(
        padding=16, border_radius=12, bgcolor="#FFFFFF",
        border=ft.border.all(1, "#E0E0E0"),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.with_opacity(0.08, "#000000"), offset=ft.Offset(0, 2)),
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Text("Nueva prenda", size=14, color="#000000", weight="bold"),
                ft.Row(spacing=8, controls=[input_titulo]),
                ft.Row(spacing=8, controls=[input_precio, input_talla, select_condicion]),
                ft.Row(spacing=8, controls=[input_marca]),
                ft.Row(spacing=8, controls=[input_descripcion]),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.ElevatedButton(
                            "Agregar", height=40,
                            style=ft.ButtonStyle(
                                bgcolor="#000000", color="#FFFFFF",
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                            on_click=nueva_prenda,
                        ),
                    ],
                ),
            ],
        ),
    )

    return ft.View(
        route="/dashboard",
        bgcolor="#F7F7F7",
        controls=[
            barra_superior,
            ft.Container(
                padding=16, expand=True,
                content=ft.Column(
                    expand=True, spacing=12,
                    controls=[
                        formulario_prenda,
                        ft.Text("Mis prendas", size=15, weight="bold", color="#000000"),
                        lista_prendas,
                    ],
                ),
            ),
        ],
    )
