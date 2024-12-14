import random

import gradio as gr

with gr.Blocks() as demo:
    input_image = gr.Image(sources=["upload", "clipboard"], type="filepath")

    @gr.render(inputs=input_image)
    def predict(image):
        if not image:
            gr.Markdown("## No Input Provided")
        else:
            for body_part in random.choices(["head", "torso", "legs", "feet"], k=random.randint(3, 8)):
                with gr.Row():
                    gr.Markdown(f"### {body_part}")
                with gr.Row():
                    gr.Gallery([image, image, image], label="Images")

demo.launch()
