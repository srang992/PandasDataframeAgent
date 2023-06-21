import flet as ft


class ChatTile(ft.ListTile):
    def __init__(self, lead_image, title_text, subtitle_text):
        super().__init__()
        self.leading = ft.Image(
            src=lead_image,
            width=36,
            height=36,
            border_radius=35,
        )
        self.title = ft.Text(
            title_text,
            font_family="Product-Sans",
            style=ft.TextThemeStyle.TITLE_SMALL,
            size=16,
            weight=ft.FontWeight.W_700
        )
        self.subtitle = ft.Text(
            subtitle_text,
            font_family="Product-Sans",
            style=ft.TextThemeStyle.BODY_MEDIUM,
            size=15,
            selectable=True
        )
        self.disabled = True
