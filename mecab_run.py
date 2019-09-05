import MeCab

mecab = MeCab.Tagger("-Ochasen")

# テキストを引数として、形態素解析の結果、名詞・動詞・形容詞(原形)のみを配列で抽出する関数を定義
def extract_words(text):
    node = mecab.parseToNode(text)
    words = []
    while node:
        word = node.feature.split(",")[6] #原形
        word_type = node.feature.split(",")[0] #品詞
        #print(word + ": " + word_type)
        if word_type in ["名詞", "動詞", "形容詞"]:
            words.append(word)
            #print(word)
        node = node.next
    return words

#  関数テスト
text = '三四郎は京都でちょっと用があって降りたついでに。誰かが困っている時に来るのです。'

# 全体のテキストを句点('。')で区切った配列にする。
sentences = text.split('。')
# それぞれの文章を単語リストに変換(処理に数分かかります)
word_list = [extract_words(sentence) for sentence in sentences]

# 結果の一部を確認
for word in word_list[1]:
    print(word)