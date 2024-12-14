import asyncio

import gradio as gr

async def process_image(image):
    await asyncio.sleep(1)
    return [{
        "1": [image, image, image],
        "2": [image, image, image],
        "3": [image, image, image],
    }]


with gr.Blocks() as demo:
    images = gr.State([])
    image = gr.Image(sources=["upload", "clipboard"], type="filepath")
    submit_btn = gr.Button("Submit")
    submit_btn.click(process_image, [image], images)

    @gr.render(inputs=images)
    def render_count(imgs):
        if imgs:
            for cont_type, cont in imgs[0].items():
                with gr.Row():
                    gr.Markdown(f"### {cont_type}")
                with gr.Row():
                    gr.Gallery(cont, label="Images", preview=True)


demo.launch()

