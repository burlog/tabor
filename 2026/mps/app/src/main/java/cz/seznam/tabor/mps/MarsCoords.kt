package cz.seznam.tabor.mps

import kotlin.math.cos
import kotlin.math.sin

/**
 * Tajné konstanty marsovského pozičního systému.
 *
 * POZOR: Tyto hodnoty si před hrou změň! Kdo je zná, dokáže z marsovských
 * souřadnic zpětně dopočítat skutečnou GPS (viz [MarsCoords.toGps]).
 * Hráč, který zná jen výsledná čísla MARS-X / MARS-Y, je odvodit nedokáže.
 */
object MarsConfig {
    /** Referenční bod (např. střed tábora) ve stupních. */
    const val BASE_LAT = 49.81750
    const val BASE_LON = 15.47300

    /** Měřítko – kolika "marsovskými metry" odpovídá jeden pozemský metr. */
    const val SCALE = 2.37

    /** Rotace souřadných os ve stupních. */
    const val ROTATION_DEG = 31.0

    /** Posun počátku, aby čísla nezačínala u nuly. */
    const val OFFSET_X = 100_000.0
    const val OFFSET_Y = 250_000.0
}

/** Marsovská souřadnice v "marsovských metrech". */
data class MarsPoint(val x: Double, val y: Double)

/**
 * Převod mezi pozemskou GPS (lat/lon) a marsovskými souřadnicemi.
 *
 * Transformace je afinní: lokální projekce do metrů → škálování → rotace →
 * posun. Je plně reverzibilní (pro pořadatele), ale z výsledných čísel není
 * snadné odvodit původní GPS bez znalosti konstant v [MarsConfig].
 */
object MarsCoords {

    private const val METERS_PER_DEG_LAT = 111_132.0
    private const val METERS_PER_DEG_LON_EQ = 111_320.0
    private const val DEG_TO_RAD = Math.PI / 180.0

    private val rot = MarsConfig.ROTATION_DEG * DEG_TO_RAD
    private val cosR = cos(rot)
    private val sinR = sin(rot)
    private val lonScale = cos(MarsConfig.BASE_LAT * DEG_TO_RAD) * METERS_PER_DEG_LON_EQ

    /** GPS (stupně) → marsovské souřadnice. */
    fun toMars(latitude: Double, longitude: Double): MarsPoint {
        val east = (longitude - MarsConfig.BASE_LON) * lonScale
        val north = (latitude - MarsConfig.BASE_LAT) * METERS_PER_DEG_LAT

        val rx = east * cosR - north * sinR
        val ry = east * sinR + north * cosR

        return MarsPoint(
            x = MarsConfig.OFFSET_X + MarsConfig.SCALE * rx,
            y = MarsConfig.OFFSET_Y + MarsConfig.SCALE * ry,
        )
    }

    /** Marsovské souřadnice → GPS (stupně). Inverze [toMars] – pro pořadatele. */
    fun toGps(mars: MarsPoint): Pair<Double, Double> {
        val rx = (mars.x - MarsConfig.OFFSET_X) / MarsConfig.SCALE
        val ry = (mars.y - MarsConfig.OFFSET_Y) / MarsConfig.SCALE

        val east = rx * cosR + ry * sinR
        val north = -rx * sinR + ry * cosR

        val longitude = MarsConfig.BASE_LON + east / lonScale
        val latitude = MarsConfig.BASE_LAT + north / METERS_PER_DEG_LAT
        return latitude to longitude
    }
}
