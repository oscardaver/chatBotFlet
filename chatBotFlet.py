import flet as ft
from huggingface_hub import InferenceClient

def main(page: ft.Page):
    # Configuración básica de la página
    page.title = "AI Chat Assistant"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1000
    page.window_height = 800
    page.window_resizable = True
    page.bgcolor = "#1a1a1a"
    page.padding = 0
    
    # Configuración del cliente
    client = InferenceClient(api_key="Token_huguingface_hub")
    messages = [{"role": "system", "content": "Eres un asistente útil, responde de forma corta y precisa"}]

    # Chat container con estilo mejorado
    chat = ft.ListView(
        expand=True,
        spacing=10,
        padding=20,
        auto_scroll=True,
    )

    # Campo de entrada mejorado
    user_input = ft.TextField(
        hint_text="Escribe tu mensaje aquí...",
        border_radius=30,
        bgcolor="#2d2d2d",
        color="white",
        border_color="transparent",
        cursor_color="white",
        min_lines=1,
        max_lines=3,
        expand=True,
        text_size=14,
        content_padding=ft.padding.all(20),
    )

    def create_message_bubble(text: str, is_user: bool):
        return ft.Container(
            content=ft.Text(
                text,
                size=14,
                color="white",
                weight=ft.FontWeight.W_400,
                selectable=True,
            ),
            padding=ft.padding.all(15),
            border_radius=20,
            bgcolor="#0078D4" if is_user else "#404040",
            margin=ft.margin.only(
                left=50 if is_user else 0,
                right=0 if is_user else 50,
            ),
            animate=ft.animation.Animation(300, "easeOut"),
        )

    def send_message(e):
        if not user_input.value:
            return

        user_text = user_input.value.strip()
        chat.controls.append(create_message_bubble(f"Tú: {user_text}", True))
        page.update()

        user_input.value = ""
        page.update()

        messages.append({"role": "user", "content": user_text})
        stream = client.chat.completions.create(
            model="microsoft/Phi-3.5-mini-instruct",
            messages=messages,
            max_tokens=500,
            stream=True
        )

        full_response = ""
        for chunk in stream:
            full_response += chunk.choices[0].delta.content

        chat.controls.append(create_message_bubble(f"Asistente: {full_response}", False))
        messages.append({"role": "assistant", "content": full_response})
        page.update()

    # Botón de envío estilizado
    send_button = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        icon_color="white",
        bgcolor="#0078D4",
        icon_size=20,
        tooltip="Enviar mensaje",
        on_click=send_message,
    )

    # Barra superior
    header = ft.Container(
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.CHAT_ROUNDED, color="white", size=24),
                ft.Text(
                    "Chat Assistant",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="white",
                ),
            ],
            spacing=10,
        ),
        padding=20,
        bgcolor="#2d2d2d",
    )

    # Contenedor de entrada
    input_container = ft.Container(
        content=ft.Row(
            [user_input, send_button],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.only(left=20, right=20, bottom=20, top=10),
        bgcolor="#1a1a1a",
    )

    # Estructura principal
    page.add(
        ft.Column(
            [
                header,
                ft.Container(
                    content=chat,
                    expand=True,
                    bgcolor="#1a1a1a",
                ),
                input_container,
            ],
            spacing=0,
            expand=True,
        )
    )

ft.app(target=main)