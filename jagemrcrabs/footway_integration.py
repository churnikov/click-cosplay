import asyncio
from pprint import pprint

import aiohttp
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
