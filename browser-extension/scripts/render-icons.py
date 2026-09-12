from pathlib import Path
import cairosvg

ROOT = Path(__file__).resolve().parents[1]
svg = ROOT / 'assets' / 'icon.svg'
out = ROOT / 'assets'
out.mkdir(exist_ok=True)
for size in (16, 32, 48, 128):
    cairosvg.svg2png(url=str(svg), write_to=str(out / f'icon{size}.png'), output_width=size, output_height=size)
print('Generated icon PNG set: 16, 32, 48, 128')
