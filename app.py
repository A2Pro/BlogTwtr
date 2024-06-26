from flask import Flask, jsonify, request, render_template
from openai import OpenAI
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


def ask_gpt(prompt):
    response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Here is a long text. Turn it into 3 twitter posts. IMPORTANT: You need to generate "
                               "some text in the voice of the author for each blog post to completely sum it up or "
                               "finish off your point. If it's a blog, maybe not as much. Make sure not to simply split the text into 3 sections and summarize each one, rather make 3 short summarizations of the whole article. So each tweet should incoportate elements from throughout the article. Each first sentence of each tweet (aka the hook) should be not in chronological order. So basically, I don't want you to write three individual tweets about three different things. I want you to write, for each tweet, an overview of the whole article. ENSURE THAT ALL TEXT THAT IS GENERATED, IS GENERATED IN THE VOICE OF THE AUTHOR. Put in the format Post 1: Post, Post 2: Post , Post 3 :Post. IMPORTANT: NO SPECIAL CHARACTERS. Here's the text: " + prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )
    if "Post" not in response.choices[0].message.content:
        print(response.choices[0].message.content)
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
                "X-RapidAPI-Key": os.getenv("RAPIDAPI_API_KEY"),
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
