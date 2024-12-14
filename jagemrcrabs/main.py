import asyncio

import gradio as gr

from footway_integration import process_image as pr_img

async def process_image(image):
    output = dict()
    for res in await pr_img(image):
        output[res.body_part] = [o.image_url for o in res.items if o.image_url]
    return [output]


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

