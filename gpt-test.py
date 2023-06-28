from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B")

inputs = tokenizer("Hello world!", return_tensors="pt")
print(inputs)
outputs = model(**inputs)
print(outputs)