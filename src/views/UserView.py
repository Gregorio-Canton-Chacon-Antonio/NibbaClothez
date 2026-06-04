import flet as ft
import base64

CONDICION_LABELS = {
    "nuevo": "Nuevo",
    "como_nuevo": "Como nuevo",
    "usado_excelente": "Usado - Excelente",
    "usado_buen_estado": "Usado - Buen estado",
    "usado_aceptable": "Usado - Aceptable",
}


def PerfilView(page, auth_controller, prenda_controller):
    datos = getattr(page, "user_data", None) or {}
    lista_prendas = ft.Column(spacing=10)

    def cerrar_sesion(e):
        def confirmar_salida(_):
            page.user_data = None
            dialogo_confirmacion.open = False
            page.update()
            page.go("/")

        def cancelar_salida(_):
            dialogo_confirmacion.open = False
            page.update()

        dialogo_confirmacion = ft.AlertDialog(
            modal=True,
            title=ft.Text("Cerrar sesión", size=18, weight="bold"),
            content=ft.Text("¿Estas seguro de que quieres salir de la cuenta?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar_salida),
                ft.ElevatedButton(
                    "Sí, salir", 
                    bgcolor=ft.Colors.RED_700, 
                    color=ft.Colors.WHITE,
                    on_click=confirmar_salida
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dialogo_confirmacion)
        dialogo_confirmacion.open = True
        page.update()

    def notificar(texto):
        page.snack_bar = ft.SnackBar(ft.Text(texto, color=ft.Colors.WHITE), bgcolor="#333333")
        page.snack_bar.open = True
        page.update()

    def borrar(id_prenda):
        exito, mensaje = prenda_controller.eliminar_prenda(datos["id_usuario"], id_prenda)
        if exito:
            cargar_prendas()
        else:
            notificar(mensaje)

    def abrir_editor(prenda):
        foto_bytes_edit = [None]  # None = sin cambios
        fotos_actuales = [f for f in (prenda.get("foto") or "").split("|") if f]

        preview_edit = ft.Container(
            width=320, height=160, border_radius=10,
            bgcolor="#F0F0F0", border=ft.border.all(1, "#CCCCCC"),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Image(src=fotos_actuales[0], fit="cover", width=320, height=160)
            if fotos_actuales else ft.Column(
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
            with open(files[0].path, "rb") as f:
                raw = f.read()
            foto_bytes_edit[0] = raw
            b64 = "data:image/jpeg;base64," + base64.b64encode(raw).decode()
            preview_edit.content = ft.Image(src=b64, fit="cover", width=320, height=160)
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
            nuevas_fotos = [foto_bytes_edit[0]] if foto_bytes_edit[0] is not None else None
            exito, msg = prenda_controller.editar_prenda(
                datos["id_usuario"], prenda["id_prenda"], e_titulo.value, e_precio.value,
                e_talla.value, e_condicion.value,
                e_marca.value or "Sin marca", e_descripcion.value or "",
                nuevas_fotos,
            )
            if exito:
                cerrar_bs()
                cargar_prendas()
            else:
                notificar(msg)

        page.overlay.append(bs)
        page.update()

    def cargar_prendas():
        if not (datos and "id_usuario" in datos):
            return
        lista_prendas.controls.clear()
        prendas = prenda_controller.obtener_lista(datos["id_usuario"])
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
                        ft.IconButton(ft.Icons.LOGOUT_ROUNDED, icon_color="#000000", on_click=cerrar_sesion),
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
            ft.Container(
                padding=ft.padding.only(left=20, right=20, bottom=40),
                content=ft.Column([
                    ft.Text("Mis prendas", size=18, weight="bold", color="#000000"),
                    lista_prendas,
                ])
            ),
        ],
    )
