import flet as ft


def custom_snackbar(msg):
    return ft.SnackBar(
        content=ft.Text(msg, font_family="Product-Sans"),
        open=True
    )
