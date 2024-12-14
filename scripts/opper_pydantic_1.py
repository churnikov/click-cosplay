import asyncio
# It is strongly recommended to use the `AsyncOpper` client to make calls asynchronously
# but if that is not an option, there is also an `Opper` client to make calls synchronously
from opperai import AsyncOpper
# Our SDK supports Pydantic to provide structured output
from pydantic import BaseModel

from jagemrcrabs.settings import settings


# Define the output structure
class RoomDescription(BaseModel):
    room_count: int
    view: str
    bed_size: str
    hotel_name: str

async def main():
    # Don't forget to set the API key as the OPPER_API_KEY environment variable!
    opper = AsyncOpper(api_key=settings.opper_api_key.get_secret_value())

    # Make a call
    result, _ = await opper.call(
        name="extractRoom",
        instructions="Extract details about the room from the provided text",
        input="The Grand Hotel offers a luxurious suite with 3 spacious rooms, each providing a breathtaking view of the ocean. The suite includes a king-sized bed, an en-suite bathroom, and a private balcony for an unforgettable stay.",
        output_type=RoomDescription,
    )

    print(result)
    # RoomDescription(room_count=3, view='ocean', bed_size='king-sized', hotel_name='The Grand Hotel')

asyncio.run(main())
