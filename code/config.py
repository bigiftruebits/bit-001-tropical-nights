"""Every path and methodological choice in one place.

Paths are relative to the package root, so the package runs wherever it is
unpacked. Change RAW only if you rebuild data/ from the public downloads.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"            # shared intermediate data (included)
RAW = ROOT / "raw"              # public raw downloads (not included; see README)
FIGURES = ROOT / "figures"      # output of make_fig*.py

THRESHOLD_C = 20.0              # tropical-night threshold, °C
SLEEP_HOURS = 8                 # hours of relief = of the 8 coldest hours, how many < 20 °C
MAX_SNAP_KM = 50.0              # population further than this from any land cell is dropped
FRAME = (-10.0, 34.0, 30.0, 47.2)   # Figure 3 map frame: W, S, E, N

# The eight Southern European EU member states counted in the aggregate.
COUNTRIES = [
    dict(key="portugal", ne_name="Portugal", geostat="PT"),
    dict(key="spain",    ne_name="Spain",    geostat="ES"),
    dict(key="italy",    ne_name="Italy",    geostat="IT"),
    dict(key="malta",    ne_name="Malta",    geostat="MT"),
    dict(key="slovenia", ne_name="Slovenia", geostat="SI"),
    dict(key="croatia",  ne_name="Croatia",  geostat="HR"),
    dict(key="greece",   ne_name="Greece",   geostat="EL"),
    dict(key="bulgaria", ne_name="Bulgaria", geostat="BG"),
]
