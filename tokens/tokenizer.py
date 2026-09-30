"""
tiktoken : Library for tokenizing text for OpenAI's models.
pip uninstall tiktoken
pip cache purge
pip install tiktoken
pip install --upgrade tiktoken
"""
import tiktoken

encoder1 = tiktoken.encoding_for_model("gpt-4o")
encder2 = tiktoken.encoding_for_model("gpt-3.5-turbo")
text = """Hi! How are you?"""
tokens1 = encoder1.encode(text)
tokens2 = encder2.encode(text)
print("Converted Tokens GPT-4o:", tokens1)
print("Converted Tokens:", tokens2)
print("Token count - GPT-4o:", len(tokens1)) ## Single line 6 tokens, multiple lines 9 tokens
print("Token count - GPT-3.5-turbo:", len(tokens2)) ## Single line 6 tokens, multiple lines 9 tokens
decoded_text = encoder1.decode(tokens1)
print(decoded_text)
decoded_text = encder2.decode(tokens2)
print(decoded_text)

### 
tokens = [112,112,676,877,9090] # can't convert negative int to unsigned
# Negative tovens are not valid, so we will ignore the negative token and decode the rest.
# 'Invalid token for decoding: 12615276
decoded_text = encoder1.decode(tokens)
print(decoded_text)
decoded_text = encder2.decode(tokens)
print(decoded_text)


print("Vocab size for GPT-4o:", encoder1.n_vocab) # 100000
print("Vocab size for GPT-3.5-turbo:", encder2.n_vocab) # 50257

tokens = [" 0x3039"]
print("Word : ", encoder1.decode([int(token, 16) for token in tokens])) # 12345

"""TikTokenizer : A tokenizer that uses the TikToken library for encoding and decoding text.
from tiktokenizer import TikTokenizer

tokenizer = TikTokenizer.create("cl100k_base")
tokens = tokenizer.encode("Hi")
print("Tokens:", tokens)
print("Token count:", len(tokens))
decoded_text = tokenizer.decode(tokens)
print("Decoded Text:", decoded_text)

"""