import flet as ft
from ionicons_python.extra_icons import chatgpt_icon
from overlay_listview import OverlayListView
from message_field import MessageField
from chat_tile import ChatTile
import pandas as pd
import os
from snack_bar import custom_snackbar
from ask_lazypandas import ask_lazy_pandas
from time import sleep

if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

secret_key = os.getenv("OPENAI_API_KEY")


async def main(page: ft.Page):
    page.fonts = {
        "Product-Sans": "fonts/ProductSans-Regular.ttf"
    }
    page.title = "Pandas Dataframe Agent"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = ft.padding.only(top=20, bottom=20, left=10, right=10)
    if page.session.contains_key("data"):
        await page.session.set("data", None)

    message_field = ft.Ref[ft.TextField]()
    send_button = ft.Ref[ft.Icon]()
    send_button_container = ft.Ref[ft.Container]()
    chat = ft.Ref[ft.ListView]()
    overlay_container = ft.Ref[ft.Container]()

    async def on_slash_click(e: ft.KeyboardEvent):
        if e.key == "/":
            await message_field.current.focus_async()
        await page.update_async()

    async def on_send(_):
        # getting data from the session
        data = page.session.get("data")

        # check if the message field is empty
        if not message_field.current.value:
            await page.show_snack_bar_async(
                snack_bar=custom_snackbar("Message Field is Empty!")
            )
            await page.update_async()
            return

        # check if any file is selected
        elif data is None:
            await page.show_snack_bar_async(
                snack_bar=custom_snackbar("Choose File First!")
            )
            await page.update_async()
            return

        # if everything is fine, send the message to the chatgpt
        else:
            # adding user message to the list
            chat.current.controls.append(
                ChatTile(
                    lead_image="images/my_image.jpg",
                    title_text="Subhradeep Rang",
                    subtitle_text=message_field.current.value
                )
            )

            # resetting the value of the textfield and saving the user text in another variable
            message, message_field.current.value = message_field.current.value, ""

            # here the main process begins
            page.splash = ft.ProgressBar()

            # resetting the textfield elements after adding the user message to the list
            if len(chat.current.controls) != 0:
                overlay_container.current.visible = False
                send_button.current.color = ft.colors.with_opacity(0.5, ft.colors.GREY)
                send_button_container.current.disabled = True
                send_button_container.current.bgcolor = ft.colors.TRANSPARENT
            await page.update_async()

            # sending message to the model
            response = ask_lazy_pandas(message, data, secret_key)

            # adding the response of the model in the list
            chat.current.controls.append(
                ChatTile(
                    lead_image=chatgpt_icon,
                    title_text="ChatGPT",
                    subtitle_text=response
                )
            )

            page.splash = None
            await page.update_async()

    async def on_textfield_change(_):
        if not message_field.current.value:
            send_button.current.color = ft.colors.with_opacity(0.5, ft.colors.GREY)
            send_button_container.current.disabled = True
            send_button_container.current.bgcolor = ft.colors.TRANSPARENT
        else:
            send_button.current.color = ft.colors.WHITE
            send_button_container.current.disabled = False
            send_button_container.current.bgcolor = ft.colors.GREEN
        await page.update_async()

    async def on_open(_):
        upload_list = []
        if os.path.exists("./uploads"):
            if len(os.listdir("./uploads")):
                for file in os.listdir("./uploads"):
                    os.remove(f"./uploads/{file}")
        if file_open.result is not None and file_open.result.files is not None:
            for f in file_open.result.files:
                upload_list.append(
                    ft.FilePickerUploadFile(
                        f.name,
                        upload_url=await page.get_upload_url_async(f.name, 600),
                    )
                )
            page.splash = ft.ProgressBar()
            await page.update_async()
            await file_open.upload_async(upload_list)
            sleep(1)
            page.splash = None
            chat.current.controls.clear()
            overlay_container.current.visible = True
            await page.update_async()
            for file in os.listdir("./uploads"):
                page.session.set("data", pd.read_csv(f"./uploads/{file}"))
            await page.show_snack_bar_async(
                snack_bar=custom_snackbar("Data Successfully Loaded!")
            )
        else:
            await page.show_snack_bar_async(
                snack_bar=custom_snackbar("Process Terminated!")
            )
        await page.update_async()

    async def open_file(_):
        await file_open.pick_files_async(allowed_extensions=["csv"])

    file_open = ft.FilePicker(on_result=on_open)

    page.overlay.append(file_open)
    page.on_keyboard_event = on_slash_click

    await page.add_async(
        ft.SafeArea(
            content=ft.Column(
                [
                    OverlayListView(
                        ref_listview=chat,
                        ref_overlay=overlay_container,
                    ),
                    MessageField(
                        ref_message_field=message_field,
                        ref_send_button=send_button,
                        ref_send_button_container=send_button_container,
                        on_file_open=open_file,
                        on_click_send=on_send,
                        on_press_enter=on_send,
                        on_field_change=on_textfield_change,
                    ),
                ],
            ),
            expand=True
        ),
    )


ft.app(
    target=main,
    assets_dir="assets",
    upload_dir="uploads",
    view=ft.AppView.WEB_BROWSER,
    port=8655,
)
