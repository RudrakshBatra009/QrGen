qrgen is a small CLI tool i made for generating QR codes from the terminal instead of using some sketchy website that probably tracks what you're encoding. Just pass it text or a url and it spits out a png. I got tired of alt-tabbing to a browser every time i needed a quick QR for wifi credentials or a link, so now it's just one command.

It auto-names the file based on what you're encoding so you don't have to think of a filename every time, but you can override that too. Also does colors, size, error correction levels, all that.

Writing this part myself too so it don't get flagged as ai readme again.

Features

* Generate a QR code from any text or URL
* Auto-names the output file based on the content (or set your own with `-o`)
* Adjustable size, border thickness, and error correction level
* Custom foreground/background colors (any hex code)
* Won't overwrite existing files — auto-numbers instead
* Optional `--show` to pop the image open right after saving

Usage

Basic:

```
qrgen "https://example.com"

```

Save with a specific filename:

```
qrgen "https://example.com" -o mycode.png

```

Save into a specific folder:

```
qrgen "https://example.com" --dir ~/Desktop/codes

```

Bigger or smaller code (box size in pixels per module, default 10):

```
qrgen "https://example.com" --size 15

```

Adjust the border (default 4, which is the QR spec minimum):

```
qrgen "https://example.com" --border 2

```

Higher error correction, useful if the code's going to get printed, stickered somewhere, or handled a lot:

```
qrgen "https://example.com" --ec high

```

Levels are `low` (~7%), `medium` (~15%, default), `quartile` (~25%), `high` (~30%).

Custom colors:

```
qrgen "https://example.com" --fg "#1a1a1a" --bg "#f5f5f5"

```

Open it right after saving:

```
qrgen "https://example.com" --show

```

Flags combine fine. For example, a big high-EC code with custom colors, saved to a folder:

```
qrgen "https://mysite.com/wifi" --size 12 --ec high --fg "#003366" --dir ~/codes --show

```

Example output

```
qrgen

  text     : https://example.com
  length   : 20 chars
  grid     : 25x25 modules
  ec level : medium
  size     : 290x290 px
  saved    : /home/user/example_com.png

```

Installing it globally

macOS / Linux

```
mkdir -p ~/.local/bin
cp qrgen.py ~/.local/bin/qrgen
chmod +x ~/.local/bin/qrgen
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc

```

On Linux with bash, swap `~/.zshrc` for `~/.bashrc`.

You'll also need the `qrcode` lib installed:

```
pip install qrcode[pil]

```

Windows

```
mkdir C:\tools
copy qrgen.py C:\tools\

```

Create `C:\tools\qrgen.bat`:

```
@echo off
python "%~dp0qrgen.py" %*

```

Add it to your PATH:

```
setx PATH "%PATH%;C:\tools"

```

Reopen your terminal afterward.