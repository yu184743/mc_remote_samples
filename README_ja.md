# minecraft_remote_samples / Naohiro2g

Minecraft Remote（マイクラリモコン）のAPIを使いPythonでユーザーコードを書く出発点

---

[Minecraft Remote（`McRemote`）プラグイン](https://github.com/Naohiro2g/McRemote)をインストールした[PaperMC](https://papermc.io/)サーバーが必要です。ご心配なく、箱庭（サンドボックス）サーバーを利用して始められます。

<img src="https://raw.githubusercontent.com/Naohiro2g/minecraft-remote-api/refs/heads/main/images/mc-remote.png" width="480" alt="Minecraft Remote World" title="Minecraft Remote World" />

---

## 箱庭サーバーの利用

- サーバー情報
  - アドレス: `mc-remote.xgames.jp`
  - ポート: `25565` （指定不要）

- クライアント アプリ（マルチモード）
  - Java / Fabric / NeoForge / Forge 1.8.8〜最新
  - Bedrock（iOS / Android / Windowsを含む）
  - 推奨セットアップ:

    [`Iris`](https://irisshaders.github.io/) / Fabric と [`MakeUp - Ultra Fast`](https://modrinth.com/shader/makeup-ultra-fast-shaders/changelog?l=iris) シェーダー

---

## 非常に重要な準備作業

`param_mc_remote.py`のパラメータを自分の環境に合わせて編集する必要があります。

```python
PLAYER_NAME = "PLAYER_NAME"  # set your player name in Minecraft

PLAYER_ORIGIN = Vec3(2000, 0, 2000)  # PO.x, PO.y, PO.z

ADRS_MCR = "mc-remote.xgames.jp"  # mc-remote sandbox server
PORT_MCR = 25575  # socket server port
```

---

- **APIを利用するには、PLAYER_NAME と同じ名前でMinecraftサーバーに参加している必要があります。**


 箱庭サーバーで始めよう！（デフォルト設定）
  - **マイクラリモコンサーバー 設定**
    - **`ADRS_MCR`**: `mc-remote.xgames.jp`
    - **`PORT_MCR`**: `25575`
  - **マイクラ サーバー情報**
    - サーバーアドレス: `mc-remote.xgames.jp`
    - ポート番号: `25565` （指定不要）

家庭、教室などに自分のサーバーを準備すると、より楽しい体験ができるかも。

--

- **`PLAYER_ORIGIN` は建築座標系の原点**となり、設定値からの相対座標でブロックが配置されます。
   - たとえば、
     - `PLAYER_ORIGIN`： `(2000, 0, 2000)`
     - コマンド： `setBlock(5, 68, 5, block.GOLD_BLOCK)`
     - 結果: `(2005, 68, 2005)` に金ブロック出現

---

### 自前のサーバーを準備する場合：

これらのパラメータを設定してください。


- **`ADRS_MCR`**：
  マイクラリモコンサーバーのアドレスで、マインクラフトサーバーと同じです。
- **`PORT_MCR`**：
　マイクラリモコンサーバーのポート番号です。デフォルト値は `25575` ですが、`plugins/McRemote/config.yml` で変更できます。

---

### Discordコミュニティに参加しよう！

マイクラリモコン専用のDiscordコミュニティでは、他のユーザーと経験を共有したりできます。

箱庭サーバーやAPIの使い方、サーバーの建て方などについて質問がある場合は、[Discordサーバー](https://discord.gg/xUqhhqWsuS)内の `mc-remote-chat` チャンネルをご利用ください。

---

## インストールと更新

このパッケージの最新版は [PyPI](https://pypi.org/project/minecraft-remote-api/) からインストールできます。

#### pyenv / poetryがインストールされている場合

```bash
poetry install


# 仮想環境(.venv/)が作成されたのを確認し、今後は、その環境内で作業してください。
```

パッケージを更新するには、次のコマンドを実行:

```bash
poetry update
```

--

#### pyenv / poetryがインストールされていない場合

Python 3.9以上がインストールされていることを確認して、次のコマンドを実行:

```bash
pyenv local 3.11.9  # もし、pyenvをインストール済みなら
pip install minecraft-remote-api
```

（他の用途も考慮すると、現在は、Python 3.11.9, 3.12.10が推奨です。）

パッケージを更新するには、次のコマンドを実行:

```bash
pip install minecraft-remote-api -U
```

パッケージ管理のためにpyenv / poetryを使うことをオススメします。少なくとも、pyenvを使うとPythonのバージョン管理が楽になります。

pyenv / poetryのインストール方法は、[こちら](https://github.com/Naohiro2g/minecraft-remote-api/docs/pyenv_and_poetry_ja.md)を参照してください。

---

## サンプルを実行

```bash
cd examples
python hello.py
python axis_flat.py
```

---

## Minecraft Remoteプロジェクトについて

詳しくは、[ミッション](docs/mission_ja.md) ドキュメントを参照してください。

--

「hacking, coding, tinkering = ハッキング、コーディング、ティンカリング」は、このプロジェクトの核心です。私たちはユーザーが自らの経験を通じて探求し学ぶことができるシステムを作成することを目指しています。このプロジェクトは誰にでも開かれており、私たちのビジョンを共有するすべての人からの貢献を歓迎します。

<img src="https://raw.githubusercontent.com/Naohiro2g/minecraft-remote-api/refs/heads/main/images/hacking_coding_tinkering.png" width="480" alt="Hacking Coding Tinkering" title="Hacking Coding Tinkering" />
