"""Testy převodu marsovských souřadnic (tools/mars.py)."""

import math
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tools import mars  # noqa: E402


def test_round_trip_returns_original_gps():
    """Převod GPS -> MARS -> GPS vrátí původní souřadnice."""
    latitude, longitude = 49.8201, 15.4755

    x, y = mars.to_mars(latitude, longitude)
    lat2, lon2 = mars.to_gps(x, y)

    assert lat2 == pytest.approx(latitude, abs=1e-7)
    assert lon2 == pytest.approx(longitude, abs=1e-7)


def test_nearby_points_differ_significantly():
    """Posun o ~111 m na sever dá stovky marsovských metrů (jako v Kotlinu)."""
    ax, ay = mars.to_mars(49.8175, 15.4730)
    bx, by = mars.to_mars(49.8185, 15.4730)

    distance = math.hypot(bx - ax, by - ay)
    assert distance > 100.0


def test_base_point_maps_to_offset():
    """Referenční bod se mapuje na posun počátku."""
    x, y = mars.to_mars(mars.BASE_LAT, mars.BASE_LON)

    assert x == pytest.approx(mars.OFFSET_X)
    assert y == pytest.approx(mars.OFFSET_Y)
