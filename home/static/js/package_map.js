document.addEventListener('DOMContentLoaded', function () {
  const mapElement = document.getElementById('route-map')

  // Stop if this page does not contain the map
  if (!mapElement) {
    return
  }

  // Center map on Nepal
  const map = L.map('route-map').setView([28.3949, 84.124], 7)

  // OpenStreetMap layer
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map)
})
