package cz.burlog.tabor.mps

import org.junit.Assert.assertEquals
import org.junit.Test

class MarsCoordsTest {

    @Test
    fun roundTripReturnsOriginalGps() {
        val lat = 49.8201
        val lon = 15.4755

        val mars = MarsCoords.toMars(lat, lon)
        val (lat2, lon2) = MarsCoords.toGps(mars)

        assertEquals(lat, lat2, 1e-6)
        assertEquals(lon, lon2, 1e-6)
    }

    @Test
    fun basePointMapsToOffset() {
        val mars = MarsCoords.toMars(MarsConfig.BASE_LAT, MarsConfig.BASE_LON)

        assertEquals(MarsConfig.OFFSET_X, mars.x, 1e-6)
        assertEquals(MarsConfig.OFFSET_Y, mars.y, 1e-6)
    }

    @Test
    fun nearbyPointsDifferSignificantly() {
        val a = MarsCoords.toMars(49.8175, 15.4730)
        val b = MarsCoords.toMars(49.8185, 15.4730)

        // ~111 m na severu * scale 2.37 -> stovky marsovskych metru
        val dy = b.y - a.y
        val dx = b.x - a.x
        assertEquals(true, kotlin.math.hypot(dx, dy) > 100.0)
    }
}
