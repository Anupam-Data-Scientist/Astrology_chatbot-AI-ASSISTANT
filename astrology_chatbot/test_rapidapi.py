from transformers import pipeline

pipe = pipeline("text2text-generation", model="google/flan-t5-small")
output = pipe("Translate English to French: What is your name?")
print(output)
