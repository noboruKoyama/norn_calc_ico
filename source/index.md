# 概要
- API対して処理することで

# 詳細
## ファイルリスト
- getdata.cgi
    - tradeデータを取得してDBに格納
- estimate.cgi
    - 固定のディレクトリにcsvを設置してそれをtradeデータに取り込む仕組み
    - 取り込みの処理を作るためのテストに使ったもの
- getdata_payment.cgi
    - payment_historyを登録
    - 画面(ログ)にも出力する