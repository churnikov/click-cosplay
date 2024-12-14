from opperai import Opper

from jagemrcrabs.settings import settings

# Your API key will be loaded from the environment variable OPPER_API_KEY if not provided
opper = Opper(api_key=settings.opper_api_key)

result, _ = opper.call(name="onboarding", input="What is the capital of Sweden?")
print(result)
