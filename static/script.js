document.getElementById('analysisForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var companyName = document.getElementById('company').value;
    document.getElementById('statusMessage').style.display = 'block';
    document.getElementById('statusText').innerText = 'Analyzing...';
    document.getElementById('statusText').style.color = 'orange';

    showModal();

    fetch('http://13.50.159.97:8000/analyze/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ company: companyName }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Analysis Started:', data);
        var taskId = data.task_id; // Salva il task_id ricevuto
        checkAnalysisStatus(taskId); // Passa il task_id a checkAnalysisStatus
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

function checkAnalysisStatus(taskId) {
    fetch(`http://13.50.159.97:8000/status/${taskId}`)
    .then(response => response.json())
    .then(data => {
        if (data.status === "Complete") {
            document.getElementById('statusText').innerText = 'Analysis Complete!';
            document.getElementById('statusText').style.color = 'green';
            showResult(taskId); // Usa il task_id per richiedere i risultati
        } else {
            setTimeout(() => checkAnalysisStatus(taskId), 5000); // Continua a controllare lo stato
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function showResult(taskId) {
    fetch(`http://13.50.159.97:8000/result/${taskId}`)
    .then(response => response.json())
    .then(data => {
        console.log('Received result data:', data);  // Aggiungi questo per il debug
        if (data.result) {
            document.getElementById('result').innerText = data.result;
            document.getElementById('result').style.display = 'block';
        } else {
            alert("Analysis not complete or file not found.");
        }
    })
    .catch((error) => {
        console.error('Error fetching the results:', error);
        alert('Error fetching the results');
    });
}

// Modal functionality
var modal = document.getElementById('disclaimerModal');
var span = document.getElementsByClassName("close")[0];

function showModal() {
    modal.style.display = "block";
}

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
