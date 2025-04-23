# minecraft_remote_samples / Naohiro2g

Starting point for writing Minecraft Remote user code in Python with its API


---

You need a [Paper](https://papermc.io/) Minecraft Server with the [Minecraft Remote (`McRemote`) plugin](https://github.com/Naohiro2g/McRemote) installed. However, you can also start with our Sandbox Server.

<img src="https://raw.githubusercontent.com/Naohiro2g/minecraft-remote-api/refs/heads/main/images/mc-remote.png" width="480" alt="Minecraft Remote World" title="Minecraft Remote World" />

--

## the Sandbox Server

- Server Information
  - address: `mc-remote.xgames.jp`
  - port: `25565` (No need to specify.)

- Minecraft Client (Multiplayer Mode)
  - Java / Fabric / NeoForge / Forge 1.8.8 - latest
  - Bedrock including iOS / Android / Windows
  - Recommended setup:

    [`Iris`](https://irisshaders.github.io/) / Fabric with [`MakeUp - Ultra Fast`](https://modrinth.com/shader/makeup-ultra-fast-shaders/changelog?l=iris) shader


---

## Very Important Preparation

Edit these parameters in `param_mc_remote.py` to suit your environment.

```python
PLAYER_NAME = "PLAYER_NAME"  # set your player name in Minecraft

PLAYER_ORIGIN = Vec3(2000, 0, 2000)  # PO.x, PO.y, PO.z

ADRS_MCR = "mc-remote.xgames.jp"  # mc-remote sandbox server
PORT_MCR = 25575  # Minecraft Remote server port
```

--

- **To use this API, you must be joined to the Minecraft server as the same name as `PLAYER_NAME` and the server has mc-remote plugin installed.** Please use the Sandbox Server with the default values for getting started.
  - **Minecraft Remote Server Settings**
    - **`ADRS_MCR`**: `mc-remote.xgames.jp`
    - **`PORT_MCR`**: `25575`
  - **Minecraft Server Information**
    - address: `mc-remote.xgames.jp`
    - port: `25565` (No need to specify)

--

- **`PLAYER_ORIGIN` defines the origin of the building coordinate system.** Building coordinates are computed relative to this origin.
   - For example,
     - `PLAYER_ORIGIN`: `(2000, 0, 2000)`
     - command: `setBlock(5, 68, 5, block.GOLD_BLOCK)`
     - result: a gold block at `(2005, 68, 2005)`

---

### If you are using your own server:

Set these parameters for your server.


- **`ADRS_MCR`** is the address of the Minecraft Remote Server, which is the same as of Minecraft Server.

- **`PORT_MCR`** is the port for the Minecraft Remote Server. The default value is `25575`, but you can change it to any port you like in the `plugins/McRemote/config.yml`.



---

If you are using your own PaperMC server, be sure to load the `McRemote` plugin. While running the server on your own PC offers a compact setup, if your PC is underpowered, it is preferable to use a server on another machine.

---

### Join Our Discord Community !!

We have a Discord community for Minecraft Remote to share your experiences with other users.

If you have questions about the Sandbox Server, API usage, or how to set up your own server, please visit the `mc-remote-chat` channel on [our Discord server](https://discord.gg/xUqhhqWsuS) for support.

---

## Installation and Update

The package of Client / API is registered on [PyPI](https://pypi.org/project/minecraft-remote-api/).


#### If you have pyenv / poetry installed

```bash
poetry install

# Make sure the virtual environment (.venv/) is created,
# and from now on, please work in that environment.
```

To update the package, run:

```bash
poetry update
```

--

#### If you don't have pyenv / poetry installed

```bash
pip install minecraft-remote-api
```

To update the package, run:

```bash
pip install minecraft-remote-api -U
```

It is recommended to use `pyenv` and `poetry` for package management, or at least to use pyenv for Python version management.

---

## Run Examples

```bash
cd examples
python hello.py
python axis_flat.py
```

---


## About the Minecraft Remote Project

Please refer to the [mission](docs/mission_en.md)  documents for more information.

<img src="https://raw.githubusercontent.com/Naohiro2g/minecraft-remote-api/refs/heads/main/images/hacking_coding_tinkering.png" width="480" alt="Hacking Coding Tinkering" title="Hacking Coding Tinkering" />
