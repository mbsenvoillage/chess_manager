from app import App
import traceback

try:
    app = App()
    app.run()
except Exception as e:
    print("In the App file")
    print(traceback.format_exc())