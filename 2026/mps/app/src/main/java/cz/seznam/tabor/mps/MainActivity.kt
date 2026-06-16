package cz.seznam.tabor.mps

import android.Manifest
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import android.os.Bundle
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import cz.seznam.tabor.mps.databinding.ActivityMainBinding
import java.util.Locale

class MainActivity : AppCompatActivity(), LocationListener {

    private lateinit var binding: ActivityMainBinding
    private lateinit var locationManager: LocationManager

    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { result ->
        val granted = result[Manifest.permission.ACCESS_FINE_LOCATION] == true ||
            result[Manifest.permission.ACCESS_COARSE_LOCATION] == true
        if (granted) startLocationUpdates()
        else binding.status.text = getString(R.string.status_no_permission)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)
        locationManager = getSystemService(LOCATION_SERVICE) as LocationManager
    }

    override fun onResume() {
        super.onResume()
        if (hasLocationPermission()) {
            startLocationUpdates()
        } else {
            permissionLauncher.launch(
                arrayOf(
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION,
                )
            )
        }
    }

    override fun onPause() {
        super.onPause()
        locationManager.removeUpdates(this)
    }

    private fun hasLocationPermission(): Boolean =
        ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) ==
            PackageManager.PERMISSION_GRANTED ||
            ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) ==
            PackageManager.PERMISSION_GRANTED

    private fun startLocationUpdates() {
        if (!hasLocationPermission()) return

        // používáme výhradně GPS, síťovou (nepřesnou) polohu ignorujeme
        if (!locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER)) {
            showUnavailable()
            return
        }

        binding.status.text = getString(R.string.status_searching)
        locationManager.requestLocationUpdates(
            LocationManager.GPS_PROVIDER, 1000L, 0f, this
        )
        locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER)
            ?.let(::showLocation)
    }

    private fun showUnavailable() {
        binding.marsX.text = getString(R.string.placeholder)
        binding.marsY.text = getString(R.string.placeholder)
        binding.accuracy.text = getString(R.string.placeholder)
        binding.status.text = getString(R.string.status_no_gps)
    }

    private fun showLocation(location: Location) {
        val mars = MarsCoords.toMars(location.latitude, location.longitude)
        binding.marsX.text = String.format(Locale.US, "%.1f", mars.x)
        binding.marsY.text = String.format(Locale.US, "%.1f", mars.y)
        binding.accuracy.text = getString(R.string.accuracy_fmt, location.accuracy)
        binding.status.text = getString(R.string.status_locked)
    }

    override fun onLocationChanged(location: Location) = showLocation(location)

    @Deprecated("Deprecated in Java")
    override fun onStatusChanged(provider: String?, status: Int, extras: Bundle?) {
    }

    override fun onProviderEnabled(provider: String) {
        startLocationUpdates()
    }

    override fun onProviderDisabled(provider: String) {
        if (provider == LocationManager.GPS_PROVIDER) showUnavailable()
    }
}
