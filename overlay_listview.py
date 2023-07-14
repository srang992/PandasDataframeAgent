import flet as ft
from custom_flet.components.custom_icon import CustomIcon
from flet import Ref


class OverlayListView(ft.Stack):
    def __init__(
            self,
            ref_listview: Ref,
            ref_overlay: Ref,
    ):
        super().__init__()
        self.expand = True
        self.width = 900
        self.controls = [
            ft.ListView(
                expand=True,
                spacing=20,
                padding=10,
                width=900,
                auto_scroll=True,
                ref=ref_listview
            ),
            ft.Container(
                content=ft.Column(
                    [
                        CustomIcon(
                            "/images/agent_logo.svg",
                            size=100,
                            color=ft.colors.with_opacity(0.6, "grey"),
                        ),
                        ft.Text(
                            "Choose a file and let's start talking.",
                            size=17,
                            font_family="Product-Sans",
                            color=ft.colors.with_opacity(0.6, "grey")
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                alignment=ft.alignment.center,
                visible=True,
                ref=ref_overlay
            ),
        ]
