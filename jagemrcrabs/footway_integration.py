import asyncio
from pprint import pprint

import aiohttp
import image_processing as ip
from jagemrcrabs.settings import settings
from pydantic import BaseModel


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


async def fetch(url, session, params=None) -> FootwayResponse:
    # Perform an HTTP GET request with query parameters
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
            items=items
        )
        return response


async def fetch_all(url, params_list):
    async with aiohttp.ClientSession() as session:
        # Create tasks for all requests with different query parameters
        tasks = [fetch(url, session, params=params) for params in params_list]
        return await asyncio.gather(*tasks)


# Example URL
FOOTWAY_PLUS_API = "https://api.footwayplus.com/v1/inventory/search"


async def search_inventory(footway_input_list: list[ip.FootwayInput]) -> [FootwayResponse]:
    params = []
    for footway_input in footway_input_list:
        params.append(
            {
                "department": footway_input.departments if footway_input.departments != "None" else "",
                "productGroup": footway_input.product_groups,
                "productType": footway_input.product_types,
            }
        )
    return await fetch_all(FOOTWAY_PLUS_API, params)


async def main():
    image_path = "examples/malfoy.jpeg"
    description_ = ip.describe_image(image_path)
    print(f"Image description: {description_}")
    footway_inputs = []
    for item in description_:
        footway_input = ip.convert_description_to_footway_input(item)
        footway_inputs.append(footway_input)
        print(f"Raw item description: {item}")
        print(f"Footway input: {footway_input}")

    # footway_inputs = [
    #     ip.FootwayInput(vendors="None", departments="None", product_groups='Hoodies & Sweaters',
    #                     product_types='Apparels'),
    #     ip.FootwayInput(vendors="None", departments="None", product_groups='Other Accessories',
    #                     product_types='Apparels'),
    #     ip.FootwayInput(vendors="None", departments="None", product_groups='Shirts', product_types='Apparels'),
    #     ip.FootwayInput(vendors="None", departments="None", product_groups='Cardigan', product_types='Apparels'),
    # ]

    results = await search_inventory(footway_inputs)
    for result in results:
        print(len(result.items))
    pprint(results)


if __name__ == "__main__":
    asyncio.run(main())
