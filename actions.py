import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from hashlib import sha256


class ActionGenerateTransactionKey(Action):

    def name(self) -> Text:
        return "action_generate_transaction_key"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        transaction_id = tracker.sender_id  
        transaction_key = sha256(transaction_id.encode()).hexdigest()

        dispatcher.utter_message(text=f"Your transaction key is: {transaction_key}")

        return []


class ActionPerformCryptoTransaction(Action):

    def name(self) -> Text:
        return "action_perform_crypto_transaction"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        amount = float(tracker.get_slot("amount"))
        currency = tracker.get_slot("currency")
        transaction_key = tracker.get_slot("transaction_key")  

        btc_price_endpoint = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        usd_price_endpoint = "https://api.coingecko.com/api/v3/simple/price?ids=usd&vs_currencies=brl"

        btc_price_response = requests.get(btc_price_endpoint)
        btc_price = btc_price_response.json()["bitcoin"]["usd"]

        usd_price_response = requests.get(usd_price_endpoint)
        usd_price = usd_price_response.json()["usd"]["brl"]

        if currency == "btc":
            volume = amount
            price = amount * btc_price
        elif currency == "usd":
            volume = amount / usd_price
            price = amount

        dispatcher.utter_message(
            text=f"Transaction Key: {transaction_key}\n"
            f"Amount: {amount}\n"
            f"Currency: {currency}\n"
            f"Volume: {volume}\n"
            f"Price: {price}"
        )

        return []
