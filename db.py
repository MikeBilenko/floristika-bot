import requests
import os


API_URL = os.getenv(
    "API_URL",
    "https://www.baclendfloristika.life/api/v1"
)


class API:

    @staticmethod
    def get_product(product_id):
        url = f"{API_URL}/products/telegram/get/{product_id}/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    @staticmethod
    def get_order_status(order_id):
        url = f"{API_URL}/orders/order/telegram/get/{order_id}/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    @staticmethod
    def get_stores():
        url = f"{API_URL}/stores/"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")