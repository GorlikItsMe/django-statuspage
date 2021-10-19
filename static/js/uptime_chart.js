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
        label: "ping ms",
        backgroundColor: "rgb(0, 255, 0)",
        borderColor: "rgb(0, 255, 0)",
        fill: false,
        data: datax.data,
      },
    ],
  };

  let uptime_chart = new Chart(ctx, {
    type: "line",
    data: data,
    options: {
      spanGaps: 1000 * 60 * 5, // 5min  // 1000 * 60 * 60 * 24 * 2, // 2 days
      responsive: true,
      interaction: {
        mode: "nearest",
      },
      plugins: {
        title: {
          display: true,
          text: "Uptime",
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
            tooltipFormat: 'H:mm',
            displayFormats: {
              minute: 'H:mm',
              hour: 'H:00',
              day: 'MMM D',
            }
          },
          ticks: {
            autoSkip: false,
            maxRotation: 0,
            major: {
              enabled: true,
            },
            // color: function(context) {
            //   return context.tick && context.tick.major ? '#FF0000' : 'rgba(0,0,0,0.1)';
            // },
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
