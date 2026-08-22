document.addEventListener('DOMContentLoaded', function () {

  console.log('PACKAGE MAP JS LOADED')

  /* =====================================
     CHECK LIBRARIES
  ===================================== */

  console.log('Leaflet loaded:', typeof L !== 'undefined')
  console.log(
    'Polyline library loaded:',
    typeof polyline !== 'undefined'
  )


  /* =====================================
     DETECT MAP TYPE
  ===================================== */

  const editMapElement =
    document.getElementById('route-map')

  const detailMapElement =
    document.getElementById('package-route-map')

  console.log(
    'Add/Edit map container:',
    editMapElement
  )

  console.log(
    'Package Detail map container:',
    detailMapElement
  )


  /* =====================================
     PACKAGE DETAIL MAP
  ===================================== */

  if (detailMapElement) {

    console.log(
      'PACKAGE DETAIL MAP DETECTED'
    )

    if (typeof L === 'undefined') {

      console.error(
        'Leaflet is not loaded.'
      )

      return
    }


    /* =====================================
       INITIALIZE DETAIL MAP
    ===================================== */

    const detailMap =
      L.map('package-route-map').setView(
        [28.3949, 84.124],
        7
      )


    L.tileLayer(
      'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      {
        maxZoom: 19,
        attribution:
          '&copy; OpenStreetMap contributors',
      }
    ).addTo(detailMap)


    console.log(
      'Package detail map initialized.'
    )


    /* =====================================
       GET SAVED ROUTE DATA
    ===================================== */

    const existingRouteElement =
      document.getElementById(
        'existing-route-points'
      )

    const detailPointsList =
      document.getElementById(
        'package-route-points'
      )


    let savedRouteData = []

    if (existingRouteElement) {

      try {

        savedRouteData =
          JSON.parse(
            existingRouteElement.textContent
          )

        console.log(
          'Saved route data:',
          savedRouteData
        )

      } catch (error) {

        console.error(
          'Unable to parse saved route data:',
          error
        )

      }

    } else {

      console.warn(
        'existing-route-points element not found.'
      )

    }


    /* =====================================
       SUPPORT BOTH DATA FORMATS
    ===================================== */

    let detailPoints = []
    let detailGeometry = null


    /*
     * Old format:
     *
     * [
     *   {
     *     name: "...",
     *     latitude: ...,
     *     longitude: ...
     *   }
     * ]
     */

    if (Array.isArray(savedRouteData)) {

      detailPoints =
        savedRouteData

    }


    /*
     * New format:
     *
     * {
     *   points: [...],
     *   geometry: "encoded-polyline"
     * }
     */

    else if (
      savedRouteData &&
      Array.isArray(
        savedRouteData.points
      )
    ) {

      detailPoints =
        savedRouteData.points

      detailGeometry =
        savedRouteData.geometry || null

    }


    console.log(
      'Detail route points:',
      detailPoints
    )

    console.log(
      'Detail route geometry:',
      detailGeometry
    )


    /* =====================================
       DISPLAY ROUTE POINTS
    ===================================== */

    const detailMarkers = []


    detailPoints.forEach(
      function (point, index) {

        const latitude =
          Number(point.latitude)

        const longitude =
          Number(point.longitude)


        if (
          Number.isNaN(latitude) ||
          Number.isNaN(longitude)
        ) {

          console.error(
            'Invalid route point:',
            point
          )

          return
        }


        const marker =
          L.marker([
            latitude,
            longitude,
          ]).addTo(detailMap)


        marker.bindPopup(`
          <strong>
            ${index + 1}. ${point.name || 'Location'}
          </strong>

          <br>

          ${point.displayName || ''}
        `)


        detailMarkers.push(marker)


        /* =====================================
           DISPLAY POINT IN LIST
        ===================================== */

        if (detailPointsList) {

          const item =
            document.createElement('div')


          item.className =
            'route-detail-point-item'


          item.innerHTML = `
            <span class="route-detail-number">
              ${index + 1}
            </span>

            <span class="route-detail-name">
              ${point.name || 'Location'}
            </span>
          `


          detailPointsList.appendChild(item)

        }

      }
    )


    /* =====================================
       DRAW SAVED ROUTE GEOMETRY
    ===================================== */

    if (
      detailGeometry &&
      typeof polyline !== 'undefined'
    ) {

      try {

        const routeCoordinates =
          polyline.decode(
            detailGeometry
          )


        if (routeCoordinates.length) {

          const routeLine =
            L.polyline(
              routeCoordinates,
              {
                color: '#0b3d91',
                weight: 5,
                opacity: 0.9,
              }
            ).addTo(detailMap)


          detailMap.fitBounds(
            routeLine.getBounds(),
            {
              padding: [50, 50],
            }
          )


          console.log(
            'Saved route geometry displayed.'
          )

        }

      } catch (error) {

        console.error(
          'Unable to decode saved route:',
          error
        )

      }

    }


    /* =====================================
       FALLBACK ROUTE
    ===================================== */

    else if (
      detailPoints.length > 1
    ) {

      const fallbackCoordinates =
        detailPoints.map(
          function (point) {

            return [
              Number(point.latitude),
              Number(point.longitude),
            ]

          }
        )


      const routeLine =
        L.polyline(
          fallbackCoordinates,
          {
            color: '#0b3d91',
            weight: 4,
            opacity: 0.8,
            dashArray: '8, 8',
          }
        ).addTo(detailMap)


      detailMap.fitBounds(
        routeLine.getBounds(),
        {
          padding: [50, 50],
        }
      )


      console.log(
        'Fallback route displayed.'
      )

    }


    /* =====================================
       SINGLE POINT
    ===================================== */

    else if (
      detailPoints.length === 1
    ) {

      detailMap.setView(
        [
          Number(
            detailPoints[0].latitude
          ),

          Number(
            detailPoints[0].longitude
          ),
        ],
        12
      )

    }


    /* =====================================
       FIX LEAFLET SIZE
    ===================================== */

    setTimeout(
      function () {

        detailMap.invalidateSize()

      },
      200
    )


    console.log(
      'PACKAGE DETAIL MAP COMPLETE'
    )


    /*
     * Stop here.
     *
     * Package detail does not need
     * the Add/Edit search system.
     */

    return
  }


  /* =====================================
     ADD / EDIT MAP
  ===================================== */

  if (!editMapElement) {

    console.warn(
      'No Add/Edit route map found.'
    )

    return
  }


  if (typeof L === 'undefined') {

    console.error(
      'Leaflet is not loaded.'
    )

    return
  }


  console.log(
    'ADD/EDIT PACKAGE MAP DETECTED'
  )


  /* =====================================
     MAP INITIALIZATION
  ===================================== */

  const map =
    L.map('route-map').setView(
      [28.3949, 84.124],
      7
    )


  L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
      maxZoom: 19,
      attribution:
        '&copy; OpenStreetMap contributors',
    }
  ).addTo(map)


  console.log(
    'Add/Edit map initialized.'
  )


  /* =====================================
     ELEMENTS
  ===================================== */

  const searchInput =
    document.getElementById(
      'location-search'
    )


  const searchButton =
    document.getElementById(
      'search-location-btn'
    )


  const resultsContainer =
    document.getElementById(
      'location-results'
    )


  const routePointsList =
    document.getElementById(
      'route-points-list'
    )


  const routePointsInput =
    document.getElementById(
      'route-points-data'
    )


  console.log(
    'Search input:',
    searchInput
  )

  console.log(
    'Search button:',
    searchButton
  )

  console.log(
    'Route points input:',
    routePointsInput
  )


  /* =====================================
     ROUTE DATA
  ===================================== */

  let routePoints = []
  let routeGeometry = null


  /*
   * Edit page provides:
   *
   * existingRoutePoints
   */

  if (
    typeof existingRoutePoints !==
    'undefined'
  ) {

    console.log(
      'Existing route points received:',
      existingRoutePoints
    )


    /*
     * New format
     */

    if (
      existingRoutePoints &&
      !Array.isArray(
        existingRoutePoints
      ) &&
      Array.isArray(
        existingRoutePoints.points
      )
    ) {

      routePoints =
        existingRoutePoints.points

      routeGeometry =
        existingRoutePoints.geometry ||
        null

    }


    /*
     * Old format
     */

    else if (
      Array.isArray(
        existingRoutePoints
      )
    ) {

      routePoints =
        existingRoutePoints

    }

  }


  console.log(
    'Loaded route points:',
    routePoints
  )

  console.log(
    'Loaded route geometry:',
    routeGeometry
  )


  let markers = []
  let routeLine = null


  /* =====================================
     UPDATE HIDDEN INPUT
  ===================================== */

  function updateRoutePointsInput() {

    if (!routePointsInput) {
      return
    }


    const routeData = {

      points:
        routePoints,

      geometry:
        routeGeometry,

    }


    routePointsInput.value =
      JSON.stringify(
        routeData
      )


    console.log(
      'Hidden route input updated:',
      routeData
    )

  }


  /* =====================================
     CSRF TOKEN
  ===================================== */

  function getCookie(name) {

    let cookieValue = null


    if (
      document.cookie &&
      document.cookie !== ''
    ) {

      const cookies =
        document.cookie.split(';')


      for (
        let i = 0;
        i < cookies.length;
        i++
      ) {

        const cookie =
          cookies[i].trim()


        if (
          cookie.substring(
            0,
            name.length + 1
          ) ===
          name + '='
        ) {

          cookieValue =
            decodeURIComponent(
              cookie.substring(
                name.length + 1
              )
            )


          break

        }

      }

    }


    return cookieValue

  }


  /* =====================================
     SEARCH LOCATION
  ===================================== */

  async function searchLocation() {

    if (!searchInput) {

      console.error(
        'Search input not found.'
      )

      return

    }


    const query =
      searchInput.value.trim()


    if (!query) {

      if (resultsContainer) {

        resultsContainer.innerHTML =
          '<p>Please enter a location to search.</p>'

      }

      return

    }


    if (resultsContainer) {

      resultsContainer.innerHTML =
        '<p>Searching location...</p>'

    }


    try {

      const searchQuery =
        `${query}, Nepal`


      const url =
        'https://nominatim.openstreetmap.org/search?' +
        new URLSearchParams({

          q:
            searchQuery,

          format:
            'jsonv2',

          addressdetails:
            '1',

          limit:
            '5',

          countrycodes:
            'np',

        })


      const response =
        await fetch(
          url,
          {
            headers: {
              Accept:
                'application/json',
            },
          }
        )


      if (!response.ok) {

        throw new Error(
          'Unable to search location.'
        )

      }


      const locations =
        await response.json()


      console.log(
        'Search results:',
        locations
      )


      displaySearchResults(
        locations
      )

    } catch (error) {

      console.error(
        'SEARCH ERROR:',
        error
      )


      if (resultsContainer) {

        resultsContainer.innerHTML = `
          <p class="search-error">
            Unable to search for this location.
          </p>
        `

      }

    }

  }


  /* =====================================
     DISPLAY SEARCH RESULTS
  ===================================== */

  function displaySearchResults(
    locations
  ) {

    if (!resultsContainer) {
      return
    }


    resultsContainer.innerHTML = ''


    if (!locations.length) {

      resultsContainer.innerHTML = `
        <p class="no-results">
          No locations found. Try another search.
        </p>
      `

      return

    }


    locations.forEach(
      function (location) {

        const result =
          document.createElement('div')


        result.className =
          'location-result'


        const locationName =
          location.name ||
          location.display_name
            .split(',')[0]


        result.innerHTML = `

          <div class="location-result-info">

            <strong>
              ${locationName}
            </strong>

            <span>
              ${location.display_name}
            </span>

          </div>


          <button
            type="button"
            class="add-route-point-btn"
          >

            <i class="fa-solid fa-plus"></i>

            Add to Route

          </button>

        `


        const addButton =
          result.querySelector(
            '.add-route-point-btn'
          )


        addButton.addEventListener(
          'click',
          function () {

            addRoutePoint({

              name:
                locationName,

              displayName:
                location.display_name,

              latitude:
                parseFloat(
                  location.lat
                ),

              longitude:
                parseFloat(
                  location.lon
                ),

            })

          }
        )


        resultsContainer.appendChild(
          result
        )

      }
    )

  }


  /* =====================================
     ADD ROUTE POINT
  ===================================== */

  function addRoutePoint(point) {

    console.log(
      'Adding route point:',
      point
    )


    routePoints.push(point)


    /*
     * Existing route is no longer
     * valid after adding a point.
     */

    routeGeometry = null


    if (searchInput) {
      searchInput.value = ''
    }


    if (resultsContainer) {
      resultsContainer.innerHTML = ''
    }


    updateRoute()

  }


  /* =====================================
     UPDATE EVERYTHING
  ===================================== */

  async function updateRoute() {

    updateMarkers()

    updateRoutePointList()

    await updateRouteLine()

    updateRoutePointsInput()

  }


  /* =====================================
     UPDATE MARKERS
  ===================================== */

  function updateMarkers() {

    markers.forEach(
      function (marker) {

        map.removeLayer(
          marker
        )

      }
    )


    markers = []


    routePoints.forEach(
      function (point, index) {

        const latitude =
          Number(point.latitude)

        const longitude =
          Number(point.longitude)


        if (
          Number.isNaN(latitude) ||
          Number.isNaN(longitude)
        ) {

          console.error(
            'Invalid route point:',
            point
          )

          return

        }


        const marker =
          L.marker([
            latitude,
            longitude,
          ]).addTo(map)


        marker.bindPopup(`

          <strong>
            ${index + 1}. ${point.name}
          </strong>

          <br>

          ${point.displayName || ''}

        `)


        markers.push(
          marker
        )

      }
    )


    if (
      routePoints.length === 1
    ) {

      map.setView(
        [
          Number(
            routePoints[0].latitude
          ),

          Number(
            routePoints[0].longitude
          ),
        ],
        12
      )

    }

  }


  /* =====================================
     DRAW SAVED ROUTE
  ===================================== */

  function drawRouteGeometry() {

    if (!routeGeometry) {
      return false
    }


    if (
      typeof polyline === 'undefined'
    ) {

      console.error(
        'Polyline library is not loaded.'
      )

      return false

    }


    try {

      const routeCoordinates =
        polyline.decode(
          routeGeometry
        )


      if (
        !routeCoordinates.length
      ) {

        return false

      }


      routeLine =
        L.polyline(
          routeCoordinates,
          {
            color:
              '#0b3d91',

            weight:
              5,

            opacity:
              0.9,

          }
        ).addTo(map)


      map.fitBounds(
        routeLine.getBounds(),
        {
          padding:
            [50, 50],
        }
      )


      return true

    } catch (error) {

      console.error(
        'Unable to draw saved route:',
        error
      )


      return false

    }

  }


  /* =====================================
     GENERATE ACTUAL ROUTE
  ===================================== */

  async function updateRouteLine() {

    if (routeLine) {

      map.removeLayer(
        routeLine
      )

      routeLine = null

    }


    if (
      routePoints.length < 2
    ) {

      return

    }


    /*
     * Use saved route geometry
     * when available.
     */

    if (routeGeometry) {

      const routeDrawn =
        drawRouteGeometry()


      if (routeDrawn) {

        return

      }

    }


    /*
     * ORS requires:
     *
     * [longitude, latitude]
     */

    const coordinates =
      routePoints.map(
        function (point) {

          return [

            Number(
              point.longitude
            ),

            Number(
              point.latitude
            ),

          ]

        }
      )


    /*
     * Make sure URL exists.
     */

    if (
      typeof CALCULATE_ROUTE_URL ===
      'undefined'
    ) {

      console.error(
        'CALCULATE_ROUTE_URL is not defined.'
      )

      return

    }


    try {

      console.log(
        'Sending route request:',
        coordinates
      )


      const response =
        await fetch(
          CALCULATE_ROUTE_URL,
          {

            method:
              'POST',

            headers: {

              'Content-Type':
                'application/json',

              'X-CSRFToken':
                getCookie(
                  'csrftoken'
                ),

            },

            body:
              JSON.stringify({
                coordinates:
                  coordinates,
              }),

          }
        )


      const data =
        await response.json()


      console.log(
        'Route response:',
        data
      )


      if (!response.ok) {

        throw new Error(
          data.details ||
          data.error ||
          'Unable to generate route.'
        )

      }


      if (
        !data.routes ||
        !data.routes.length
      ) {

        throw new Error(
          'No route found.'
        )

      }


      routeGeometry =
        data.routes[0].geometry


      console.log(
        'Route geometry saved:',
        routeGeometry
      )


      drawRouteGeometry()


    } catch (error) {

      console.error(
        'ROUTE ERROR:',
        error
      )


      /*
       * Fallback straight line.
       */

      const fallbackCoordinates =
        routePoints.map(
          function (point) {

            return [

              Number(
                point.latitude
              ),

              Number(
                point.longitude
              ),

            ]

          }
        )


      routeLine =
        L.polyline(
          fallbackCoordinates,
          {

            color:
              '#888',

            weight:
              3,

            opacity:
              0.7,

            dashArray:
              '8, 10',

          }
        ).addTo(map)


      map.fitBounds(
        routeLine.getBounds(),
        {
          padding:
            [50, 50],
        }
      )

    }

  }


  /* =====================================
     UPDATE ROUTE POINT LIST
  ===================================== */

  function updateRoutePointList() {

    if (!routePointsList) {
      return
    }


    routePointsList.innerHTML = ''


    if (
      !routePoints.length
    ) {

      routePointsList.innerHTML = `
        <div class="no-route-points">
          No route points added yet.
        </div>
      `

      return

    }


    routePoints.forEach(
      function (point, index) {

        const item =
          document.createElement('div')


        item.className =
          'route-point-item'


        item.innerHTML = `

          <div class="route-point-number">
            ${index + 1}
          </div>


          <div class="route-point-name">
            ${point.name}
          </div>


          <button
            type="button"
            class="remove-route-point"
            title="Remove location"
          >

            <i class="fa-solid fa-trash"></i>

          </button>

        `


        const removeButton =
          item.querySelector(
            '.remove-route-point'
          )


        removeButton.addEventListener(
          'click',
          function () {

            console.log(
              'Removing route point:',
              point
            )


            routePoints.splice(
              index,
              1
            )


            /*
             * Existing geometry is no
             * longer valid.
             */

            routeGeometry = null


            updateRoute()

          }
        )


        routePointsList.appendChild(
          item
        )

      }
    )

  }


  /* =====================================
     SEARCH EVENTS
  ===================================== */

  if (searchButton) {

    searchButton.addEventListener(
      'click',
      searchLocation
    )

  }


  if (searchInput) {

    searchInput.addEventListener(
      'keydown',
      function (event) {

        if (
          event.key === 'Enter'
        ) {

          event.preventDefault()

          searchLocation()

        }

      }
    )

  }


  /* =====================================
     INITIALIZE EXISTING ROUTE
  ===================================== */

  if (
    routePoints.length > 0
  ) {

    console.log(
      'Initializing saved Add/Edit route...'
    )


    updateRoute()

  } else {

    updateRoutePointsInput()

  }


  /*
   * Fix Leaflet dimensions.
   */

  setTimeout(
    function () {

      map.invalidateSize()

    },
    200
  )


  console.log(
    'ADD/EDIT PACKAGE MAP COMPLETE'
  )

})
