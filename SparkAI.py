import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, jsonify, request
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage


#init GOOGLE API
load_dotenv(find_dotenv())
os.getenv('GOOGLE_API_KEY')

app = Flask(__name__)

#initiate Google llm

llm = ChatGoogleGenerativeAI(
    model = "gemini-1.5-pro",
    temparature=0,
    max_output_tokens= None,
    max_retries = 2,
    timeout=None,
)

chat_history =[]

@app.route('/clear', methods=['POST'])
def clear():
    global chat_history
    chat_history.clear()  # This resets the array to an empty list
    return jsonify({"message": "Array cleared", "array": chat_history}), 200


@app.route('/chat', methods=['POST'])
def chat():
    
    #get input from user
    user_input = request.json.get('message')
    print(chat_history)
    if not user_input:
        return jsonify({"error":"No message provided"}),400
    try:
        chat_history.append(HumanMessage(user_input))
        #Generate AI response from LLM
        response = llm.invoke(chat_history)
        chat_history.append(AIMessage(response.content))
        return jsonify({"response":response.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
  return  """
    <html>
        <body>
            <h1>Chat API</h1>
            <div id="response"></div>
            <form id="chatForm">
                <input type="text" id="messageInput" placeholder="Enter your message">
                <button type="submit">Send</button>
                <button type="reset">Start over</button>
            </form>
            

            <script>
                document.getElementById('chatForm').onreset = function(e) {
                    e.preventDefault();
                    fetch('/clear',{
                        method: 'POST'
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('response').innerText = "";
                        document.getElementById('messageInput').value = "";
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
                };
                document.getElementById('chatForm').onsubmit = function(e) {
                    e.preventDefault();
                    var message = document.getElementById('messageInput').value;
                    
                    fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({message: message}),
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('response').innerText = data.response;
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
                };
            </script>
        </body>
    </html>
    """

if __name__=="__main__":
    app.run()
