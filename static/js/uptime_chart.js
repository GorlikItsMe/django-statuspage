const newDateString = (n) => {
  return moment(new Date(), "DD.MM.YYYY H:mm:ss").add(n, "days").toISOString();
};

const random = (a, b) => {
  return Math.floor(Math.random() * b + a);
};

async function render_uptime_chart(ctx, service_slug) {
  const r = await fetch(`/api/uptimechart/${service_slug}/`);
  const datax = await r.json();

  const data = {
    datasets: [
      {
        label: "Ping (ms)",
        backgroundColor: "#3ba55c50",
        borderColor: "#3ba55c",
        fill: true,
        data: datax.data,
        lineTension: 0.1,
        pointRadius: 0,
        pointHoverRadius: 0,
        pointBorderWidth: 0,
        segment: {
          borderColor: (ctx) => {
            if (ctx.p1.parsed.y == 0) {
              return "rgb(255,0,0)";
            }
            return undefined;
          },
          //ctx => skipped(ctx, 'rgb(0,0,0,0.2)') || down(ctx, 'rgb(192,75,75)'),
        },
      },
    ],
  };

  var delayed;
  
  let uptime_chart = new Chart(ctx, {
    type: "line",
    data: data,
    options: {
      spanGaps: 1000 * 60 * 60, // 60min
      responsive: true,
      interaction: {
        intersect: false,
        mode: "index",
      },
      animation: {
        onComplete: () => {
          delayed = true;
        },
        delay: (context) => {
          let delay = 0;
          if (context.type === 'data' && context.mode === 'default' && !delayed) {
            delay = context.dataIndex * 4;
          }
          return delay;
        },
      },
      plugins: {
        tooltip: {
          position: "average",
        },
        legend: {
          display: false,
        },
      },
      scales: {
        x: {
          type: "time",
          display: true,
          // title: {
          //   display: true,
          //   text: "Date",
          // },
          time: {
            tooltipFormat: "H:mm",
            displayFormats: {
              minute: "H:mm",
              hour: "H:00",
              day: "MMM d",
            },
          },
          ticks: {
            autoSkip: false,
            maxRotation: 0,
            major: {
              enabled: true,
            },
            color: function(context) {
              return context.tick && context.tick.major ? '#000' : '#727272';
            },
            font: function (context) {
              if (context.tick && context.tick.major) {
                return {
                  weight: "bold",
                };
              }
            },
          },
        },
        y: {
          display: true,
          title: {
            display: true,
            text: "ping ms",
          },
        },
      },
    },
  });
  return {
    chart: uptime_chart,
    refreshWithApi: () => {
      fetch(`/api/uptimechart/${service_slug}/`)
        .then((r) => r.json())
        .then((apidata) => {
          uptime_chart.data.datasets[0].data = apidata.data;
          uptime_chart.update();
        });
    },
  };
}
