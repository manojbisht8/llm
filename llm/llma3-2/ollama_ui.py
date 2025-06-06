from flask import Flask, request, render_template
import requests

app = Flask(__name__)

#####Define Constants#############
HTML_TEMPLATE = "llma3-2-prompt.html"
API_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "llama3.2"
###################################


@app.route('/', methods=['GET', 'POST'])
def index():
    response = None
    if request.method == 'POST':
        prompt = request.form['prompt']
        response = get_ollama_response(prompt)
    return render_template(HTML_TEMPLATE, response=response)

import requests

def get_ollama_response(prompt, model=DEFAULT_MODEL, api_url=API_URL):
    """
    Sends a prompt to the Ollama API and returns the model's response.

    Args:
        prompt (str): The user's input prompt.
        model (str): The model to use (default is "llama3.2").
        api_url (str): The API endpoint URL.

    Returns:
        str: The model's response content or an error message.
    """
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return data.get("message", {}).get("content", "No content in response.")
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    except ValueError:
        return "Invalid JSON response from API."


if __name__ == '__main__':
    app.run(debug=True)
