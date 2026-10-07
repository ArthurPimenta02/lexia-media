"""Render Lexia post HTML files to Instagram-ready JPGs (1080x1350).

Each HTML file is a standalone page whose root element is a fixed
1080x1350 box. Logos are referenced as ASSETS/<file> and resolved to
brand/assets/ at render time.

Usage (from the repo root):
    python3 tools/render.py posts/2026-10-08-am/src posts/2026-10-08-am
Renders every *.html in the source folder, in name order, to
01.jpg, 02.jpg, ... in the output folder, plus a contact sheet
(_sheet.jpg) for a quick visual check.
"""
import pathlib
import sys

from PIL import Image
from playwright.sync_api import sync_playwright

W, H = 1080, 1350
REPO = pathlib.Path(__file__).resolve().parent.parent
ASSETS_URI = (REPO / "brand" / "assets").as_uri() + "/"


def show(path: pathlib.Path) -> str:
    """Path relative to the repo when inside it, else absolute."""
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


def main(src_dir: str, out_dir: str) -> None:
    src = pathlib.Path(src_dir).resolve()
    out = pathlib.Path(out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    pages = sorted(src.glob("*.html"))
    if not pages:
        sys.exit(f"No .html files in {src}")

    rendered = []
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--allow-file-access-from-files"])
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for i, html_path in enumerate(pages, 1):
            html = html_path.read_text().replace("ASSETS/", ASSETS_URI)
            tmp = src / f"_render_tmp_{i}.html"
            tmp.write_text(html)
            try:
                page.goto(tmp.as_uri(), wait_until="networkidle")
                page.evaluate("document.fonts.ready")
                page.wait_for_timeout(400)
                png = out / f"_{i:02d}.png"
                page.screenshot(path=str(png), clip={"x": 0, "y": 0, "width": W, "height": H})
                jpg = out / f"{i:02d}.jpg"
                Image.open(png).convert("RGB").save(jpg, quality=95)
                png.unlink()
                rendered.append(jpg)
                print(f"rendered {html_path.name} -> {show(jpg)}")
            finally:
                tmp.unlink(missing_ok=True)
        browser.close()

    # Contact sheet for visual review (not published).
    cols = min(4, len(rendered))
    rows = (len(rendered) + cols - 1) // cols
    tw, th = 540, 675
    sheet = Image.new("RGB", (cols * (tw + 10) + 10, rows * (th + 10) + 10), "#777777")
    for idx, jpg in enumerate(rendered):
        thumb = Image.open(jpg).resize((tw, th))
        sheet.paste(thumb, (10 + (idx % cols) * (tw + 10), 10 + (idx // cols) * (th + 10)))
    sheet.save(out / "_sheet.jpg", quality=85)
    print(f"contact sheet -> {show(out / '_sheet.jpg')}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
