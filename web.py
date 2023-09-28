from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse
import joblib
import re
import joblib
import re

loaded_classifier = joblib.load('C:/Users/omkar/Desktop/project/DecisionTree/decision_tree_model.pkl')
loaded_vectorizer = joblib.load('C:/Users/omkar/Desktop/project/DecisionTree/vectorizer.pkl')

# Preprocess user input
def preprocess_input(input_text):
    # Convert to lowercase
    input_text = input_text.lower()
    # Remove special characters
    input_text = re.sub(r'[^a-zA-Z0-9\s]', '', input_text)
    return input_text

app = FastAPI()

valid_users = {
    "admin": "admin",
    "user": "admin"
}

html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Drug Recommendation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
            background-image: url('https://i.ibb.co/zNbMgzM/img.png');
            background-position-y: 100px;
            background-position-x: 120px;
        }
        .container {
            width: 80%;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 5px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        h2 {
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"],
        input[type="password"],
        textarea {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 3px;
            font-size: 16px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            font-size: 16px;
        }
        #medicineResult {
            margin-top: 20px;
            font-weight: bold;
        }
        #loginError {
            color: red;
            display: none;
        }

        #lofin
        {
            opacity: 1;
        }
    </style>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
    <script>
         function showMedicine() {
            document.getElementById("medicine").style.display = "block";
        }


    </script>
</head>
<body>
    <div class="container" >
        <h2>Drug Recommendation</h2>
        <form method="post" id="loginForm">
            <label for="username" id="login">Username:</label>
            <input type="text" id="username" name="username" required>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            <button type="submit" onclick="showMedicine()">Login</button>
        </form>
        <p id="loginError">Invalid credentials</p>
    </div>

    <div class="container" id="medicine" style="display: none;">
        <textarea id="paragraph" rows="4" placeholder="Enter paragraph..."></textarea>
        <button onclick="getMedicine()">Get Medicine</button>
        <button onclick="clearInput()">Reload</button>
        <p id="medicineResult" ></p>
    </div>
    <script>

        $(document).ready(function(){
            $("#medicineResult").hide();
        });

    function showMedicine() {
        document.getElementById("loginError").style.display = "none"; // Hide the login error message
        document.getElementById("loginForm").style.display = "none"; // Hide the login form
    }

    function clearInput() {
        document.getElementById("paragraph").value = ""; // Clear the input box
        document.getElementById("medicineResult").innerText = ""; // Clear the medicine result text
    }

         function getMedicine() {
            $("#medicineResult").show();
    const paragraph = document.getElementById("paragraph").value;
    fetch("/get_medicine?paragraph=" + encodeURIComponent(paragraph))
        .then(response => response.text())  // Receive response as text
        .then(data => {
            document.getElementById("medicineResult").innerText = "Recommended Medicine: " + data;
            document.getElementById("medicine").style.display = "block"; // Show the medicine section
        });
}
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def get_login_page():
    return html_content


@app.post("/")
def login(username: str = Form(...), password: str = Form(...)):
    if username in valid_users and valid_users[username] == password:
        return HTMLResponse(content=html_content.replace('style="color: red; display: none;"', 'style="color: red; display: none;"') + '<script>showMedicine(); getMedicine();</script>')
    else:
        return HTMLResponse(content=html_content.replace('style="color: red; display: none;"', 'style="color: red; display: block;"'))


@app.get("/get_medicine")
def get_medicine(paragraph: str):
    if paragraph:
        user_input = preprocess_input(paragraph)  # Preprocess the user input
        input_vector = loaded_vectorizer.transform([user_input]).toarray()  # Use the loaded vectorizer
        recommended_medicine = loaded_classifier.predict(input_vector)  # Use the loaded model

        return PlainTextResponse(content=recommended_medicine[0], media_type="text/plain") 
    else:
        raise HTTPException(status_code=400, detail="Missing paragraph")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
