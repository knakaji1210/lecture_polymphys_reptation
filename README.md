# lecture_polymphys_reptation

講義「高分子物理学特論」の#8「Entanglement Effects」で利用

SingleChainDynamicsのプログラムを援用して、管の中に拘束された理想鎖とFH鎖をシミュレートしただけ、まだ沢山修正が必要

＜未解決問題＞
元々FEを想定して作っていたので、RCを選んだときに初期に管に埋もれちゃっている時がある
SAW鎖で実現してみたい
重心が管から抜けたら終了するようなプログラムに変更したい
それをさらに繰り返して統計ができるとなお良い

以下プログラム中のコメントから
管の中のレプテーションを記述できるように修正
細い管にしても、理想だと縮んでいってしまう
ただし、少し飛び出させてradi=1で行うと、管更新が観察される場合もある！