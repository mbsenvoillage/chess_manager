from app import App

try:
    app = App()
    app.run()
except Exception as e:
    print("In the App file")
    print(e)