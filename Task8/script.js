const socket = new WebSocket("ws://127.0.0.1:8000/ws")

const tempChart = new Chart(
    document.getElementById("tempChart"), {
    type: "line",
    data: {
        labels: [],
        datasets: [
            {
                label: "Temperature",
                data: [],
                borderWidth: 2
            }
        ]
    }
})

const vibChart = new Chart(
    document.getElementById("vibChart"), {
    type: "line",
    data: {
        labels: [],
        datasets: [
            {
                label: "Vibration",
                data: [],
                borderWidth: 2
            }
        ]
    }
})

socket.onmessage = function (event) {
    const data = JSON.parse(event.data)
    const time = data.timestamp

    tempChart.data.labels.push(time)
    tempChart.data.datasets[0].data.push(
        data.temperature.value

    )

    vibChart.data.labels.push(time)
    vibChart.data.datasets[0].data.push(
        data.vibration.value
    )
    tempChart.update()
    vibChart.update()

    document.getElementById("tempAvg").innerText =data.temperature.moving_avg;
    document.getElementById("vibAvg").innerText =data.vibration.moving_avg;

    if (data.temperature.alert)
        addAlert("Temperature anomaly detected at " + time)

    if (data.vibration.alert)
        addAlert("Vibration anomaly detected at " + time)
}

function addAlert(message) {
    const li = document.createElement("li")
    li.innerText = message
    document.getElementById("alertList").prepend(li)
}