import flet as ft


class ChatTile(ft.Row):
    def __init__(self, lead_image, title_text, subtitle_text):
        super().__init__()
        self.width = 900,
        self.vertical_alignment = ft.CrossAxisAlignment.START
        self.controls = [
            ft.Image(
                src=lead_image,
                width=36,
                height=36,
                border_radius=35,
            ),
            ft.Column(
                [
                    ft.Text(
                        title_text,
                        font_family="Product-Sans",
                        style=ft.TextThemeStyle.TITLE_SMALL,
                        size=15,
                        weight=ft.FontWeight.W_700
                    ),
                    ft.Markdown(
                        subtitle_text,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                        code_theme="atelier-savanna-light",
                        code_style=ft.TextStyle(
                            font_family="Product-Sans",
                            size=15,
                            weight=ft.FontWeight.W_500
                        ),
                        selectable=True,
                    )
                ],
                spacing=2,
                expand=True
            )
        ]
