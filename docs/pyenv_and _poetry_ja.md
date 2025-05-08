## pyenv と poetryを使う

ここでは、Pythonのバージョン管理と仮想環境の管理を行なうためにpyenvとpoetryを導入する方法を説明する。Minecraft Remote(マイクラリモコン）を使う上で必須 ではないが、強くオススメ。

--

**pyenvだけでも入れよう。**
- 「Pythonのインストール」のためだけに、公式インストーラーの代わりに使っても良い。
- ただし、linuxやmacOSの場合は、poetryも使うことを推奨。システムもPythonを使っているため、独立しておいたほうが安心。


---

## まず、用語がわからないが？

- **pyenv** ：Pythonのバージョン管理ツール
- **poetry** ：Pythonのパッケージ管理ツールであり、仮想環境の管理も行う。
- **パッケージ** ：「拡張機能のようなもの」
ライブラリや、モジュールと呼んだりもする、初学者泣かせなややこしい存在。
- **仮想環境** ：プロジェクトごとに異なる依存関係を管理するための独立したPython環境。


**厳密な定義ではなく、ここでの使い方に沿った、わかりやすい捉え方なので、注意。**

---

## オススメ導入ステップ

- ステップ１：
  - pyenvを導入。
  - 仮想環境なし。
  - Pythonのバージョンは、3.10.11、3.11.9、3.12.10。
(それぞれのマイナーバージョンの最終版)
  - **基本的には、3.11.9を使う。**

--

- ステップ２：
  - poetryを導入。(扱うプロジェクトが増えてきたら。)
  - 仮想環境あり。
  - pyenvだけ使うプロジェクトも有って良い。

poetryを必須と考えなくて良いのでラク。

**初心者のうちは、プロジェクト間で依存関係がぶつかる可能性が低いため、poetryが必須ではない。**


---

## Python仮想環境(ふたたび)

Python自体とそのPythonが使うライブラリを、他のプロジェクトと分離して管理するための仕組み。システム全体の開発環境を汚すこともなく、プロジェクト同士も干渉が起きない。

pyenvでPython仮想環境を作成することもできるが、その部分はpoetryに任せる。

---

## pyenvのインストール

### Windowsの場合

**Git Bash**で、

```bash
# インストール
git clone https://github.com/pyenv-win/pyenv-win.git "$HOME/.pyenv"
```

**PowerShell**で、

```powershell
# pathを設定する。
[System.Environment]::SetEnvironmentVariable('PYENV',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
[System.Environment]::SetEnvironmentVariable('PYENV_ROOT',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
[System.Environment]::SetEnvironmentVariable('PYENV_HOME',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
[System.Environment]::SetEnvironmentVariable('path', $env:USERPROFILE + "\.pyenv\pyenv-win\bin;" + $env:USERPROFILE + "\.pyenv\pyenv-win\shims;" + [System.Environment]::GetEnvironmentVariable('path', "User"),"User")
```


--

### Ubuntuの場合

```bash
# ビルド環境をインストール
sudo apt install build-essential libffi-dev libssl-dev zlib1g-dev liblzma-dev libbz2-dev   libreadline-dev libsqlite3-dev libopencv-dev tk-dev git
```

```bash
# pyenv インストール
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
# 終了するまで、ちょっと時間がかかるが待つこと。
# 待たないで失敗することが多い。
```

```bash
# path設定
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc

# 反映させる
source ~/.bashrc
```

--


### macOSの場合

```bash
# Homebrewでインストールするのが簡単。
brew install pyenv
brew install xz
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

---

## Pythonをインストール

```bash
# ターミナルを再起動して、以下のコマンドを実行する。
pyenv install 3.10.11 3.11.9 3.12.10
pyenv global 3.11.9

python -V
```

---

## poetryのインストール

### Windowsの場合

