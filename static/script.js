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
        checkAnalysisStatus(companyName, data.task_id); // Passa il task_id a checkAnalysisStatus
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

function checkAnalysisStatus(companyName, taskId) {
    fetch(`http://13.50.159.97:8000/status/${companyName}/${taskId}`) // Usa taskId nell'URL
    .then(response => response.json())
    .then(data => {
        if (data.status === "Complete") {
            document.getElementById('statusText').innerText = 'Analysis Complete!';
            document.getElementById('statusText').style.color = 'green';
            showResult(companyName, taskId); // Passa il task_id a showResult
        } else {
            setTimeout(() => checkAnalysisStatus(companyName, taskId), 5000); // Passa il task_id a checkAnalysisStatus
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function showResult(companyName, taskId) {
    fetch(`http://13.50.159.97:8000/result/${companyName}/${taskId}`) // Usa taskId nell'URL
    .then(response => response.json())
    .then(data => {
        if (data.result) {
            document.getElementById('result').innerText = data.result;
            document.getElementById('result').style.display = 'block';
        } else {
            alert("Analysis not complete or file not found.");
        }
    })
    .catch((error) => {
        console.error('Error:', error);
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
