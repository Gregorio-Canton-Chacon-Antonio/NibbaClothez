import flet as ft
import os
import base64

CONDICION_LABELS = {
    "nuevo": "Nuevo",
    "como_nuevo": "Como nuevo",
    "usado_excelente": "Usado - Excelente",
    "usado_buen_estado": "Usado - Buen estado",
    "usado_aceptable": "Usado - Aceptable",
}


def DashboardView(page, prenda_controller):
    usuario_actual = getattr(page, "user_data", None)
    lista_prendas = ft.Column(spacing=10)

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

    def abrir_editor(prenda):
        foto_edit = [prenda.get("foto", "")]

        preview_edit = ft.Container(
            width=320, height=160, border_radius=10,
            bgcolor="#F0F0F0", border=ft.border.all(1, "#CCCCCC"),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Image(src=prenda["foto"], fit="cover", width=320, height=160)
            if prenda.get("foto") else ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.ADD_PHOTO_ALTERNATE_ROUNDED, size=32, color="#AAAAAA"),
                    ft.Text("Toca para cambiar foto", size=11, color="#AAAAAA"),
                ],
            ),
        )

        async def cambiar_foto_edit(_):
            files = await page.file_picker.pick_files(
                allowed_extensions=["jpg", "jpeg", "png", "webp"], allow_multiple=False
            )
            if not files or not files[0].path:
                return
            import base64
            with open(files[0].path, "rb") as f:
                foto_edit[0] = base64.b64encode(f.read()).decode()
            preview_edit.content = ft.Image(src=foto_edit[0], fit="cover", width=320, height=160)
            preview_edit.update()

        preview_edit.on_click = cambiar_foto_edit

        def campo_edit(label, valor, expand=False, width=None, keyboard_type=None):
            tf = ft.TextField(
                label=label, value=str(valor) if valor else "",
                expand=expand, width=width, border_radius=10, filled=True,
                bgcolor="#F5F5F5", border_color="#CCCCCC", focused_border_color="#000000",
                label_style=ft.TextStyle(color="#666666"), color="#000000",
                keyboard_type=keyboard_type,
            )
            return tf

        e_titulo = campo_edit("Título", prenda["titulo"], expand=True)
        e_precio = campo_edit("Precio", prenda["precio"], width=100, keyboard_type=ft.KeyboardType.NUMBER)
        e_talla = campo_edit("Talla", prenda["talla"], width=80)
        e_marca = campo_edit("Marca", prenda.get("marca", ""), expand=True)
        e_descripcion = campo_edit("Descripción", prenda.get("descripcion", ""), expand=True)
        e_condicion = ft.Dropdown(
            label="Condición", width=160, border_radius=10,
            bgcolor="#F5F5F5", border_color="#CCCCCC", focused_border_color="#000000",
            label_style=ft.TextStyle(color="#666666"), color="#000000",
            options=[ft.dropdown.Option(k, text=v) for k, v in CONDICION_LABELS.items()],
            value=prenda.get("condicion", "nuevo"),
        )

        def cerrar_bs(_=None):
            bs.open = False
            page.update()

        bs = ft.BottomSheet(
            open=True,
            on_dismiss=cerrar_bs,
            content=ft.Container(
                padding=20, bgcolor="#FFFFFF",
                content=ft.Column(
                    tight=True, spacing=10, scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Editar prenda", size=16, weight="bold", color="#000000"),
                                ft.IconButton(ft.Icons.CLOSE_ROUNDED, icon_color="#000000",
                                              on_click=cerrar_bs),
                            ],
                        ),
                        preview_edit,
                        ft.Row(controls=[e_titulo]),
                        ft.Row(spacing=8, controls=[e_precio, e_talla, e_condicion]),
                        ft.Row(controls=[e_marca]),
                        ft.Row(controls=[e_descripcion]),
                        ft.ElevatedButton(
                            "Guardar cambios", height=42,
                            style=ft.ButtonStyle(
                                bgcolor="#000000", color="#FFFFFF",
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                            on_click=lambda _: guardar_edicion(),
                        ),
                    ],
                ),
            ),
        )

        def guardar_edicion():
            if not e_titulo.value or not e_precio.value or not e_talla.value:
                notificar("Título, precio y talla son obligatorios")
                return
            foto_nueva = foto_edit[0] if foto_edit[0] != prenda.get("foto", "") else None
            exito, msg = prenda_controller.editar_prenda(
                prenda["id_prenda"], e_titulo.value, e_precio.value,
                e_talla.value, e_condicion.value,
                e_marca.value or "Sin marca", e_descripcion.value or "",
                foto_nueva,
            )
            if exito:
                cerrar_bs()
                cargar_prendas()
            else:
                notificar(msg)

        page.overlay.append(bs)
        page.update()

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
                            ft.Container(
                                width=60, height=60, border_radius=8,
                                bgcolor="#F0F0F0",
                                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                content=ft.Image(src=prenda["foto"], fit="cover") if prenda.get("foto") else ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED_ROUNDED, color="#AAAAAA"),
                            ),
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
                                icon=ft.Icons.EDIT_ROUNDED, icon_color="#555555", icon_size=22,
                                on_click=lambda e, p=prenda: abrir_editor(p),
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

    foto_path = [""]

    preview_imagen = ft.Container(
        width=358, height=180, border_radius=10,
        bgcolor="#F0F0F0", border=ft.border.all(1, "#CCCCCC"),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.ADD_PHOTO_ALTERNATE_ROUNDED, size=36, color="#AAAAAA"),
                ft.Text("Toca para agregar foto", size=12, color="#AAAAAA"),
            ],
        ),
    )

    file_picker = page.file_picker

    async def abrir_picker(_):
        files = await file_picker.pick_files(
            allowed_extensions=["jpg", "jpeg", "png", "webp"], allow_multiple=False
        )
        if not files:
            return
        src = files[0].path
        if not src:
            return
        with open(src, "rb") as f:
            foto_path[0] = base64.b64encode(f.read()).decode()
        preview_imagen.content = ft.Image(src=foto_path[0], fit="cover", width=358, height=180)
        preview_imagen.update()

    preview_imagen.on_click = abrir_picker

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
            input_marca.value or "Sin marca", input_descripcion.value or "",
            foto_path[0],
        )
        if exito:
            input_titulo.value = input_precio.value = input_talla.value = input_marca.value = input_descripcion.value = ""
            select_condicion.value = "nuevo"
            foto_path[0] = ""
            preview_imagen.content = ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.ADD_PHOTO_ALTERNATE_ROUNDED, size=36, color="#AAAAAA"),
                    ft.Text("Toca para agregar foto", size=12, color="#AAAAAA"),
                ],
            )
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
                ft.Text(f"Que vamos a vender hoy? ", size=18, weight="bold", color="#000000"),
                ft.Row(
                    spacing=4,
                    controls=[
                ft.IconButton(ft.Icons.HOME_ROUNDED, icon_color="#000000", on_click=lambda _: page.go("/casa")),
                ft.IconButton(ft.Icons.PERSON_ROUNDED, icon_color="#000000", on_click=lambda _: page.go("/perfil")),
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
                preview_imagen,
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
        scroll=ft.ScrollMode.AUTO,
        controls=[
            barra_superior,
            ft.Container(
                padding=16,
                content=ft.Column(
                    spacing=12,
                    controls=[
                        formulario_prenda,
                        ft.Text("Mis prendas", size=15, weight="bold", color="#000000"),
                        lista_prendas,
                    ],
                ),
            ),
        ],
    )
