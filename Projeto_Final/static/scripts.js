
      
var options = {
  series: [{
    name: 'Temperatura',
    data: [0] // Dados iniciais
}, {
    name: 'Umidade',
    data: [0] // Dados iniciais
}],
chart: {
    height: 350,
    type: 'line' 
},
colors: ['#FF4560', '#00E396'],

yaxis: [{
  title: {
      text: 'Temperatura (°C)',
  },
}, {
  opposite: true,
  title: {
      text: 'Umidade (%)'
  }
}],

chart: {
  type: 'line'
},
stroke: {
  curve: 'smooth',
  width: 2
},
markers: {
  size: 5
},

xaxis: {
  type: 'datetime',
    labels: {
      formatter: function(val, timestamp) {
        // Formatar a data para exibir dia, mês, hora e minuto
        const date = new Date(timestamp);
        const day = date.getDate();
        const month = date.getMonth() + 1;
        const hour = date.getHours();
        const minute = date.getMinutes();
        return `${day}/${month} ${hour}:${minute}`;
      }
    },
    tickAmount: 4,  
    },

};
  
var chart = new ApexCharts(document.querySelector("#chart"), options);
chart.render();
        
function atualizarDados() {
  fetch('/latest-sensor-data')
    .then(response => response.json())
    .then(data => {
        if (data.temperatura.length && data.umidade.length && data.categorias.length) {
            chart.updateSeries([
                { name: 'Temperatura', data: data.temperatura.map((val, i) => ({ x: data.categorias[i], y: val })) },
                { name: 'Umidade', data: data.umidade.map((val, i) => ({ x: data.categorias[i], y: val })) }
            ]);

            var dadosTabela = data.categorias.map((categoria, i) => ({
                data_hora: categoria,
                temperatura: data.temperatura[i],
                umidade: data.umidade[i]
            }));

            var tabela = $('#dataTable').DataTable();
            tabela.clear();
            tabela.rows.add(dadosTabela);
            tabela.draw();

        } else {
            console.error('Erro ao buscar dados: ', data.erro);
        }
    })
    .catch(error => console.error('Erro ao fazer fetch: ', error));
}

setInterval(atualizarDados, 2000);
atualizarDados();

$(document).ready(function() {
  $('#dataTable').DataTable({
      "columns": [
          { 
            "data": "data_hora",
            "render": function(data, type, row) {
              if (type === 'display' || type === 'filter') {
                const date = new Date(data);
                const day = date.getDate();
                const month = date.getMonth() + 1;
                const year = date.getFullYear();
                const hour = date.getHours();
                const minute = date.getMinutes();
                const second = date.getSeconds();
                return `${day}/${month}/${year} - ${hour}:${minute}:${second}`;
              }
              return data;
            }
          },
          { "data": "temperatura" },
          { "data": "umidade" }
      ]
  });
});