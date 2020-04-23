# Algo Basic Dealer on Discord 
### はじめに
カードゲーム「[algo](https://www.sansu-olympic.gr.jp/algo/)」をDiscord上で遊べるようにしたものです。2人でのマルチプレイ専用となります。

### ルール
1. 0から11までのカードが白黒の2種類、計24枚ある。プレイヤーは最初に4枚ずつカードを配られ、相手に伏せて左から数字の小さい順に並べる。同じ数字の場合は、黒が小さいとする。

1. プレイヤーは山札から1枚手札を引き、相手の特定のカードの数字をあてる(これをアタックと呼ぶ)。

1. アタックが成功すると、あてられたカードは表を向けて並べる。この時、プレイヤーは続けてアタックをするか、アタックをやめて自分の手札を**相手に伏せて**並べるかを選ぶことができる。

1. アタックが失敗した場合、自分の手札を**表に向けて**並べる。アタックは相手の番に移る。

1. 2～4を続け、先に相手のカードをすべて表にしたものが勝者である。

詳しいルールは、https://www.sansu-olympic.gr.jp/algo/ を参照のこと。

### 使い方
botとの個人チャットで以下のように投稿する。

- `$create algo (4桁の数字)` …対戦するための部屋を作る。


- `$join algo (4桁の数字)`　…作られた部屋に入る。

- `$attack (a~l) (1~11の数字)` …アタックをする。a~lは、カードを指定するための識別子であり、生成される画像に示されている。

- `$hide` …アタックをやめ、手札を伏せる。

- `$help` …コマンドの操作方法などについての記述を返す。


- `$quit` …対戦を途中で棄権する場合に使う。

- `$mashiro` …おまけです。

### 環境
`Windows 10 Home (version:1903)`での動作を確認しています。
`Python 3.7.7`
`MySQL 8.0.19`
以下はPythonの外部ライブラリ
`discord.py 1.3.3`
`pymysql 0.9.3`

### 今後の予定
1. `$attack`をせずに`$hide`する禁止行為を防ぐ機能を実装する。
2. ユーザの勝敗数を記録し、ランキングを作る。

### お断り
本ソースコードの実行によって発生したいかなる損害に対しても責任は負いかねます。また、高負荷の係る環境での動作確認はしておりません。
 
# Algo Basic Dealer on Discord (for international readers)
Play a card game named "algo basic" on discord.

### Rule
See https://www.sansu-olympic.gr.jp/algo/ for detailed rules.
In your turn, guess the opponent's card number.
If you guess it successfully, you can continue guessing or hide your hand.
If your guess is failed, open your hand and an attacker changes.

### Usage
See https://github.com/kingofwhiterock/algo for detailed command description.
You should type a command starting with `$`!

`$create algo [0-9]{4}`
......Create multi-play room. A room number should be 4-digit integer.

`$join algo [0-9]{4}`
......Join a multi-play room which is already created.

`$attack [a-l] ([0-9]|1[01])`
......Attack the opponent's card with your hand.

`$hide`
......Stop attack and hide your current hand into your cards.
......Be careful that `$attack` should be done at least one time!

`$help`
......Open Algo Basic Dealer's help utility (this page).

`$quit`
......Quit the game. You lose automatically.

`$mashiro`
......Return a picture of Mashiro. See it and relax!

### System Requirement
Use `Python 3.7.0`or later.
Use `MySQL 8.0.0` or later.
Following library should be installed.
`discord.py == 1.3.3`
`pymysql == 0.9.3`

### Developing Utility
1. Develop checking hide-without-attack method.
2. Count a user's win-lose (ranking system).

### Caution
We don't bear any responsibility for using this source code.