const apiKey = 'c9c3f289f9a98421ddf3e808330ceb3c'; // Replace with your OpenWeatherMap API key
let swiper; // Declare swiper variable globally

function searchWeather() {
    const location = document.getElementById('locationInput').value;
    fetchWeather(location);
}

async function fetchWeather(location) {
    const response = await fetch(`https://api.openweathermap.org/data/2.5/forecast?q=${location}&appid=${apiKey}&units=metric`);
    const data = await response.json();
    const weatherContainer = document.getElementById('weatherContainer');
    const weatherSlider = document.getElementById('weatherSlider'); // Get weatherSlider element
    
    // Clear previous weather data
    weatherContainer.innerHTML = '';
    weatherSlider.innerHTML = ''; // Clear weatherSlider content

    if (data.cod === '404') {
        weatherContainer.innerHTML = '<p>Location not found</p>';
        return;
    }

    // Group forecast data by date
    const forecastMap = new Map();
    data.list.forEach(forecast => {
        const date = new Date(forecast.dt * 1000).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' });
        if (!forecastMap.has(date)) {
            forecastMap.set(date, []);
        }
        forecastMap.get(date).push(forecast);
    });

    // Display forecast data
    forecastMap.forEach((forecasts, date) => {
        const weatherCard = document.createElement('div');
        weatherCard.classList.add('weather-card');

        // Date
        const forecastDate = document.createElement('div');
        forecastDate.textContent = date;

        // Weather Info
        const weatherInfo = document.createElement('ul');

        forecasts.forEach(forecast => {
            const listItem = document.createElement('li');

            // Weather Icon
            const weatherIcon = document.createElement('img');
            weatherIcon.classList.add('weather-icon');
            weatherIcon.src = `http://openweathermap.org/img/wn/${forecast.weather[0].icon}.png`;

            // Weather Description
            const weatherDescription = document.createElement('span');
            weatherDescription.textContent = forecast.weather[0].description;

            // Temperature
            const weatherTemperature = document.createElement('span');
            weatherTemperature.textContent = `Temperature: ${forecast.main.temp}°C`;

            // Precipitation
            const precipitation = document.createElement('span');
            precipitation.textContent = `Precipitation: ${forecast.pop}%`;

            // Wind Speed
            const windSpeed = document.createElement('span');
            windSpeed.textContent = `Wind Speed: ${forecast.wind.speed} m/s`;

            // Humidity
            const humidity = document.createElement('span');
            humidity.textContent = `Humidity: ${forecast.main.humidity}%`;

            // Soil Moisture (for demonstration)
            const soilMoisture = document.createElement('span');
            soilMoisture.textContent = `Soil Moisture: ${Math.floor(Math.random() * 100)}%`;

            // UV Index (for demonstration)
            const uvIndex = document.createElement('span');
            uvIndex.textContent = `UV Index: ${Math.floor(Math.random() * 10)}`;

            // Sunrise Time (for demonstration)
            const sunriseTime = document.createElement('span');
            sunriseTime.textContent = `Sunrise: ${new Date(forecast.sys.sunrise * 1000).toLocaleTimeString('en-US')}`;

            // Sunset Time (for demonstration)
            const sunsetTime = document.createElement('span');
            sunsetTime.textContent = `Sunset: ${new Date(forecast.sys.sunset * 1000).toLocaleTimeString('en-US')}`;

            listItem.appendChild(weatherIcon);
            listItem.appendChild(weatherDescription);
            listItem.appendChild(weatherTemperature);
            listItem.appendChild(precipitation);
            listItem.appendChild(windSpeed);
            listItem.appendChild(humidity);
            listItem.appendChild(soilMoisture);
            listItem.appendChild(uvIndex);
            listItem.appendChild(sunriseTime);
            listItem.appendChild(sunsetTime);

            weatherInfo.appendChild(listItem);
        });

        // Add click event listener to weather card
        weatherCard.addEventListener('click', () => {
            // Toggle class to expand or collapse weather details
            weatherCard.classList.toggle('expanded');
        });

        weatherCard.appendChild(forecastDate);
        weatherCard.appendChild(weatherInfo);

        weatherSlider.appendChild(weatherCard); // Append weather card to weatherSlider
    });

    // Initialize Swiper
    swiper = new Swiper('.swiper-container', {
        loop: true,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });
}

// Add event listeners for tap or arrow key press to navigate slides
document.addEventListener('keydown', function(event) {
    if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
        swiper.slideNext();
    }
});

// Initial weather fetch example
fetchWeather('Bhopal');
