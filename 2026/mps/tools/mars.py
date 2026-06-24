#!/usr/bin/env python3
"""Převod mezi pozemskou GPS a marsovskými souřadnicemi MPS.

Pořadatelský nástroj k aplikaci MPS. Implementuje stejnou afinní
transformaci jako MarsCoords.kt, takže z čísel MARS-X/MARS-Y, která hráč
přečte v mobilu, lze zpětně dopočítat skutečnou GPS.

NOTE(burlog): konstanty níže musí být shodné s MarsConfig v
app/src/main/java/cz/burlog/tabor/mps/MarsCoords.kt
"""

import argparse
import math

# tajné konstanty marsovského pozičního systému (viz MarsConfig.kt)
BASE_LAT = 49.81750
BASE_LON = 15.47300
SCALE = 2.37
ROTATION_DEG = 31.0
OFFSET_X = 100_000.0
OFFSET_Y = 250_000.0

# konstanty lokální projekce do metrů
METERS_PER_DEG_LAT = 111_132.0
METERS_PER_DEG_LON_EQ = 111_320.0


def _projection() -> tuple[float, float, float]:
    # předpočítané hodnoty rotace a délkového měřítka
    rot = math.radians(ROTATION_DEG)
    lon_scale = math.cos(math.radians(BASE_LAT)) * METERS_PER_DEG_LON_EQ
    return math.cos(rot), math.sin(rot), lon_scale


def to_mars(latitude: float, longitude: float) -> tuple[float, float]:
    """GPS (stupně) -> marsovské souřadnice (marsovské metry)."""
    cos_r, sin_r, lon_scale = _projection()

    # lokální projekce do metrů vůči referenčnímu bodu
    east = (longitude - BASE_LON) * lon_scale
    north = (latitude - BASE_LAT) * METERS_PER_DEG_LAT

    # rotace os a škálování s posunem počátku
    rx = east * cos_r - north * sin_r
    ry = east * sin_r + north * cos_r
    return OFFSET_X + SCALE * rx, OFFSET_Y + SCALE * ry


def to_gps(mars_x: float, mars_y: float) -> tuple[float, float]:
    """Marsovské souřadnice -> GPS (stupně). Inverze to_mars()."""
    cos_r, sin_r, lon_scale = _projection()

    # odstranění posunu a měřítka, poté zpětná rotace
    rx = (mars_x - OFFSET_X) / SCALE
    ry = (mars_y - OFFSET_Y) / SCALE
    east = rx * cos_r + ry * sin_r
    north = -rx * sin_r + ry * cos_r

    # zpětná projekce z metrů na stupně
    longitude = BASE_LON + east / lon_scale
    latitude = BASE_LAT + north / METERS_PER_DEG_LAT
    return latitude, longitude


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Převod mezi GPS a marsovskými souřadnicemi MPS.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # GPS -> MARS
    p_mars = sub.add_parser("to-mars", help="GPS (lat lon) -> MARS-X MARS-Y")
    p_mars.add_argument("latitude", type=float)
    p_mars.add_argument("longitude", type=float)

    # MARS -> GPS
    p_gps = sub.add_parser("to-gps", help="MARS-X MARS-Y -> GPS (lat lon)")
    p_gps.add_argument("mars_x", type=float)
    p_gps.add_argument("mars_y", type=float)

    return parser


def main() -> None:
    args = _build_parser().parse_args()

    # výpis výsledku podle zvoleného směru převodu
    if args.command == "to-mars":
        x, y = to_mars(args.latitude, args.longitude)
        print(f"MARS-X: {x:.1f}  MARS-Y: {y:.1f}")
    else:
        latitude, longitude = to_gps(args.mars_x, args.mars_y)
        print(f"GPS: {latitude:.6f}, {longitude:.6f}")


if __name__ == "__main__":
    main()
