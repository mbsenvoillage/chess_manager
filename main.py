from app import App
import traceback

try:
    app = App()
    app.run()
except Exception as e:
    print(e)
    print(traceback.format_exc())
