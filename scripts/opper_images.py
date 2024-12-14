from typing import Literal

from opperai import Opper
from opperai.types import ImageInput
from pydantic import BaseModel

from jagemrcrabs.settings import settings

opper = Opper(api_key=settings.opper_api_key)

class FootwayInput(BaseModel):
    vendors: Literal[
        "Gant",
        "Birkenstock",
        "Tommy Jeans",
        "Kappa",
        "None",
    ]
    departments: Literal[
        "Women",
        "Men",
        "Children",
        "None"
    ]
    product_groups: Literal[
        "2 & 3 Piece Sets",
        "Accessories",
        "Alpine",
        "Ankle Socks",
        "Bags",
        "Balls",
        "Base Layers",
        "Basketball Shoes",
        "Bath Textiles",
        "Beanies",
        "Beauty",
        "Belts",
        "Blazers",
        "Bodies & Jumpsuits",
        "Bomber",
        "Books",
        "Boots",
        "Bottles & Flasks",
        "Bottoms",
        "Boxers",
        "Caps",
        "Cardigan",
        "Cargo Pants",
        "Chinos",
        "Clothing",
        "Coats",
        "Contact Lenses",
        "Crew Necks",
        "Dampeners",
        "Decoration",
        "Denim",
        "Denim Jeans",
        "Dress Shoes",
        "Electronics",
        "Equestrian",
        "Equipment",
        "Espadrille",
        "Everyday Shoes",
        "Eye Drops",
        "Eyewear",
        "Facial Care",
        "Flats",
        "Fleece & Sherpa",
        "Football Shoes",
        "Gift Set",
        "Gloves",
        "Golf Shoes",
        "Grips",
        "Haircare",
        "Hats & Caps",
        "Hats & Gloves",
        "Headbands",
        "Headwear & Scarves",
        "Heels",
        "Helmets",
        "High Boots & Ankle Boots",
        "High Top Shoes",
        "Hiking Equipment",
        "Hiking Shoes",
        "Home",
        "Hoodies",
        "Hoodies & Sweaters",
        "Hoodies & Sweatshirts",
        "Jackets",
        "Jersey",
        "Jewellery",
        "Jumpsuits & Rompers",
        "Knits",
        "Knitwear",
        "Leather Insoles",
        "Leggings",
        "Leisure Shoes",
        "Lens Solution",
        "Life Vests",
        "Loafer",
        "Long Sleeve",
        "Loungwear",
        "Low Top Shoes",
        "Low-Shoe",
        "Maternity",
        "Mid Top Shoes",
        "Nicotine Pouches",
        "Other Accessories",
        "Outdoor Shoes",
        "Outerwear",
        "Panties",
        "Pants",
        "Parkas Jacket",
        "Phone Case",
        "Pike",
        "Polo Shirts",
        "Polos",
        "Poloshirts",
        "Protective Gear",
        "Puffer",
        "Rackets",
        "Rainwear",
        "Reading Glasses",
        "Roller Skates",
        "Romper & Overall",
        "Rubber Boots",
        "Running Shoes",
        "Safety Shoes",
        "Sandals & Slippers",
        "Scarves & Gloves",
        "Shirts",
        "Shoe Accessories",
        "Shoe Care",
        "Shoes",
        "Short Sleeve",
        "Shorts",
        "Shorts & Skirts & Dresses",
        "Skis",
        "Sleepwear",
        "Slides",
        "Slippers",
        "Sneakers",
        "Sneakers & Sport Shoes",
        "Socks",
        "Sport Bras",
        "Sport Shoes",
        "Sports Bras",
        "Sports Shoes",
        "Sticks & Clubs",
        "Stops",
        "Strings",
        "Sunglasses",
        "Sweatpants",
        "Sweatshirts",
        "Swimshorts",
        "Swimwear",
        "T-Shirts",
        "Tanktops",
        "Technical & Shell",
        "Textile Care",
        "Tights & Leggings",
        "Tops",
        "Toys & Games",
        "Tracksuits & Overalls",
        "Training Equipment",
        "Training Shoes",
        "Trousers",
        "Underwear",
        "Varsity & Letterman",
        "Vests",
        "Walking Shoes",
        "Watches",
        "Water Bottles",
        "Winter Boots",
        "Wristbands",
        "Zip Hoodies",
        "None",
    ]
    product_types: Literal[
        "Apparels",
        "Shoes",
        "Accessories & Equipment",
        "Beauty",
        "Contact Lenses",
        "Consumable",
        "Health",
        "None",
    ]


class ImageOutput(BaseModel):
    color: str
    body_part: str
    item_description: str


def convert_description_to_footway_input(description: ImageOutput) -> FootwayInput:
    footway_input, response = opper.call(
        name="convert_description_to_footway_input",
        instructions="Convert a description of a clothing item to Footway input",
        output_type=FootwayInput,
        input=description,
    )

    return footway_input


def describe_image(path: str) -> list[ImageOutput]:
    description, response = opper.call(
        name="describe_image",
        instructions="You are a designer of a casual cosplay costume. " 
                     "Give a list of potential clothing items that could be inspired by the image. "
                     "Clothing items should be easily obtainable and not too expensive. "
                     "Costume should be more inspired by the image than a direct copy.",
        output_type=list[ImageOutput],
        input=ImageInput.from_path(path),
        model="openai/gpt-4o",
    )

    return description

image_path = "examples/malfoy.jpeg"
description_ = describe_image(image_path)
print(f"Image description: {description_}")
for item in description_:
    footway_input = convert_description_to_footway_input(item)
    print(f"Raw item description: {item}")
    print(f"Footway input: {footway_input}")


# Image description: The image shows a person giving a presentation in a dark room. The presenter is pointing at a screen displaying a visual related to artificial intelligence (AI). The screen has the text 'AI' and 'AI RORENGE' along with circuit-like graphics. Several people are seated, watching the presentation attentively.
