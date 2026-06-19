let currentHR = "--";
let currentRR = "--";
let currentSDNN = "--";
let currentRMSSD = "--";
let currentQuality = "--";
let currentStress = "--";
let currentFatigue = "--";
let currentOverall = "--";

let recentReadings = [];
const connectBtn = document.getElementById("connectBtn");

let timerStarted = false;
let countdown;
let seconds = 180;

const ctx = document.getElementById('ecgChart');

const glowPlugin = {

    id: 'glowEffect',

    beforeDatasetDraw(chart) {

        const ctx = chart.ctx;

        ctx.save();

        ctx.shadowColor = '#4dd0ff';
        ctx.shadowBlur = 15;
    },

    afterDatasetDraw(chart) {

        chart.ctx.restore();
    }
};

const ecgChart = new Chart(ctx, {

    type: 'line',

    data: {
        labels: [],
        datasets: [{
            data: [],
            borderColor: '#00e5ff',
            borderWidth: 2,
            pointRadius: 0,
            tension: 0
        }]
    },

    plugins:[glowPlugin],

    options: {

        responsive:true,
        maintainAspectRatio:false,
        animation:false,

        plugins:{
            legend:{
                display:false
            }
        },

        scales:{

            x:{
                display:false,
                grid:{
                    color:'rgba(255,255,255,0.05)'
                }
            },

            y:{
                display:false,
                grid:{
                    color:'rgba(255,255,255,0.05)'
                }
            }

        }

    }

});

function startTimer(){

    countdown = setInterval(()=>{

        let min = Math.floor(seconds/60);
        let sec = seconds%60;

        document.getElementById("timer").innerText =
            `${String(min).padStart(2,'0')}:${String(sec).padStart(2,'0')}`;

        seconds--;

        if(seconds < 0){

            clearInterval(countdown);

            finishRecording();
        }

    },1000);
}

function addECG(value){

    ecgChart.data.labels.push('');

    ecgChart.data.datasets[0].data.push(value);

    if(ecgChart.data.datasets[0].data.length > 300){

        ecgChart.data.labels.shift();
        ecgChart.data.datasets[0].data.shift();
    }

    ecgChart.update('none');
}

let ecgInterval;

function startECG(){

    // Waiting for ECG values from ESP32
}

function finishRecording(){

    clearInterval(ecgInterval);

    addReading(
        currentHR,
        currentSDNN,
        currentRMSSD,
        currentStress
    );

    resetDashboard();
}

function resetDashboard(){

    seconds = 180;

    document.getElementById("timer").innerText = "03:00";

    timerStarted = false;

    ecgChart.data.labels = [];
    ecgChart.data.datasets[0].data = [];

    ecgChart.update();

    document.getElementById("deviceStatus").innerHTML =
        "🔴 Waiting For Electrode";
}

function addReading(hr, sdnn, rmssd, stress){

    const reading = {

        time: new Date().toLocaleTimeString(),

        hr: hr,
        sdnn: sdnn,
        rmssd: rmssd,
        stress: stress
    };

    recentReadings.unshift(reading);

    if(recentReadings.length > 3){
        recentReadings.pop();
    }

    updateTable();
}

function updateTable(){

    const tbody = document.getElementById("tableBody");

    tbody.innerHTML = "";

    recentReadings.forEach(reading => {

        tbody.innerHTML += `
            <tr>
                <td>${reading.time}</td>
                <td>${reading.hr}</td>
                <td>${reading.sdnn}</td>
                <td>${reading.rmssd}</td>
                <td>${reading.stress}</td>
            </tr>
        `;
    });
}

connectBtn.addEventListener("click",()=>{

    if(timerStarted) return;

    timerStarted = true;

    document.getElementById("deviceStatus").innerHTML =
        "🟢 Connected";

    startTimer();

    startECG();
});