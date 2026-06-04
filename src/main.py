import flet as ft
import traceback
from database.init_db import init_db
from controllers.UserController import AuthController
from controllers.PrendaController import PrendaController
from views.LoginView import LoginView
from views.dashboardView import DashboardView
from views.RegistroView import RegistroView
from views.UserView import PerfilView
from views.RecuperarView import RecuperarView
from views.vistaDeCasa import VistaDeCasa
from views.PrendaDetalleView import PrendaDetalleView
from views.PerfilVendedorView import PerfilVendedorView


async def start(page: ft.Page):
    page.title = "Nibba Clothez"
    page.window.width = 430
    page.window.height = 720
    page.window.min_width = 430
    page.window.max_width = 430
    page.window.min_height = 720
    page.window.max_height = 720
    page.window.resizable = False
    page.window.title_bar_hidden = False
    page.update()
    await page.window.center()
    page.update()

    auth_ctrl = AuthController()
    prenda_ctrl = PrendaController()

    file_picker = ft.FilePicker()
    page.services.append(file_picker)
    page.file_picker = file_picker
    page.update()

    def route_change(e):
        try:
            page.views.clear()
            if page.route == "/casa":
                page.views.append(VistaDeCasa(page, prenda_ctrl))
            elif page.route == "/":
                page.views.append(LoginView(page, auth_ctrl))
            elif page.route == "/dashboard":
                page.views.append(DashboardView(page, prenda_ctrl))
            elif page.route == "/registro":
                page.views.append(RegistroView(page, auth_ctrl))
            elif page.route == "/perfil":
                page.views.append(PerfilView(page, auth_ctrl, prenda_ctrl))
            elif page.route == "/recuperar":
                page.views.append(RecuperarView(page, auth_ctrl))
            elif page.route == "/prenda":
                page.views.append(PrendaDetalleView(page, auth_ctrl))
            elif page.route == "/perfil_vendedor":
                page.views.append(PerfilVendedorView(page, prenda_ctrl))
            page.update()
        except Exception:
            traceback.print_exc()

    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            page.update()
            page.go(page.views[-1].route)

    def on_error(e):
        traceback.print_exc()
        # Mostramos el error en un SnackBar para que sea visible al usuario
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Error: {e.data}", color=ft.Colors.WHITE),
            bgcolor=ft.Colors.RED_700,
            action="Cerrar"
        )
        page.snack_bar.open = True
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.on_error = on_error

    page.go("/casa")


def main():
    import os
    assets = os.path.join(os.path.dirname(__file__), "..", "img")
    ft.app(target=start, assets_dir=assets)


if __name__ == "__main__":
    main()