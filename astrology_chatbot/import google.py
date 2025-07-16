import google.generativeai as genai

genai.configure(api_key="AIzaSyDxlZC7JkCHCaQWHqtl3uoyyYmfHfUhYh8")

models = genai.list_models()
for model in models:
    print(model.name)
