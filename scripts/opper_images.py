from opperai import Opper

from jagemrcrabs import image_processing as ip
from jagemrcrabs.settings import settings

opper = Opper(api_key=settings.opper_api_key)

image_path = "examples/malfoy.jpeg"
description_ = ip.describe_image(image_path)
print(f"Image description: {description_}")
for item in description_:
    footway_input = ip.convert_description_to_footway_input(item)
    print(f"Raw item description: {item}")
    print(f"Footway input: {footway_input}")

# Image description: The image shows a person giving a presentation in a dark room. The presenter is pointing at a screen displaying a visual related to artificial intelligence (AI). The screen has the text 'AI' and 'AI RORENGE' along with circuit-like graphics. Several people are seated, watching the presentation attentively.
