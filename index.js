document.addEventListener('DOMContentLoaded', () => {
  fetch('https://api.open-meteo.com/v1/forecast?latitude=24.8&longitude=121.0&hourly=temperature_2m')
    .then(response => response.json())
    .then(data => {
      const temperatures = data.hourly.temperature_2m;
      const times = data.hourly.time;

      const result = times.map((time, index) => ({
        time,
        temperature_2m: temperatures[index]
      }));

      const tableBody = document.querySelector('#temperature-table tbody');
      
      tableBody.innerHTML = '';

      result.forEach(item => {
        const row = document.createElement('tr');
        const timeCell = document.createElement('td');
        const temperatureCell = document.createElement('td');

        timeCell.textContent = item.time;
        temperatureCell.textContent = item.temperature_2m;

        row.appendChild(timeCell);
        row.appendChild(temperatureCell);
        tableBody.appendChild(row);
      });
    })
    .catch(error => {
      console.error('Error:', error);
    });
});