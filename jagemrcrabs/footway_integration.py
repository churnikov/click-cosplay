import asyncio
from pprint import pprint

import aiohttp
from loguru import logger
from pydantic import BaseModel

import image_processing as ip
from jagemrcrabs.settings import settings


class FootwayItem(BaseModel):
    # merchantId: str
    # variantId: str
    productName: str
    # supplierModelNumber: str
    # ean: list[str]
    size: str
    # "price": null,
    # "product_description": null,
    vendor: str
    quantity: int
    productType: str
    productGroup: str
    department: str
    image_url: str


class FootwayResponse(BaseModel):
    items: list[FootwayItem]
    body_part: str


async def fetch(url, session, params=None) -> FootwayResponse:
    # Perform an HTTP GET request with query parameters
    body_part = params.pop("bodyPart")
    async with session.get(url, params=params, headers={"X-API-KEY": settings.footway_api_key}) as response:
        json = await response.json()
        items = []
        for item in json["items"]:
            items.append(
                FootwayItem(
                    productName=item["productName"] or "",
                    size=item["size"] or "",
                    vendor=item["vendor"],
                    quantity=item["quantity"],
                    productType=item["productType"][0] or "",
                    productGroup=item["productGroup"][0] or "",
                    department=item["department"][0] or "",
                    image_url=item["image_url"] or "",
                )
            )
        response = FootwayResponse(
            items=items,
            body_part= body_part
        )
        return response


async def fetch_all(url, params_list):
    async with aiohttp.ClientSession() as session:
        # Create tasks for all requests with different query parameters
        tasks = [fetch(url, session, params=params) for params in params_list]
        return await asyncio.gather(*tasks)


# Example URL
FOOTWAY_PLUS_API = "https://api.footwayplus.com/v1/inventory/search"


async def search_inventory(footway_input_list: list[ip.FootwayInput], body_parts: list[str]) -> [FootwayResponse]:
    params = []
    for i, footway_input in enumerate(footway_input_list):
        params.append(
            {
                "department": footway_input.departments if footway_input.departments != "None" else "",
                "productGroup": footway_input.product_groups,
                "productType": footway_input.product_types,
                "bodyPart": body_parts[i],
            }
        )
    return await fetch_all(FOOTWAY_PLUS_API, params)


async def process_image(image_path: str) -> list[FootwayResponse]:
    description_ = ip.describe_image(image_path)
    print(f"Image description: {description_}")
    footway_inputs = []
    body_parts = []

    for item in description_:
        footway_input = ip.convert_description_to_footway_input(item)
        footway_inputs.append(footway_input)
        body_parts.append(item.body_part)
        print(f"Raw item description: {item}")
        print(f"Footway input: {footway_input}")
        with open("cache.txt", "a") as f:
            f.write(item.body_part)
            f.write("\n")
            f.write(str(footway_input))
            f.write("\n")
            f.write("\n")

    # body_parts = ["upper body", "neck", "torso", "full_body"]
    #
    # footway_inputs = [
    #     ip.FootwayInput(vendors="None", departments="None", product_groups='Hoodies & Sweaters',
    #                     product_types='Apparels'),
    #     ip.FootwayInput(vendors="None", departments="None", product_groups='Other Accessories',
    #                     product_types='Apparels'),
    #     ip.FootwayInput(vendors="None", departments="None", product_groups='Shirts', product_types='Apparels'),
    #     ip.FootwayInput(vendors="None", departments="None", product_groups='Cardigan', product_types='Apparels'),
    # ]

    results = await search_inventory(footway_inputs, body_parts)
    for result in results:
        print(len(result.items))
    pprint(results)

 #    results = [FootwayResponse(items=[FootwayItem(productName='1373b-ow White', size='L', vendor='PAM', quantity=1, productType='Apparels', productGroup='T-Shirts', department='Men', image_url='https://images.footway.com/ca_images/1373B-OW_OW_1.png'), FootwayItem(productName='1908 All Star Knit Tunic Blue', size='130/140', vendor='Converse', quantity=1, productType='Apparels', productGroup='T-Shirts', department='Children', image_url='https://images.footway.com/sm_images/009328874607_001_308d369926ed43dfa7ad8ad8117da919.png'), FootwayItem(productName='1908 All Star Knit Tunic Blue', size='140/150', vendor='Converse', quantity=15, productType='Apparels', productGroup='T-Shirts', department='Children', image_url='https://images.footway.com/sm_images/009328874607_001_308d369926ed43dfa7ad8ad8117da919.png'), FootwayItem(productName='1908 All Star Knit Tunic Blue', size='150', vendor='Converse', quantity=10, productType='Apparels', productGroup='T-Shirts', department='Children', image_url='https://images.footway.com/sm_images/009328874607_001_308d369926ed43dfa7ad8ad8117da919.png'), FootwayItem(productName='1908 All Star Knit Tunic Blue', size='160/170', vendor='Converse', quantity=8, productType='Apparels', productGroup='T-Shirts', department='Children', image_url='https://images.footway.com/sm_images/009328874607_001_308d369926ed43dfa7ad8ad8117da919.png'), FootwayItem(productName='20/1 Mesh-ssl-psh Polo Black', size='L', vendor='Polo Ralph Lauren', quantity=3, productType='Apparels', productGroup='T-Shirts', department='Men', image_url='https://images.footway.com/02/60903-96_001.png'), FootwayItem(productName='2021-22 City Edition Philadelp Navy/red', size='L', vendor='Nike', quantity=1, productType='Apparels', productGroup='T-Shirts', department='Men', image_url='https://images.footway.com/02/60986-85_001.png'), FootwayItem(productName='2021-22 City Edition Philadelp Navy/red', size='M', vendor='Nike', quantity=2, productType='Apparels', productGroup='T-Shirts', department='Men', image_url='https://images.footway.com/02/60986-85_001.png'), FootwayItem(productName='2021-22 City Edition Philadelp Navy/red', size='S', vendor='Nike', quantity=1, productType='Apparels', productGroup='T-Shirts', department='Men', image_url='https://images.footway.com/02/60986-85_001.png'), FootwayItem(productName='20/21 Sweden Away Jersey Youth Night Indigo / Yellow', size='140', vendor='adidas', quantity=1, productType='Apparels', productGroup='T-Shirts', department='Children', image_url='https://images.footway.com/02/09347-45_001.png'), FootwayItem(productName='23 ENGINEE LONG SLEEVE TEE', size='S', vendor='Jordan', quantity=1, productType='Apparels', productGroup='T-Shirts', department='Men', image_url='https://images.footway.com/02/60588-05_001.png'), FootwayItem(productName='23 ENGINEE LONG SLEEVE TEE', size='M', vendor='Jordan', quantity=3, productType='Apparels', productGroup='T-Shirts', department='Men', image_url='https://images.footway.com/02/60588-04_001.png'), FootwayItem(productName='23 ENGINEE LONG SLEEVE TEE', size='M', vendor='Jordan', quantity=1, productType='Apparels', productGroup='T-Shirts', department='Men', image_url='https://images.footway.com/02/60588-05_001.png'), FootwayItem(productName='23 ENGINEE LONG SLEEVE TEE', size='XL', vendor='Jordan', quantity=1, productType='Apparels', productGroup='T-Shirts', department='Men', image_url='https://images.footway.com/02/60588-05_001.png'), FootwayItem(productName='23 ENGINEE LONG SLEEVE TEE', size='XXL', vendor='Jordan', quantity=2, productType='Apparels', productGroup='T-Shirts', department='Men', image_url='https://images.footway.com/02/60588-05_001.png'), FootwayItem(productName='23 ENGINEE LONG SLEEVE TEE', size='L', vendor='Jordan', quantity=3, productType='Apparels', productGroup='T-Shirts', department='Men', image_url='https://images.footway.com/02/60588-05_001.png'), FootwayItem(productName='23 ENGINEE LONG SLEEVE TEE', size='L', vendor='Jordan', quantity=3, productType='Apparels', productGroup='T-Shirts', department='Men', image_url='https://images.footway.com/02/60588-04_001.png'), FootwayItem(productName='23 ENGINEE LONG SLEEVE TEE', size='XL', vendor='Jordan', quantity=2, productType='Apparels', productGroup='T-Shirts', department='Men', image_url='https://images.footway.com/02/60588-04_001.png'), FootwayItem(productName='25/7 Tee Black', size='S', vendor='adidas', quantity=10, productType='Apparels', productGroup='T-Shirts', department='Women', image_url='https://images.footway.com/sm_images/001_8887979fa3e145ec92bc1674ed2093ce.png'), FootwayItem(productName='25/7 Tee Black', size='S', vendor='adidas', quantity=6, productType='Apparels', productGroup='T-Shirts', department='Men', image_url='https://images.footway.com/sm_images/001_382c6191ee5942518c6b4ac3efbfd155.png')], body_part='torso'),
 # FootwayResponse(items=[FootwayItem(productName='3S Dress Black', size='XS', vendor='adidas', quantity=12, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/sm_images/4062049338441_001_33bd3dab0e094c3fbe51745b8f29728d.png'), FootwayItem(productName='Adelina Skort 45 cm Red', size='34', vendor='Daily Sports', quantity=1, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/02/90086-99_001.png'), FootwayItem(productName='Adv Essence Hot Pants 2 W Black', size='S', vendor='Craft', quantity=3, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/02/60901-31_001.png'), FootwayItem(productName='Adv Essence Hot Pants 2 W Black', size='L', vendor='Craft', quantity=6, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/02/60901-31_001.png'), FootwayItem(productName='Adv Essence Hot Pants 2 W Black', size='XL', vendor='Craft', quantity=2, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/02/60901-31_001.png'), FootwayItem(productName='Adv Essence Hot Pants 2 W Black', size='M', vendor='Craft', quantity=10, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/02/60901-31_001.png'), FootwayItem(productName='Adv Essence Hot Pants 2 W Black', size='XS', vendor='Craft', quantity=4, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/02/60901-31_001.png'), FootwayItem(productName='Aia Mw Dnm Skirt Black', size='XS', vendor='Pieces', quantity=13, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/sm_images/5713754846040_002_bc2e6b2841f2471a8c9c41df0944817c.png'), FootwayItem(productName='Aia Mw Dnm Skirt Blue', size='XS', vendor='Pieces', quantity=14, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/sm_images/5713754846132_001_2e878871d16f48c8a399261006d46459.png'), FootwayItem(productName='Aidah Skirt Blue', size='42', vendor='Tenson', quantity=2, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/sm_images/7333019855730_001_d67235741cd84b9496a01f166f673310.png'), FootwayItem(productName='Aidah Skirt Blue/White', size='42', vendor='Tenson', quantity=3, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/sm_images/7333019855792_001_106f90d5fc364d638ebf7fc1bc33b63d.png'), FootwayItem(productName='Air Halterneck Dress Blue', size='S', vendor='Boob', quantity=3, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/sm_images/7332480184585_001_cb9c3db76947491b8b8f0e4a57e492c1.png'), FootwayItem(productName='Air Halterneck Dress Red', size='S', vendor='Boob', quantity=2, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/sm_images/7332480184554_001_cd5247e79c2f4b2cbdc64bc9b82c8911.png'), FootwayItem(productName='All-In-One Dress Engineered Blue', size='S', vendor='adidas Tennis', quantity=2, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/02/09351-76_001.png'), FootwayItem(productName='All-In-One Dress Engineered Blue', size='M', vendor='adidas Tennis', quantity=1, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/02/09351-76_001.png'), FootwayItem(productName='All-In-One Dress Engineered Blue', size='L', vendor='adidas Tennis', quantity=1, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/02/09351-76_001.png'), FootwayItem(productName='All-In-One Dress Engineered White', size='M', vendor='adidas Tennis', quantity=6, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/02/09351-75_001.png'), FootwayItem(productName='All-In-One Dress Engineered White', size='S', vendor='adidas Tennis', quantity=10, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/02/09351-75_001.png'), FootwayItem(productName='All-In-One Dress Engineered White', size='XS', vendor='adidas Tennis', quantity=3, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/02/09351-75_001.png'), FootwayItem(productName='All-In-One Dress Engineered White', size='L', vendor='adidas Tennis', quantity=4, productType='Apparels', productGroup='Shorts & Skirts & Dresses', department='Women', image_url='https://images.footway.com/02/09351-75_001.png')], body_part='lower body'),
 # FootwayResponse(items=[FootwayItem(productName='Headband Black', size='ONESIZE', vendor='Yonex', quantity=8, productType='Accessories & Equipment', productGroup='Headbands', department='Men', image_url='https://images.footway.com/02/61075-65_001.png'), FootwayItem(productName='Headband Navy Blue', size='ONESIZE', vendor='Yonex', quantity=9, productType='Accessories & Equipment', productGroup='Headbands', department='Men', image_url='https://images.footway.com/02/61075-63_001.png'), FootwayItem(productName='Logo Wristband White', size='ONESIZE', vendor='Babolat', quantity=13, productType='Accessories & Equipment', productGroup='Headbands', department='Women', image_url='https://images.footway.com/sm_images/3324921741086_001_3b0c44351469458da0da20e578f6c2eb.png')], body_part='head'),
 # FootwayResponse(items=[FootwayItem(productName='02.643-46 Dark Navy', size='EU 36', vendor='Gabor', quantity=2, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/602/60275-63/01/4000/4000/60275-63.png'), FootwayItem(productName='02.643-46 Dark Navy', size='EU 35,5', vendor='Gabor', quantity=1, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/602/60275-63/01/4000/4000/60275-63.png'), FootwayItem(productName='02.690.47 Black', size='EU 36', vendor='Gabor', quantity=7, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/491/49118-00/01/4000/4000/49118-00.png'), FootwayItem(productName='06.400.37 Black', size='EU 38,5', vendor='Gabor', quantity=160, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/491/49121-00/01/4000/4000/49121-00.png'), FootwayItem(productName='104 Canela Rosa Metal', size='EU 40', vendor='Billi Bi', quantity=1, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/600/60043-05/01/4000/4000/60043-05.png'), FootwayItem(productName='104 Nude Buffalo', size='EU 40', vendor='Billi Bi', quantity=1, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/600/60043-03/01/4000/4000/60043-03.png'), FootwayItem(productName='1099401 Himmelblau', size='EU 37', vendor='Mustang', quantity=4, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/600/60074-40/01/4000/4000/60074-40.png'), FootwayItem(productName='1-1-22104-22 001 Black', size='EU 36', vendor='Tamaris', quantity=2, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/601/60135-77/01/4000/4000/60135-77.png'), FootwayItem(productName='1-1-22104-22 001 Black', size='EU 37', vendor='Tamaris', quantity=4, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/601/60135-77/01/4000/4000/60135-77.png'), FootwayItem(productName='1-1-22104-22 678 Powder Flower', size='EU 36', vendor='Tamaris', quantity=1, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/601/60136-20/01/4000/4000/60136-20.png'), FootwayItem(productName='1-1-22104-24 Black', size='EU 36', vendor='Tamaris', quantity=1, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/602/60242-44/01/4000/4000/60242-44.png'), FootwayItem(productName='1-1-22104-24 Black', size='EU 37', vendor='Tamaris', quantity=1, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/602/60242-44/01/4000/4000/60242-44.png'), FootwayItem(productName='1-1-22129-24 Black Structure', size='EU 36', vendor='Tamaris', quantity=2, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/602/60242-48/shelf/160/1500/60242-48.png'), FootwayItem(productName='1-1-23631-24 White/silver', size='EU 36', vendor='Tamaris', quantity=1, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/602/60242-34/01/4000/4000/60242-34.png'), FootwayItem(productName='1-1-23722-25 Black Nubuc', size='EU 39', vendor='Tamaris', quantity=1, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/602/60266-60/01/4000/4000/60266-60.png'), FootwayItem(productName='1-1-23722-25 Black Nubuc', size='EU 37', vendor='Tamaris', quantity=3, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/602/60266-60/01/4000/4000/60266-60.png'), FootwayItem(productName='1-1-24211-24 Black', size='EU 36', vendor='Tamaris', quantity=4, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/602/60242-66/01/4000/4000/60242-66.png'), FootwayItem(productName='1-1-24212-22 001 Black', size='EU 36', vendor='Tamaris', quantity=2, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/01/601/60136-12/01/4000/4000/60136-12.png'), FootwayItem(productName='1-1-24216-20 006 Black', size='EU 38', vendor='Tamaris', quantity=9, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/02/60913-87_001.png'), FootwayItem(productName='1-1-24216-20 006 Black', size='EU 41', vendor='Tamaris', quantity=2, productType='Shoes', productGroup='Flats', department='Women', image_url='https://images.footway.com/02/60913-87_001.png')], body_part='feet'),
 # FootwayResponse(items=[FootwayItem(productName='1-pack Bauble Gift Set Red', size='41-46', vendor='Happy Socks', quantity=11, productType='Apparels', productGroup='Socks', department='Women', image_url=''), FootwayItem(productName='1-pack Bauble Gift Set Red', size='36-40', vendor='Happy Socks', quantity=1, productType='Apparels', productGroup='Socks', department='Women', image_url=''), FootwayItem(productName='1-pack Do Not Disturb Gift Set White', size='41-46', vendor='Happy Socks', quantity=12, productType='Apparels', productGroup='Socks', department='Women', image_url=''), FootwayItem(productName='1-pack Heart Sock Gift Set Navy', size='41-46', vendor='Happy Socks', quantity=7, productType='Apparels', productGroup='Socks', department='Women', image_url=''), FootwayItem(productName='1-pack Snowflake Gift Set Dark Green', size='41-46', vendor='Happy Socks', quantity=10, productType='Apparels', productGroup='Socks', department='Women', image_url=''), FootwayItem(productName='1-pack Snowflake Gift Set Dark Green', size='36-40', vendor='Happy Socks', quantity=2, productType='Apparels', productGroup='Socks', department='Women', image_url=''), FootwayItem(productName='24-pack Advent Calendar Gift S White', size='36-40', vendor='Happy Socks', quantity=1, productType='Apparels', productGroup='Socks', department='Women', image_url=''), FootwayItem(productName='24-pack Advent Calendar Gift S White', size='36-40', vendor='Happy Socks', quantity=1, productType='Apparels', productGroup='Socks', department='Women', image_url=''), FootwayItem(productName='24-pack Advent Calendar Gift S White', size='41-46', vendor='Happy Socks', quantity=8, productType='Apparels', productGroup='Socks', department='Women', image_url=''), FootwayItem(productName='2-Pack Basic Socks - Mario Blue', size='23-26', vendor='Norfolk', quantity=18, productType='Apparels', productGroup='Socks', department='Children', image_url='https://images.footway.com/sm_images/8680081423688_001_e7b6fd6317304e32ba90b35038841d5a.png'), FootwayItem(productName='2-Pack Basic Socks - Mario Blue', size='27-30', vendor='Norfolk', quantity=32, productType='Apparels', productGroup='Socks', department='Children', image_url='https://images.footway.com/sm_images/8680081423688_001_e7b6fd6317304e32ba90b35038841d5a.png'), FootwayItem(productName='2-Pack Basic Socks - Mario Green', size='31-34', vendor='Norfolk', quantity=3, productType='Apparels', productGroup='Socks', department='Children', image_url='https://images.footway.com/sm_images/8680081423749_001_1c89e1cceab7492199c29c11224dc380.png'), FootwayItem(productName='2-Pack Basic Socks - Mario Green', size='23-26', vendor='Norfolk', quantity=71, productType='Apparels', productGroup='Socks', department='Children', image_url='https://images.footway.com/sm_images/8680081423749_001_1c89e1cceab7492199c29c11224dc380.png'), FootwayItem(productName='2-Pack Basic Socks - Mario Green', size='27-30', vendor='Norfolk', quantity=9, productType='Apparels', productGroup='Socks', department='Children', image_url='https://images.footway.com/sm_images/8680081423749_001_1c89e1cceab7492199c29c11224dc380.png'), FootwayItem(productName='2-Pack Basic Socks - Mario Patterned', size='23-26', vendor='Norfolk', quantity=28, productType='Apparels', productGroup='Socks', department='Children', image_url='https://images.footway.com/sm_images/8680081423824_001_589c28a17a684f78ae2af263ad55b269.png'), FootwayItem(productName='2-Pack Basic Socks - Mario Pink', size='23-26', vendor='Norfolk', quantity=170, productType='Apparels', productGroup='Socks', department='Children', image_url='https://images.footway.com/sm_images/8680081423770_001_94190e62abdf424191724a9c18c8ffd0.png'), FootwayItem(productName='2-Pack Basic Socks - Mario Pink', size='27-30', vendor='Norfolk', quantity=83, productType='Apparels', productGroup='Socks', department='Children', image_url='https://images.footway.com/sm_images/8680081423770_001_94190e62abdf424191724a9c18c8ffd0.png'), FootwayItem(productName='2-Pack Basic Socks - Mario Pink', size='31-34', vendor='Norfolk', quantity=22, productType='Apparels', productGroup='Socks', department='Children', image_url='https://images.footway.com/sm_images/8680081423770_001_94190e62abdf424191724a9c18c8ffd0.png'), FootwayItem(productName='2-pack Bestie Socks Gift Set Dark Blue', size='36-40', vendor='Happy Socks', quantity=5, productType='Apparels', productGroup='Socks', department='Women', image_url='https://images.footway.com/02/60523-23_001.png'), FootwayItem(productName='2-Pack Big Dot Low Socks Black', size='41-45', vendor='Happy Socks', quantity=12, productType='Apparels', productGroup='Socks', department='Women', image_url='https://images.footway.com/sm_images/7333102126952_001_51c83befa65e41bc90082ab3cc436989.png')], body_part='accessory')]
    return results



async def main():
    image_path = "examples/malfoy.jpeg"
    description_ = ip.describe_image(image_path)
    print(f"Image description: {description_}")
    footway_inputs = []
    body_parts = []

    for item in description_:
        footway_input = ip.convert_description_to_footway_input(item)
        footway_inputs.append(footway_input)
        body_parts.append(item.body_part)
        print(f"Raw item description: {item}")
        print(f"Footway input: {footway_input}")

    # body_parts = ["upper body", "neck", "torso", "full_body"]
    #
    # footway_inputs = [
    #     ip.FootwayInput(vendors="None", departments="None", product_groups='Hoodies & Sweaters',
    #                     product_types='Apparels'),
    #     ip.FootwayInput(vendors="None", departments="None", product_groups='Other Accessories',
    #                     product_types='Apparels'),
    #     ip.FootwayInput(vendors="None", departments="None", product_groups='Shirts', product_types='Apparels'),
    #     ip.FootwayInput(vendors="None", departments="None", product_groups='Cardigan', product_types='Apparels'),
    # ]

    results = await search_inventory(footway_inputs, body_parts)
    for result in results:
        print(len(result.items))
    pprint(results)


if __name__ == "__main__":
    asyncio.run(main())
