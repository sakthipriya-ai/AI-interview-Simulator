new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ["Average Score","Remaining"],
        datasets: [{
            data: [avg, 100 - avg]
        }]
    },
    options:{
        responsive:true,
        maintainAspectRatio:false,   // 🔥 allows custom size
        plugins:{
            legend:{
                labels:{ color:"white" }
            }
        }
    }
});