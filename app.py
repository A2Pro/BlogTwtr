from flask import Flask, jsonify, request, render_template
from openai import OpenAI
import requests
from dotenv import load_dotenv

import os

load_dotenv()

print(os.getenv("OPENAI_API_KEY"))
app = Flask(__name__)
client = OpenAI(
    api_key="",
)


def ask_gpt(prompt):
    response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Here is a long text. Turn it into 3 twitter posts. IMPORTANT: You need to generate "
                               "some text in the voice of the author for each blog post to completely sum it up or "
                               "finish off your point. If it's a blog, maybe not as much. Each individual post should fully encapsulate the whole article, summing up everything, and each individual post can convey the message of the whole article. ENSURE THAT ALL TEXT THAT IS GENERATED, IS GENERATED IN THE VOICE OF THE AUTHOR. Put in the format Post 1: Post, Post 2: Post , Post 3 :Post. IMPORTANT: NO SPECIAL CHARACTERS. Here's the text: " + prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )
    if "Post" not in response.choices[0].message.content:
        ask_gpt(prompt)
    return response.choices[0].message.content


def split_into_content(content):
    response = ask_gpt(content)
    with open("response.txt", "w") as f:
        f.write(response)


@app.route('/process', methods=['POST'])
def process_text():
    if request.method == 'POST':
        data = request.get_json()
        text = data.get('text', '')
        if "medium.com" in text:
            data = text.split("-")[-1]
            url = f'https://medium2.p.rapidapi.com/article/{data}/content'

            headers = {
                "X-RapidAPI-Key": "230e8649e8msh98f52a40b7c2062p195e3fjsnef027265a3f1",
                "X-RapidAPI-Host": "medium2.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers)

            text = response.json()['content']

        x = ask_gpt(text)
        return jsonify({'processed_text': x})



@app.route('/input')
def takeinput():
    return render_template("input.html")


if __name__ == '__main__':
    app.run()
