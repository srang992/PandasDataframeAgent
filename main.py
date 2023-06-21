import flet as ft
from ionicons_python.extra_icons import chatgpt_icon
from ionicons_python.ionicons_icons import folder_open_outline_icon
from custom_flet.components.custom_icon import CustomIcon
from chat_tile import ChatTile
import pandas as pd
from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
import os
from time import sleep

if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

secret_key = os.getenv("OPENAI_API_KEY")

dataframe = None


def main(page: ft.Page):
    page.fonts = {
        "Product-Sans": "fonts/ProductSans-Regular.ttf"
    }
    page.title = "Pandas Dataframe Agent"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = ft.padding.only(top=20, bottom=20, left=10, right=10)

    message_field = ft.Ref[ft.TextField]()
    send_button = ft.Ref[ft.Icon]()
    send_button_container = ft.Ref[ft.Container]()
    chat = ft.Ref[ft.ListView]()
    overlay_container = ft.Ref[ft.Container]()

    def on_slash_click(e: ft.KeyboardEvent):
        if e.key == "/":
            message_field.current.focus()
        elif e.ctrl and e.shift and e.key == "D":
            page.splash = ft.ProgressBar()
            page.update()
            if os.path.exists("./uploads"):
                for file in os.listdir("./uploads"):
                    os.remove(f"./uploads/{file}")
            sleep(1)
            page.splash = None
            page.update()
            page.snack_bar = ft.SnackBar(
                ft.Text("Data Successfully Removed!", font_family="Product-Sans"),
                open=True
            )
        page.update()

    def on_send(_):
        global dataframe
        if not message_field.current.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Message Field is Empty!", font_family="Product-Sans"),
                open=True
            )
            page.update()
            return
        elif dataframe is None:
            page.snack_bar = ft.SnackBar(
                ft.Text("Choose a file first!", font_family="Product-Sans"),
                open=True
            )
            page.update()
            return
        else:
            chat.current.controls.append(
                ChatTile(
                    lead_image="images/my_image.jpg",
                    title_text="Subhradeep Rang",
                    subtitle_text=message_field.current.value
                )
            )
            message, message_field.current.value = message_field.current.value, ""
            page.splash = ft.ProgressBar()
            page.update()
            if len(chat.current.controls) != 0:
                overlay_container.current.visible = False
            send_button.current.color = ft.colors.with_opacity(0.5, ft.colors.GREY)
            send_button_container.current.disabled = True
            send_button_container.current.bgcolor = ft.colors.TRANSPARENT
            agent = create_pandas_dataframe_agent(
                OpenAI(
                    temperature=0,
                    openai_api_key=secret_key
                ),
                df=dataframe,
            )
            response = agent.run(message)
            chat.current.controls.append(
                ChatTile(
                    lead_image=chatgpt_icon,
                    title_text="ChatGPT",
                    subtitle_text=response
                )
            )
            page.splash = None
            page.update()

    def on_textfield_change(_):
        if not message_field.current.value:
            send_button.current.color = ft.colors.with_opacity(0.5, ft.colors.GREY)
            send_button_container.current.disabled = True
            send_button_container.current.bgcolor = ft.colors.TRANSPARENT
        else:
            send_button.current.color = ft.colors.WHITE
            send_button_container.current.disabled = False
            send_button_container.current.bgcolor = ft.colors.GREEN
        page.update()

    def on_open(_):
        global dataframe
        upload_list = []
        if file_open.result is not None and file_open.result.files is not None:
            for f in file_open.result.files:
                if len(os.listdir("./uploads")):
                    for file in os.listdir("./uploads"):
                        os.remove(f"./uploads/{file}")
                upload_list.append(
                    ft.FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )
            page.splash = ft.ProgressBar()
            page.update()
            file_open.upload(upload_list)
            sleep(1)
            page.splash = None
            chat.current.controls.clear()
            page.update()

            for file in os.listdir("./uploads"):
                dataframe = pd.read_csv(f"./uploads/{file}")

            page.snack_bar = ft.SnackBar(
                ft.Text("Data Successfully Loaded!", font_family="Product-Sans"), open=True
            )
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text("Process Terminated!", font_family="Product-Sans"), open=True
            )
        page.update()

    file_open = ft.FilePicker(on_result=on_open)

    page.overlay.append(file_open)
    page.on_keyboard_event = on_slash_click

    page.add(
        ft.Stack(
            [
                ft.ListView(
                    expand=True,
                    spacing=10,
                    width=900,
                    padding=10,
                    auto_scroll=True,
                    ref=chat
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            CustomIcon(
                                chatgpt_icon,
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
                    ref=overlay_container
                ),
            ],
            width=900,
            expand=True
        ),
        ft.Container(
            content=ft.Row(
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
                        on_change=on_textfield_change,
                        on_submit=on_send,
                        ref=message_field,
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
                        on_click=lambda _: file_open.pick_files(allowed_extensions=["csv"])
                    ),
                    ft.Container(
                        border_radius=6,
                        content=ft.Icon(
                            ft.icons.SEND_ROUNDED,
                            size=20,
                            color=ft.colors.with_opacity(0.5, ft.colors.GREY),
                            ref=send_button,
                            tooltip="Send Message"
                        ),
                        padding=5,
                        disabled=True,
                        bgcolor=ft.colors.TRANSPARENT,
                        ink=True,
                        on_click=on_send,
                        ref=send_button_container,
                    ),
                ],
            ),
            shadow=ft.BoxShadow(
                blur_radius=3,
                blur_style=ft.ShadowBlurStyle.OUTER,
                color=ft.colors.with_opacity(0.5, ft.colors.GREY)
            ),
            border_radius=8,
            width=900,
            padding=ft.padding.only(right=10),
        )
    )


ft.app(
    target=main,
    assets_dir="./assets",
    upload_dir="./uploads",
    view=ft.WEB_BROWSER,
    port=8600,
)
