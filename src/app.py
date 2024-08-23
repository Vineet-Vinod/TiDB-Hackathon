from website import createApp

app = createApp() # Create an instance of the web app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")