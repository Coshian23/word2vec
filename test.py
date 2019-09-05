from gensim.models import word2vec

model = word2vec.Word2Vec.load("./sangetsuki.model")

# print(model.__dict__['wv']['科挙'])

results = model.wv.most_similar(positive=['虎'])
for result in results:
    print(result)

print("")
model = word2vec.Word2Vec.load("./sangetsuki_correct.model")

# print(model.__dict__['wv']['科挙'])

results = model.wv.most_similar(positive=['虎'])
for result in results:
    print(result)

print("")
model = word2vec.Word2Vec.load("./sangetsuki_correct500.model")

# print(model.__dict__['wv']['科挙'])

results = model.wv.most_similar(positive=['自分'])
for result in results:
    print(result)