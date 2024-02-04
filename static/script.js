document.getElementById('analysisForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var companyName = document.getElementById('company').value;
    var analyzeButton = this.querySelector('button[type="submit"]');
    var loader = document.getElementById('loader');
    var gifContainer = document.getElementById('gifContainer');
    var gifMessage = document.getElementById('gifMessage');

    // Disabilita il bottone "Analyze" e mostra lo spinner e la GIF
    analyzeButton.disabled = true;
    loader.style.display = 'block';
    gifContainer.style.display = 'block';
    gifMessage.textContent = "L'analisi può richiedere alcuni minuti, nel frattempo goditi questa gif.";

    fetch('http://13.50.159.97:8000/analyze/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ company: companyName }),
    })
    .then(response => response.json())
    .then(data => {
        var taskId = data.task_id;
        checkAnalysisStatus(taskId);
    })
    .catch((error) => {
        console.error('Error:', error);
        analyzeButton.disabled = false;
        loader.style.display = 'none';
        gifContainer.style.display = 'none';
    });
});


function checkAnalysisStatus(taskId) {
    fetch(`http://13.50.159.97:8000/status/${taskId}`)
    .then(response => response.json())
    .then(data => {
        if (data.status === "SUCCESS") {
            showResult(taskId);
        } else if (data.status !== "FAILURE") {
            setTimeout(() => checkAnalysisStatus(taskId), 5000);
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    })
    .finally(() => {
        // Riabilita il bottone "Analyze" e nasconde lo spinner quando l'analisi è completata o fallita
        document.querySelector('button[type="submit"]').disabled = false;
        document.getElementById('loader').style.display = 'none';
    });
}

function showResult(taskId) {
    fetch(`http://13.50.159.97:8000/result/${taskId}`)
    .then(response => response.json())
    .then(data => {
        if (data.result) {
            var preElement = document.createElement('pre');
            preElement.textContent = data.result;
            var resultContainer = document.getElementById('result');
            resultContainer.innerHTML = '';
            resultContainer.appendChild(preElement);
            resultContainer.style.display = 'block';
        } else {
            alert("Analysis not complete or file not found.");
        }
    })
    .catch((error) => {
        console.error('Error fetching the results:', error);
    });
}




// Gestione del disclaimer modal
var modal = document.getElementById('disclaimerModal');
var span = document.getElementsByClassName("close")[0];
var agreeButton = document.getElementById('agreeButton');

function showModal() {
    modal.style.display = "block";
}

span.onclick = function() {
    modal.style.display = "none";
}

agreeButton.addEventListener('click', function() {
    modal.style.display = "none";
});

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
