// Creating chart for humidity
const humidityChart = document.getElementById('humidity-chart');
new Chart(humidityChart, {
  type: 'line',
  data: {
    labels: datetimeLabels,
    datasets: [
      {
        label: 'Kelembaban Udara (%)',
        data: humidityValue,
        borderWidth: 1,
        borderColor: 'rgba(50, 50, 0, 0.5)',
      }
    ]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});

// Creating chart for temperature
const temperatureChart = document.getElementById('temperature-chart');
new Chart(temperatureChart, {
  type: 'line',
  data: {
    labels: datetimeLabels,
    datasets: [
      {
        label: 'Suhu Udara (C)',
        data: temperatureValue,
        borderWidth: 1,
        borderColor: 'rgba(50, 50, 0, 0.5)',
      }
    ]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});

// Creating chart for wind speed
const windspeedChart = document.getElementById('windspeed-chart');
new Chart(windspeedChart, {
  type: 'line',
  data: {
    labels: datetimeLabels,
    datasets: [
      {
        label: 'Kecepatan Angin (km per jam)',
        data: windspeedValue,
        borderWidth: 1,
        borderColor: 'rgba(50, 50, 0, 0.5)',
      }
    ]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});