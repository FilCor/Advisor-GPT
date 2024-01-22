document.getElementById('analysisForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var companyName = document.getElementById('company').value;
    document.getElementById('statusMessage').style.display = 'block';
    document.getElementById('statusText').innerText = 'Analyzing...';
    document.getElementById('statusText').style.color = 'orange';

    showModal();

    fetch('http://13.60.22.140:8000/analyze/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ company: companyName }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Analysis Started:', data);
        checkAnalysisStatus(companyName);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

function checkAnalysisStatus(companyName) {
    fetch(`http://13.60.22.140:8000/status/${companyName}`)
    .then(response => response.json())
    .then(data => {
        if (data.status === "Complete") {
            document.getElementById('statusText').innerText = 'Analysis Complete!';
            document.getElementById('statusText').style.color = 'green';
            showResult(companyName);
        } else {
            setTimeout(() => checkAnalysisStatus(companyName), 5000);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function showResult(companyName) {
    fetch(`http://13.60.22.140:8000/result/${companyName}`)
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
