import gradio as gr


def process_image(image):
    print(image)
    return image


demo = gr.Interface(
    fn=process_image,
    inputs=[gr.Image(sources=["upload", "clipboard"], type="filepath")],
    outputs=[gr.Image()],
    examples="./examples",
    theme=gr.themes.Citrus(),
)

demo.launch()