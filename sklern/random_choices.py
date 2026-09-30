# This code is just for understanding the softmax functionality in Gen AI transformer model

# Softmax : Chooses best possible word. 
# To illustrate I am generating inputs and probability, and use random module to choose best suitable time

import random 

time = ["Morning","Afternoon","Evening","Night"]
probability = [0.7,0.4,0.6,0.2]
print("Usually I take tea at : ",random.choices(time,probability))