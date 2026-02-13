# lecture_polymphys_reptation

講義「高分子物理学特論」の#8「Entanglement Effects」で利用  

SingleChainDynamicsのプログラムを援用して、管の中に拘束された理想鎖とFH鎖、さらにSAW鎖を実装  

＜未解決問題＞  
元々FEを想定して作っていたので、RCを選んだときに初期に管に埋もれちゃっている時がある（260201修正済み）  
SAW鎖で実現してみたい（260213修正済み）  
重心が管から抜けたら終了するようなプログラムに変更したい（260201修正済み）  
それをさらに繰り返して統計ができるとなお良い（260202に理想鎖のみ対応済み、ただしNのスケーリングは微妙）  
（260213にSAWでも対応）  

＜260201コメント＞  
まず、上記未解決問題を一部対応  
SAW鎖のChain Dynamicsを実装できた  

＜260203コメント＞  
シミュレーション終了時のrep numberがそのまま菅更新時間と定義できるので、突貫工事だが繰り返しにも対応できた  （singleChainDynamics_Trapped_Ideal_stat_v3.py）  

＜202013コメント＞  
SAWのsegmentMotion(coordinate_list, radi, i)を作成している最中に  
updated_coordinate_list = coordinate_list.copy()  
を追加した。この修正をidealChainにも適用  