document
  .getElementById("weather-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault()

    const city = document.getElementById("city").value
    const weatherImage = document.getElementById("weather-image")
    const weatherLocation = document.getElementById("weather-location")
    const weatherTemperature = document.getElementById("weather-temperature")
    const weatherDescription = document.getElementById("weather-description")

    try {
      const response = await fetch(`/weather?city=${city}`)
      if (!response.ok) throw new Error("City not found")

      const data = await response.json()

      // Log the response to debug
      console.log(data)

      if (
        data.weather &&
        Array.isArray(data.weather) &&
        data.weather.length > 0
      ) {
        const weatherCondition = data.weather[0].main.toLowerCase()
        const weatherIconCode = data.weather[0].icon

        weatherLocation.textContent = `${data.name}, ${data.sys.country}`
        weatherTemperature.textContent = `Temperature: ${data.main.temp}°C`
        weatherDescription.textContent = `Condition: ${data.weather[0].description}`
        weatherImage.src = `https://openweathermap.org/img/wn/${weatherIconCode}@2x.png`
      } else {
        throw new Error("No weather data found in the response.")
      }
    } catch (error) {
      console.error("Error fetching weather data:", error)
      weatherLocation.textContent = "Error"
      weatherTemperature.textContent = ""
      weatherDescription.textContent = error.message
      weatherImage.src = ""
    }
  })

// Add event listener for "View Cities" button
document
  .getElementById("view-cities-btn")
  .addEventListener("click", async function (e) {
    e.preventDefault()

    const citiesList = document.getElementById("cities-list")
    citiesList.innerHTML = "" // Clear existing list

    try {
      const response = await fetch("/cities")
      if (!response.ok) throw new Error("Failed to fetch cities")

      const cities = await response.json()
      cities.forEach((city) => {
        const cityItem = document.createElement("li")
        cityItem.textContent = `${city.city}, ${city.country} - ${city.temperature}°C - ${city.description}`

        // Add delete button to each city
        const deleteBtn = document.createElement("button")
        deleteBtn.textContent = "Delete"
        deleteBtn.classList.add("delete-btn")
        deleteBtn.addEventListener("click", async () => {
          try {
            const response = await fetch("/delete_city", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ city: city.city }),
            })
            const data = await response.json()
            console.log(data.message)
            cityItem.remove() // Remove the city from the list in the UI
          } catch (error) {
            console.error("Error deleting city:", error)
          }
        })

        cityItem.appendChild(deleteBtn)
        citiesList.appendChild(cityItem)
      })
    } catch (error) {
      console.error("Error fetching cities:", error)
    }
  })