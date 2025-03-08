import gradio as gr
from deep_translator import GoogleTranslator

def translate_text(text, lang):
    if not text.strip():
        return "Please enter some text to translate."
    
    try:
        translated = GoogleTranslator(source="auto", target=lang).translate(text)
        return translated
    except Exception as e:
        return f"Error: {e}"

# Available languages
languages = {
    "French 🇫🇷": "fr",
    "Spanish 🇪🇸": "es",
    "German 🇩🇪": "de",
    "Chinese 🇨🇳": "zh-CN",
    "Japanese 🇯🇵": "ja",
    "Arabic 🇸🇦": "ar",
    "Hindi 🇮🇳": "hi",
    "Portuguese 🇵🇹": "pt",
    "Russian 🇷🇺": "ru"
}

# Gradio UI
interface = gr.Interface(
    fn=translate_text,
    inputs=[
        gr.Textbox(lines=3, placeholder="Enter text here...", label="Input Text"),
        gr.Dropdown(choices=list(languages.values()), label="Select Language"),
    ],
    outputs=gr.Textbox(label="Translated Text"),
    title="Language Translator",
    description="Enter text and select a language to translate.",
    theme="compact"
)

# Launch the app
interface.launch()