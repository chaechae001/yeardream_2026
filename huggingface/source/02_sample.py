from transformers import pipeline

# Load the classification pipeline with the specified model
pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")

# Classify a new sentence
# sentence = "I love this product! It's amazing and works perfectly."
sentence = "공간을 많이 차지하지 않고, 냉방 능력이 확실함."
result = pipe(sentence)

# Print the result
print(result)
