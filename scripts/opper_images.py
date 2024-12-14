from opperai import Opper
from opperai.types import ImageInput

from jagemrcrabs.settings import settings

opper = Opper(api_key=settings.opper_api_key)

def describe_image(path: str) -> str:
    description, response = opper.call(
        name="describe_image",
        instructions="Describe the content of the image",
        output_type=str,
        input=ImageInput.from_path(path),
        model="openai/gpt-4o",
    )
    return description

image_path = "examples/malfoy.jpeg"
description = describe_image(image_path)
print(f"Image description: {description}")
# Image description: The image shows a person giving a presentation in a dark room. The presenter is pointing at a screen displaying a visual related to artificial intelligence (AI). The screen has the text 'AI' and 'AI RORENGE' along with circuit-like graphics. Several people are seated, watching the presentation attentively.
