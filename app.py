from flask import Flask, render_template_string, request

app = Flask(__name__)

# Basic CSS style for the page
page_style = """
<style>
  body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    margin: 0; padding: 0; 
    display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh;
  }
  h1 {
    font-size: 3em;
    margin-bottom: 0;
  }
  p {
    font-size: 1.25em;
    margin-top: 0;
    margin-bottom: 1.5em;
  }
  input[type="text"] {
    padding: 10px; 
    font-size: 1em; 
    border-radius: 5px; 
    border: none;
    margin-right: 10px;
  }
  button {
    padding: 10px 15px;
    font-size: 1em;
    border-radius: 5px;
    border: none;
    background-color: #5a31f4;
    color: white;
    cursor: pointer;
  }
  button:hover {
    background-color: #3e20a0;
  }
  footer {
    position: absolute;
    bottom: 15px;
    font-size: 0.9em;
    color: #ddd;
  }
</style>
"""

# Home page with a welcome message and a simple greeting form
@app.route("/", methods=["GET", "POST"])
def home():
    greeting = ""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            greeting = f"Hello, {name}! Welcome to myWelcomeWebApp 🎉"
        else:
            greeting = "Hello, mysterious visitor! Please enter your name next time 😉"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome to myWelcomeWebApp</title>
        {page_style}
    </head>
    <body>
        <h1>Welcome to <span style="color:#ffd700;">myWelcomeWebApp</span>!</h1>
        <p>Built with Python & Flask on Azure App Service</p>

        <form method="post">
            <input type="text" name="name" placeholder="Enter your name" autocomplete="off" />
            <button type="submit">Greet Me</button>
        </form>

        <p style="margin-top:20px; font-size:1.5em;">{greeting}</p>

        <footer>Made by Vivek Singh Shekhawat | Azure App Service Demo</footer>
    </body>
    </html>
    """
    return render_template_string(html)


# About page with some info
@app.route("/about")
def about():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>About myWelcomeWebApp</title>
        {page_style}
    </head>
    <body>
        <h1>About This App</h1>
        <p>This app demonstrates deployment of a Python Flask app on Azure App Service.</p>
        <p>Features include:</p>
        <ul>
            <li>Dynamic greeting form</li>
            <li>Clean UI with CSS styling</li>
            <li>Multiple routes</li>
        </ul>
        <p>Created by Vivek Singh Shekhawat</p>
        <a href="/" style="color:#ffd700; font-weight:bold;">Back to Home</a>
        <footer>Azure App Service Demo</footer>
    </body>
    </html>
    """
    return render_template_string(html)


# Health check endpoint for Azure or monitoring tools
@app.route("/health")
def health():
    return {"status": "Healthy", "app": "myWelcomeWebApp"}, 200


if __name__ == "__main__":
    # Run on port 8000 to match Azure App Service expectations
    app.run(host="0.0.0.0", port=8000)
