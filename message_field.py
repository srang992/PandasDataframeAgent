import flet as ft
from ionicons_python.ionicons_icons import folder_open_outline_icon


class MessageField(ft.Container):

    def __init__(
            self,
            ref_message_field,
            ref_send_button,
            ref_send_button_container,
            on_field_change,
            on_press_enter,
            on_file_open,
            on_click_send,
    ):
        super().__init__()
        self.content = ft.Row(
            [
                ft.TextField(
                    hint_text="Start typing...",
                    text_style=ft.TextStyle(
                        font_family="Product-Sans",
                    ),
                    hint_style=ft.TextStyle(
                        font_family="Product-Sans",
                        color=ft.colors.with_opacity(0.5, ft.colors.GREY)
                    ),
                    border_color=ft.colors.TRANSPARENT,
                    max_lines=3,
                    expand=True,
                    on_change=on_field_change,
                    on_submit=on_press_enter,
                    ref=ref_message_field,
                ),
                ft.Container(
                    content=ft.Image(
                        src=folder_open_outline_icon,
                        width=24,
                        height=24,
                    ),
                    padding=8,
                    border_radius=35,
                    ink=True,
                    tooltip="Choose a File",
                    on_click=on_file_open
                ),
                ft.Container(
                    border_radius=6,
                    content=ft.Icon(
                        ft.icons.SEND_ROUNDED,
                        size=20,
                        color=ft.colors.with_opacity(0.5, ft.colors.GREY),
                        ref=ref_send_button,
                        tooltip="Send Message"
                    ),
                    padding=5,
                    disabled=True,
                    bgcolor=ft.colors.TRANSPARENT,
                    ink=True,
                    on_click=on_click_send,
                    ref=ref_send_button_container,
                ),
            ]
        )
        self.shadow = ft.BoxShadow(
            blur_radius=3,
            blur_style=ft.ShadowBlurStyle.OUTER,
            color=ft.colors.with_opacity(0.5, ft.colors.GREY)
        )
        self.border_radius = 8
        self.width = 900
        self.padding = ft.padding.only(right=10)
