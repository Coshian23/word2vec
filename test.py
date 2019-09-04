from gensim.models import word2vec

model = word2vec.Word2Vec.load("./nikkityou.model")

print(model.__dict__['wv']['兄'])

results = model.wv.most_similar(positive=['病気'])
for result in results:
    print(result)