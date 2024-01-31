import json
import requests
import datetime
import numpy as np
from tensorflow import keras
import pickle
import openai
from bardapi import SESSION_HEADERS, Bard


class ultraChatBot:
    def __init__(self, json):
        self.json = json
        self.dict_messages = json["data"]
        self.ultraAPIUrl = "https://api.ultramsg.com/{instanceid}/"
        self.token = "{instancetoken}"

    def send_requests(self, type, data):
        url = f"{self.ultraAPIUrl}{type}?token={self.token}"
        headers = {"Content-type": "application/json"}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()

    def send_message(self, chatID, text):
        data = {"to": chatID, "body": text}
        answer = self.send_requests("messages/chat", data)
        return answer

    def send_image(self, chatID):
        data = {
            "to": chatID,
            "image": "https://file-example.s3-accelerate.amazonaws.com/images/test.jpeg",
        }
        answer = self.send_requests("messages/image", data)
        return answer

    def send_contact(self, chatID):
        data = {"to": chatID, "contact": "917893414930@c.us"}
        answer = self.send_requests("messages/contact", data)
        return answer

    def time(self, chatID):
        t = datetime.datetime.now()
        time = t.strftime("%Y-%m-%d %H:%M:%S")
        return self.send_message(chatID, time)

    def get_gpt_response(self, chatID, text):
        openai.api_key = "{openaiapikey}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}],
            max_tokens=100,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return self.send_message(chatID, response.choices[0].message["content"])

    def send_bard_response(self, chatID, message):
        session = requests.session()
        session.headers = SESSION_HEADERS
        session.cookies.set(
            "__Secure-1PSID",
            "aAibYkv1Rp38V7T1oFkwLzPHF5F73wF19u1wPT0RTv52TGlI2zXOQ_q2vv4XPvNP_nziIA.",
        )
        session.cookies.set(
            "__Secure-1PSIDTS",
            "sidts-CjEBSAxbGaAAjppcAVPtP1h7PbHSYd7UWnrBxD4AE6Apb87oQCdTwe5EmTI9Aqj43bV-EAA",
        )
        session.cookies.set(
            "__Secure-1PSIDCC",
            "APoG2W__umS-P5i0NZgKp5yT095JDqrVZ84WUSwS9NHaylYQQiVTzDo6SEYWeG8HAAePvjqi",
        )
        bard = Bard(session=session, token_from_browser=True)
        response = bard.get_answer(message)
        return self.send_message(chatID, response["content"])

    def extract_location(self, message):
        if "location" in message:
            location_data = message["location"]
            latitude = location_data.get("latitude")
            longitude = location_data.get("longitude")
            if latitude is not None and longitude is not None:
                api_url = f"https://apis.mapmyindia.com/advancedmaps/v1/5c78d5d1-bb8c-4901-9ae1-aea8e47720d8/rev_geocode?lng={longitude}&lat={latitude}&region=IND"
                try:
                    response = requests.get(api_url)
                    response_data = response.json()
                    if "results" in response_data:
                        results = response_data["results"][0]
                        formatted_address = results.get("formatted_address")
                        lat = results.get("lat")
                        lng = results.get("lng")
                        if formatted_address and lat and lng:
                            return f"Location: {formatted_address}, Latitude: {lat}, Longitude: {lng}"
                        else:
                            return "Location details not found."
                    else:
                        return "Failed to retrieve location details."
                except Exception as e:
                    return f"Error: {str(e)}"
        return "Latitude and longitude not found in the location attachment."

    def chat_with_model(self, user_input):
        with open("intents.json") as file:
            data = json.load(file)
        model = keras.models.load_model("chat_model")
        with open("tokenizer.pickle", "rb") as handle:
            tokenizer = pickle.load(handle)
        with open("label_encoder.pickle", "rb") as ecn:
            lbl_encoder = pickle.load(ecn)
        max_len = 20

        result = model.predict(
            keras.preprocessing.sequence.pad_sequences(
                tokenizer.texts_to_sequences([user_input]),
                truncating="post",
                maxlen=max_len,
            )
        )
        tag = lbl_encoder.inverse_transform([np.argmax(result)])
        for i in data["intents"]:
            if i["tag"] == tag:
                return ((np.random.choice(i["responses"])),)

    def Processingـincomingـmessages(self):
        if self.dict_messages != []:
            message = self.dict_messages
            text = message["body"].split()
            if not message["fromMe"]:
                chatID = message["from"]
                if text[0].lower() == "time":
                    return self.time(chatID)
                elif text[0].lower() == "image":
                    return self.send_image(chatID)
                elif text[0].lower() == "contact":
                    return self.send_contact(chatID)
                elif text[0].lower() == "gpt":
                    if len(text) >= 2:
                        input_text = " ".join(text[1:])
                        return self.get_gpt_response(chatID, input_text)
                    else:
                        return self.send_message(
                            chatID, "Please provide input for GPT-3."
                        )
                elif text[0].lower() == "bard":
                    if len(text) >= 2:
                        input_text = " ".join(text[1:])
                        return self.send_bard_response(chatID, input_text)
                    else:
                        return self.send_message(
                            chatID, "Please provide input for Bard."
                        )
                elif "location" in message:
                    location_result = self.extract_location(message)
                    if isinstance(location_result, tuple):
                        formatted_address, latitude, longitude = location_result
                        response_message = (
                            f"Address: {formatted_address}\n"
                            f"Latitude: {latitude}\n"
                            f"Longitude: {longitude}"
                        )
                        return self.send_message(chatID, response_message)
                    else:
                        return self.send_message(chatID, location_result)
                else:
                    user_input = message["body"]
                    response = self.chat_with_model(user_input)
                    return self.send_message(chatID, response)
            else:
                return "NoCommand"
