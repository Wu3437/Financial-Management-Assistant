import sys
from flask import Flask, request, jsonify, render_template
from standalone_chatbot import StandaloneChatbot

print("Initializing Flask app...", file=sys.stderr)
app = Flask(__name__)
print("Creating chatbot instance...", file=sys.stderr)
bot = StandaloneChatbot()
print("Chatbot initialized successfully!", file=sys.stderr)

@app.route('/')
def index():
    print("Serving index page...", file=sys.stderr)
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get('message', '')
        print(f"Received message: {user_input}", file=sys.stderr)
        
        if not user_input:
            return jsonify({'response': '请输入内容~'})
        
        response = bot.respond(user_input)
        print(f"Response: {response}", file=sys.stderr)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}", file=sys.stderr)
        return jsonify({'response': f'抱歉，处理失败：{str(e)}'})

@app.route('/api/status')
def status():
    return jsonify({'status': 'online'})

if __name__ == '__main__':
    print("Starting Flask server on http://localhost:5000...", file=sys.stderr)
    app.run(debug=True, host='0.0.0.0', port=5000)