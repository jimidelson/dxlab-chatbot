from flask import Flask, request, render_template, jsonify
import openai
import os

app = Flask(__name__)

# OpenAI API Key (Load from environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load knowledge base from a local file
KNOWLEDGE_BASE_FILE = "../data/dxlab_knowledge_base.txt"

def load_knowledge_base():
    """Loads DXLab documentation from a file"""
    with open(KNOWLEDGE_BASE_FILE, "r", encoding="utf-8") as f:
        return f.read()

knowledge_base = load_knowledge_base()

def ask_chatbot(user_input):
    """Send user question to OpenAI with DXLab context"""
    prompt = f"""You are an expert in DXLab, answering questions based on this knowledge base:

    {knowledge_base}

    User Question: {user_input}
    Answer:
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=["GET"])
def home():
    return render_template("chat.html")

@app.route("/ask", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    response = ask_chatbot(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

