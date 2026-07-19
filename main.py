#!/usr/bin/env python3
import sys, os, argparse
from pathlib import Path

try:
    import qrcode
except ImportError:
    print("missing qrcode lib. run: pip install qrcode[pil]")
    sys.exit(1)


# error correction levels - higher = more redundant data,
# survives more damage/dirt on the printed code but bigger
EC_LEVELS = {
    "low": qrcode.constants.ERROR_CORRECT_L,      # ~7%
    "medium": qrcode.constants.ERROR_CORRECT_M,    # ~15%, default
    "quartile": qrcode.constants.ERROR_CORRECT_Q,  # ~25%
    "high": qrcode.constants.ERROR_CORRECT_H,      # ~30%
}


def hex_to_rgb(hexcode):
    h = hexcode.lstrip("#")
    if len(h) == 3:
        h = "".join(c*2 for c in h)
    if len(h) != 6:
        return None
    try:
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def make_filename(text, custom_name):
    if custom_name:
        return custom_name if custom_name.endswith(".png") else custom_name + ".png"

    # build something readable from the text itself
    # strip protocol junk, keep it short, swap bad chars
    clean = text.replace("https://", "").replace("http://", "")
    clean = clean.replace("www.", "")

    # cut at first slash or query string so it's not a giant filename
    for sep in ["/", "?", "#"]:
        if sep in clean:
            clean = clean.split(sep)[0]
            break

    clean = clean[:40]  # don't let it get out of hand
    clean = "".join(c if c.isalnum() or c in "-_." else "_" for c in clean)
    clean = clean.strip("_")

    if not clean:
        clean = "qrcode"

    return f"{clean}.png"


def main():
    ap = argparse.ArgumentParser(
        prog="qrgen",
        description="generate a qr code from text or a url, saves as png"
    )

    ap.add_argument("text", help="text or url to encode")
    ap.add_argument("-o", "--out", default=None, help="output filename (default: auto-named from text)")
    ap.add_argument("--dir", default=".", help="folder to save into (default: current folder)")
    ap.add_argument("--size", type=int, default=10, help="box size in pixels per module (default: 10)")
    ap.add_argument("--border", type=int, default=4, help="border thickness in modules (default: 4, qr spec minimum)")
    ap.add_argument("--ec", default="medium", choices=list(EC_LEVELS.keys()), help="error correction level (default: medium)")
    ap.add_argument("--fg", default="#000000", help="foreground color as hex, e.g. #1a1a1a")
    ap.add_argument("--bg", default="#ffffff", help="background color as hex")
    ap.add_argument("--show", action="store_true", help="open the image after saving")

    args = ap.parse_args()

    if not args.text.strip():
        print("can't encode empty text")
        sys.exit(1)

    fg = hex_to_rgb(args.fg)
    bg = hex_to_rgb(args.bg)

    if fg is None:
        print(f"bad foreground color: {args.fg}")
        sys.exit(1)
    if bg is None:
        print(f"bad background color: {args.bg}")
        sys.exit(1)

    out_dir = Path(args.dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = make_filename(args.text, args.out)
    out_path = out_dir / filename

    # don't silently overwrite something that already exists
    if out_path.exists() and not args.out:
        n = 2
        stem = out_path.stem
        while out_path.exists():
            out_path = out_dir / f"{stem}_{n}.png"
            n += 1

    qr = qrcode.QRCode(
        version=None,  # auto-pick the smallest version that fits the data
        error_correction=EC_LEVELS[args.ec],
        box_size=args.size,
        border=args.border,
    )

    qr.add_data(args.text)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fg, back_color=bg)

    img.save(out_path)

    # rough info about what got encoded
    data_len = len(args.text)
    modules = qr.modules_count  # grid size, e.g. 25 means 25x25

    print(f"\nqrgen\n")
    print(f"  text     : {args.text[:60]}{'...' if len(args.text) > 60 else ''}")
    print(f"  length   : {data_len} chars")
    print(f"  grid     : {modules}x{modules} modules")
    print(f"  ec level : {args.ec}")
    print(f"  size     : {img.size[0]}x{img.size[1]} px")
    print(f"  saved    : {out_path}")
    print()

    if args.show:
        try:
            img.show()
        except Exception as e:
            print(f"  couldn't open image viewer: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\ncancelled")

