# zipファイルダウンロード
# 三四郎
# url = 'https://www.aozora.gr.jp/cards/000148/files/794_ruby_4237.zip'
# zip = '794_ruby_4237.zip'
# 日記帳
# url = 'https://www.aozora.gr.jp/cards/001779/files/57190_ruby_58233.zip'
# zip = '57190_ruby_58233.zip'
# 山月記
url = 'https://www.aozora.gr.jp/cards/000119/files/624_ruby_5668.zip'
zip = '624_ruby_5668.zip'


import urllib.request
urllib.request.urlretrieve(url, zip)

# ダウンロードしたzipの解凍
import zipfile
with zipfile.ZipFile(zip, 'r') as myzip:
    myzip.extractall()
    # 解凍後のファイルからデータ読み込み
    for myfile in myzip.infolist():
        # 解凍後ファイル名取得
        filename = myfile.filename
        # ファイルオープン時にencodingを指定してsjisの変換をする
        with open(filename, encoding='sjis') as file:
            text = file.read()

# ファイル整形
import re
# ヘッダ部分の除去
text = re.split('\-{5,}',text)[2]
# フッタ部分の除去
text = re.split('底本：',text)[0]
# | の除去
text = text.replace('|', '')
# ルビの削除
text = re.sub('《.+?》', '', text)
# 入力注の削除
text = re.sub('［＃.+?］', '',text)
# 空行の削除
text = re.sub('\n\n', '\n', text)
text = re.sub('\r', '', text)

#形態素解析
import MeCab

mecab = MeCab.Tagger("-Ochasen")
words = []

# テキストを引数として、形態素解析の結果、名詞・動詞・形容詞(原形)のみを配列で抽出する関数を定義
def extract_words(text):
    node = mecab.parseToNode(text)
    while node:
        word = node.feature.split(",")[6] #原形
        word_type = node.feature.split(",")[0] #品詞
        #print(word + ": " + word_type)
        if word_type in ["名詞", "動詞", "形容詞"]:
            words.append(word)
            #print(word)
        node = node.next
    return words

# 全体のテキストを句点('。')で区切った配列にする。
sentences = text.split('。')
# それぞれの文章を単語リストに変換(処理に数分かかります)
word_list = [extract_words(sentence) for sentence in sentences]

# 学習開始
# Word2Vecライブラリのロード
from gensim.models import word2vec

# size: 圧縮次元数
# min_count: 出現頻度の低いものをカットする
# window: 前後の単語を拾う際の窓の広さを決める
# iter: 機械学習の繰り返し回数(デフォルト:5)十分学習できていないときにこの値を調整する
# model.wv.most_similarの結果が1に近いものばかりで、model.dict['wv']のベクトル値が小さい値ばかりの
# ときは、学習回数が少ないと考えられます。
# その場合、iterの値を大きくして、再度学習を行います。

# 事前準備したword_listを使ってWord2Vecの学習実施
model = word2vec.Word2Vec(word_list, size=100,min_count=5,window=5,iter=100)

# モデルの保存
model.save("./sangetsuki.model")

# 結果の確認1
# 一つ一つの単語は100次元のベクトルになっています。
# 「世間」のベクトル値を確認します。
print(model.__dict__['wv']['虎'])