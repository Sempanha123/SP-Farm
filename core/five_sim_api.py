# core/five_sim_api.py
import requests

class FiveSimAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://5sim.net/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }














    def _parse_response(self, response):
        """Helper method to safely parse JSON and handle common 5sim text errors."""
        if response.status_code == 200:
            try:
                # print("from 200: ", response.json())
                return response.json()
            except requests.exceptions.JSONDecodeError:
                print("ex: ", response.text)
                return {"error": f"Invalid JSON received: {response.text}"}
        
        elif response.status_code == 400:
            print("from 400 :", {"error": response.text})
            return {"error": response.text}
            
        elif response.status_code == 401:
            print("from 400 :", {"error": "Unauthorized: Invalid or expired API Key."})
            return {"error": "Unauthorized: Invalid or expired API Key."}
            
        else:
            print("from 400 :", {"error": f"API Error {response.status_code}: {response.text}"})
            return {"error": f"API Error {response.status_code}: {response.text}"}

    def get_profile(self):
        """Fetches account email and balance."""
        if not self.api_key:
            return {"error": "No API Key"}
            
        try:
            url = f"{self.base_url}/user/profile"
            response = requests.get(url, headers=self.headers, timeout=5)
            return self._parse_response(response)
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Network Error: {str(e)}"}

    def get_countries(self):
        """Fetches the list of available countries from 5sim."""
        try:
            url = f"{self.base_url}/guest/countries"
            headers = {"Accept": "application/json"}
            # No Auth header needed for guest endpoints
            response = requests.get(url, headers=headers, timeout=5)
            return self._parse_response(response)
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Network Error: {str(e)}"}
        
    def buy_number(self, country="any", operator="any", product="facebook"):
        """Purchases an activation number."""
        if not self.api_key:
            return {"error": "No API Key"}
            
        try:
            url = f"{self.base_url}/user/buy/activation/{country}/{operator}/{product}"
            response = requests.get(url, headers=self.headers, timeout=10)
            return self._parse_response(response)
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Network Error: {str(e)}"}

    def check_sms(self, order_id):
        """Checks if the SMS code has arrived for a specific order."""
        if not self.api_key:
            return {"error": "No API Key"}
            
        try:
            url = f"{self.base_url}/user/check/{order_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            return self._parse_response(response)
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Network Error: {str(e)}"}

    def cancel_order(self, order_id):
        """Cancels the order to get a refund if the number is banned or SMS fails."""
        if not self.api_key:
            return {"error": "No API Key"}
            
        try:
            url = f"{self.base_url}/user/cancel/{order_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            return self._parse_response(response)
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Network Error: {str(e)}"}

    def finish_order(self, order_id):
        """Completes the order after successful registration."""
        if not self.api_key:
            return {"error": "No API Key"}
            
        try:
            url = f"{self.base_url}/user/finish/{order_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            return self._parse_response(response)
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Network Error: {str(e)}"}