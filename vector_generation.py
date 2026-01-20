import math
import sys

message = ["I love Pizza", "Pizza is my favorite food", "I like to eat Pizza every day", "I enjoy playing football",
           "Football is a great sport", "I like reading books", "Books are a great source of knowledge",
           "I love to travel", "Traveling is my passion"]
vocabulary = list(set([words for sentence in message for words in sentence.lower().split()]))
vector_embedding = []

def simple_embedding(sentence,vocab):
    words = sentence.lower().split()
    vector = []
    for word in vocab:
        word_cnt = words.count(word)
        vector.append(word_cnt)
    return vector

vectors = [simple_embedding(sentence,vocabulary) for sentence in message]
for sentence, vec in zip(message, vectors):
    print(f"{sentence} : {vec}")

print("")
query = "Vector Embeddings"
query_vector = simple_embedding(query,vocabulary)
print(f"{query} : {query_vector}")

def cosine_similarity(vector1,vector2):
    dot = sum(a*b for a,b in zip(vector1,vector2))
    norm1 = math.sqrt(sum(a*a for a in vector1))
    norm2 = math.sqrt(sum(b*b for b in vector2))
    if norm1 == 0 or norm2 == 0:
        return 0
    else:
        return dot/(norm1*norm2)

similarities = [cosine_similarity(query_vector,vec) for vec in vectors]
if similarities.count(0) == len(similarities):
    print("No Matching Query !!")
    sys.exit(1)
best_match_index = similarities.index(max(similarities))
print("Query : ",query)
print("Similarity Score : ",similarities)
print("Best Matching document: ",message[best_match_index])
print("Best similarity Score : ",similarities[best_match_index])