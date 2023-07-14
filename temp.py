import flet as ft
import pandas as pd


def main(page: ft.Page):
    page.session.set("data", pd.read_csv("D://chocolate_database.csv"))
    page.session.set("Data", None)
    data = page.session.get("data")
    page.add(
        ft.Text(data.REF[0])
    )


ft.app(target=main)
