document.getElementById('analysisForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var companyName = document.getElementById('company').value;
    var analyzeButton = document.querySelector('button[type="submit"]');
    var loader = document.getElementById('loader'); // Utilizza questo elemento come spinner
    var gifContainer = document.getElementById('gifContainer'); // Seleziona il contenitore della GIF

    // Disabilita il bottone "Analyze" e mostra sia lo spinner che la GIF
    analyzeButton.disabled = true;
    loader.style.display = 'block';
    gifContainer.style.display = 'block'; // Mostra la GIF

    fetch('https://www.filotech.eu/analyze/', {
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
        // Riabilita il bottone "Analyze" e nasconde sia lo spinner che la GIF in caso di errore
        analyzeButton.disabled = false;
        loader.style.display = 'none';
        gifContainer.style.display = 'none'; // Nasconde la GIF
    });
});

function checkAnalysisStatus(taskId) {
    fetch(`https://www.filotech.eu/status/${taskId}`)
    .then(response => response.json())
    .then(data => {
        console.log('Status data:', data); // Aggiungi questo log per debug
        if (data.status === "SUCCESS") {
            document.getElementById('statusText').innerText = 'Analysis Complete!';
            document.getElementById('statusText').style.color = 'green';
            document.getElementById('loader').style.display = 'none'; // Nasconde lo spinner
            document.getElementById('gifContainer').style.display = 'none'; // Nasconde la GIF
            document.querySelector('button[type="submit"]').disabled = false; // Riabilita il bottone "Analyze"
            showResult(taskId); // Richiede il risultato
        } else if (data.status === "FAILURE") {
            console.error('Analysis failed');
            alert("Analysis failed or an error occurred.");
            document.getElementById('loader').style.display = 'none'; // Nasconde lo spinner
            document.querySelector('button[type="submit"]').disabled = false; // Riabilita il bottone "Analyze"
        } else {
            // Se lo stato non è né "Complete" né "Failed", continua a controllare lo stato
            setTimeout(() => checkAnalysisStatus(taskId), 5000);
            document.getElementById('statusText').innerText = 'Analyzing!';
            document.getElementById('statusText').style.color = 'yellow';
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('loader').style.display = 'none'; // Nasconde lo spinner in caso di errore
        document.querySelector('button[type="submit"]').disabled = false; // Riabilita il bottone "Analyze" in caso di errore
    });
}


function showResult(taskId) {
    fetch(`https://www.filotech.eu/result/${taskId}`)
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
