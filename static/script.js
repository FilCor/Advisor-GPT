document.getElementById('analysisForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var companyName = document.getElementById('company').value;
    var analyzeButton = document.querySelector('button[type="submit"]');
    var loader = document.getElementById('loader');

    // Disabilita il bottone "Analyze" e mostra lo spinner
    analyzeButton.disabled = true;
    loader.style.display = 'block';

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
        // Riabilita il bottone "Analyze" e nasconde lo spinner in caso di errore
        analyzeButton.disabled = false;
        loader.style.display = 'none';
    });
});

function checkAnalysisStatus(taskId) {
    fetch(`http://13.50.159.97:8000/status/${taskId}`)
    .then(response => response.json())
    .then(data => {
        console.log('Status data:', data); // Aggiungi questo log per debug
        if (data.status === "SUCCESS") {
            document.getElementById('statusText').innerText = 'Analysis Complete!';
            document.getElementById('statusText').style.color = 'green';
            document.getElementById('loader').style.display = 'none'; // Nasconde lo spinner
            document.getElementById('gifContainer').style.display = 'none'; // Nasconde la GIF
            showResult(taskId); // Richiede il risultato
        } else if (data.status === "FAILURE") {
            console.error('Analysis failed');
            alert("Analysis failed or an error occurred.");
            document.getElementById('loader').style.display = 'none'; // Nasconde lo spinner
        } else {
            // Se lo stato non è né "Complete" né "Failed", continua a controllare lo stato
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
            // Prepara il contenuto mantenendo la formattazione
            var resultContainer = document.getElementById('result');
            resultContainer.innerHTML = ''; // Pulisce il contenitore
            var preElement = document.createElement('pre');
            preElement.textContent = data.result;
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
