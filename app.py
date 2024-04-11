from flask import Flask, jsonify, request, render_template
from openai import OpenAI

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
                               "finish off your point. If it's a blog, maybe not as much. Put in the format Post 1: Post, Post 2: Post , Post 3 :Post. IMPORTANT: NO SPECIAL CHARACTERS. Here's the text: " + prompt,
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
        x = ask_gpt(text)
        return jsonify({'processed_text': x})



@app.route('/input')
def takeinput():
    return render_template("input.html")


if __name__ == '__main__':
    app.run()
