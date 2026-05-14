import flet as ft
import traceback
from controllers.UserController import AuthController
from controllers.PrendaController import PrendaController
from views.LoginView import LoginView
from views.dashboardView import DashboardView
from views.RegistroView import RegistroView
from views.UserView import PerfilView


def start(page: ft.Page):
    page.title = "Nibba Clothez"
    page.window_width = 420
    page.window_height = 700

    auth_ctrl = AuthController()
    prenda_ctrl = PrendaController()

    def route_change(e):
        try:
            page.views.clear()
            if page.route == "/":
                page.views.append(LoginView(page, auth_ctrl))
            elif page.route == "/dashboard":
                page.views.append(DashboardView(page, prenda_ctrl))
            elif page.route == "/registro":
                page.views.append(RegistroView(page, auth_ctrl))
            elif page.route == "/perfil":
                page.views.append(PerfilView(page, auth_ctrl))
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
        print("PAGE ERROR:", e.data)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.on_error = on_error

    if page.route == "/":
        route_change(None)
    else:
        page.go("/")


def main():
    ft.app(target=start)


if __name__ == "__main__":
    main()