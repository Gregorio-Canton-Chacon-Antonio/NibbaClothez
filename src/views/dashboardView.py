import flet as ft
import os
import shutil
import uuid

CONDICION_LABELS = {
    "nuevo": "Nuevo",
    "como_nuevo": "Como nuevo",
    "usado_excelente": "Usado - Excelente",
    "usado_buen_estado": "Usado - Buen estado",
    "usado_aceptable": "Usado - Aceptable",
}


def DashboardView(page, prenda_controller):
    usuario_actual = getattr(page, "user_data", None)

    def notificar(texto):
        page.snack_bar = ft.SnackBar(ft.Text(texto, color=ft.Colors.WHITE), bgcolor="#333333")
        page.snack_bar.open = True
        page.update()

    fotos_lista = []
    texto_conteo = ft.Text("Fotos · 0 / 5", size=14, weight="bold", color="#000000")
    contenedor_fotos = ft.Row(spacing=10, scroll=ft.ScrollMode.AUTO)

    UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "img", "uploads")

    def ver_foto(img_path):
        def cerrar_dialogo(_):
            dialogo.open = False
            page.update()
        dialogo = ft.AlertDialog(
            content=ft.Image(src=img_path, fit="contain", border_radius=10),
            actions=[ft.TextButton("Cerrar", on_click=cerrar_dialogo)]
        )
        page.overlay.append(dialogo)
        dialogo.open = True
        page.update()

    def eliminar_foto(indice):
        fotos_lista.pop(indice)
        actualizar_galeria()

    def actualizar_galeria():
        contenedor_fotos.controls.clear()
        if len(fotos_lista) < 5:
            contenedor_fotos.controls.append(preview_imagen)
        
        for i, f_path in enumerate(fotos_lista):
            contenedor_fotos.controls.append(
                ft.Stack([
                    ft.Container(
                        width=120, height=120, border_radius=10,
                        content=ft.Image(src=f_path, fit="cover", width=120, height=120)
                    ),
                    ft.IconButton(
                        ft.Icons.EDIT_ROUNDED, icon_color="white",
                        bgcolor=ft.Colors.with_opacity(0.4, "black"),
                        left=-5, top=-5, icon_size=16,
                        on_click=lambda _, img=f_path: ver_foto(img)
                    ),
                    ft.IconButton(ft.Icons.CANCEL, icon_color="red", right=-5, top=-5, 
                                  on_click=lambda _, idx=i: eliminar_foto(idx))
                ])
            )
        texto_conteo.value = f"Fotos · {len(fotos_lista)} / 5"
        page.update()

    preview_imagen = ft.Container(
        width=120, height=120, border_radius=10,
        bgcolor="#F0F0F0", border=ft.border.all(1, "#CCCCCC"),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.CAMERA_ALT_ROUNDED, size=30, color="#555555"),
                ft.Text("Agregar fotos", size=10, color="#555555", weight="bold"),
            ],
        ),
    )

    file_picker = page.file_picker

    async def abrir_picker(_):
        restantes = 5 - len(fotos_lista)
        if restantes <= 0:
            notificar("Límite de 5 fotos alcanzado")
            return
            
        files = await file_picker.pick_files(
            allowed_extensions=["jpg", "jpeg", "png", "webp"], allow_multiple=True
        )
        if not files:
            return
            
        for f_obj in files[:restantes]:
            if f_obj.path:
                ext = os.path.splitext(f_obj.path)[1]
                nombre = f"{uuid.uuid4().hex}{ext}"
                destino = os.path.join(UPLOADS_DIR, nombre)
                shutil.copy2(f_obj.path, destino)
                fotos_lista.append(f"uploads/{nombre}")
        
        actualizar_galeria()

    preview_imagen.on_click = abrir_picker
    actualizar_galeria()

    def campo(label, expand=False, width=None, keyboard_type=None):
        return ft.TextField(
            label=label, expand=expand, width=width, border_radius=10, filled=True,
            bgcolor="#F5F5F5", border_color="#CCCCCC", focused_border_color="#000000",
            label_style=ft.TextStyle(color="#666666"), color="#000000",
            keyboard_type=keyboard_type,
        )

    input_titulo = campo("Título", expand=True)
    input_precio = campo("Precio", width=100, keyboard_type=ft.KeyboardType.NUMBER)
    input_talla = campo("Talla", expand=True)
    input_marca = campo("Marca", expand=True)
    input_descripcion = campo("Descripción", expand=True)

    select_condicion = ft.Dropdown(
        label="Condición", expand=True, border_radius=10,
        bgcolor="#F5F5F5", border_color="#CCCCCC", focused_border_color="#000000",
        label_style=ft.TextStyle(color="#666666"), color="#000000",
        options=[ft.dropdown.Option(k, text=v) for k, v in CONDICION_LABELS.items()],
        value="nuevo",
    )

    select_genero = ft.Dropdown(
        label="Género", expand=True, border_radius=10,
        bgcolor="#F5F5F5", border_color="#CCCCCC", focused_border_color="#000000",
        label_style=ft.TextStyle(color="#666666"), color="#000000",
        options=[
            ft.dropdown.Option("Hombres"),
            ft.dropdown.Option("Mujeres"),
            ft.dropdown.Option("Unisex"),
        ],
        value="Unisex",
    )

    select_categoria = ft.Dropdown(
        label="Categoría", expand=True, border_radius=10,
        bgcolor="#F5F5F5", border_color="#CCCCCC", focused_border_color="#000000",
        label_style=ft.TextStyle(color="#666666"), color="#000000",
        options=[
            ft.dropdown.Option("Ropa Superior"),
            ft.dropdown.Option("Ropa Inferior"),
            ft.dropdown.Option("Ropa Interior"),
            ft.dropdown.Option("Ropa Exterior"),
        ],
        value="Ropa Superior",
    )

    def nueva_prenda(e):
        if not (usuario_actual and input_titulo.value and input_precio.value and input_talla.value):
            notificar("Título, precio y talla son obligatorios")
            return
        
        foto_principal = fotos_lista[0] if fotos_lista else ""
        
        exito, mensaje = prenda_controller.guardar_nueva(
            usuario_actual["id_usuario"], input_titulo.value, input_precio.value,
            input_talla.value, select_condicion.value,
            input_marca.value or "Sin marca", input_descripcion.value or "",
            foto_principal, select_genero.value, select_categoria.value,
        )
        if exito:
            input_titulo.value = input_precio.value = input_talla.value = input_marca.value = input_descripcion.value = ""
            select_condicion.value = "nuevo"
            select_genero.value = "Unisex"
            select_categoria.value = "Ropa Superior"
            fotos_lista.clear()
            actualizar_galeria()
            notificar("¡Publicación creada exitosamente!")
            page.go("/casa")
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
                ft.IconButton(ft.Icons.CLOSE_ROUNDED, icon_color="#000000", on_click=lambda _: page.go("/casa")),
                ft.Text("Nueva publicación", size=16, weight="bold", color="#000000", expand=True, text_align="center"),
                ft.TextButton("Publicar", style=ft.ButtonStyle(color="#1877F2"), on_click=nueva_prenda),
            ],
        ),
    )

    seccion_fotos = ft.Container(
        padding=ft.padding.symmetric(horizontal=16, vertical=20),
        content=ft.Column(
            spacing=10,
            controls=[
                texto_conteo,
                contenedor_fotos,
                ft.Text("Las fotos ayudan a que los compradores vean el estado del artículo.", size=12, color="#666666"),
            ]
        )
    )

    formulario_campos = ft.Container(
        padding=ft.padding.symmetric(horizontal=16),
        content=ft.Column(
            spacing=15,
            controls=[
                input_titulo,
                input_precio,
                ft.Row(spacing=10, controls=[select_condicion, input_talla]),
                ft.Row(spacing=10, controls=[select_genero, select_categoria]),
                input_marca,
                input_descripcion,
            ]
        )
    )

    return ft.View(
        route="/dashboard",
        bgcolor="#FFFFFF",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            barra_superior,
            seccion_fotos,
            ft.Divider(height=1, color="#E0E0E0"),
            ft.Container(height=10),
            formulario_campos,
            ft.Container(height=20),
        ],
    )
