fetch('/data')
  .then(res => res.json())
  .then(data => {
    const tbody = document.querySelector("#song-table tbody");
    const x = [];
    const y = [];

    data.forEach(song => {
      // Insertar fila en la tabla
      const row = `<tr>
        <td>${song.song_id}</td>
        <td>${song.title}</td>
        <td>${song.artist}</td>
        <td>${song.genre}</td>
        <td>${song.duration_sec}</td>
        <td>${song.timestamp}</td>
      </tr>`;
      tbody.innerHTML += row;

      // Datos para el gráfico
      x.push(song.title);
      y.push(song.duration_sec);
    });

    // Gráfico con Plotly
    const trace = { x: x, y: y, type: 'bar' };
    Plotly.newPlot('chart', [trace]);
  });
