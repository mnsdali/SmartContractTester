function handleFileSelect(event) {
    var files = event.target.files;
    var selectedFile = document.getElementById('selectedFile');
    selectedFile.innerHTML = '';
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        var fileListItem = document.createElement('div');
        fileListItem.id = "ptext";
        fileListItem.innerText = file.name;
        selectedFile.appendChild(fileListItem);
        var contractDetails = document.getElementById('contractDetails');
        contractDetails.style.display = 'block';
        var x = document.getElementById('fileArea');
        x.style.display = 'block';
        var dest = document.getElementById("inform");
        dest.value = file.name;

        if (file) {
            var reader = new FileReader();
            reader.readAsText(file, "UTF-8");
            reader.onload = function (evt) {
                document.getElementById("question-input").innerText = evt.target.result;
            }
            reader.onerror = function (evt) {
                document.getElementById("question-input").innerText = "error reading file";
            }
        }
    }
}


const fileInput = document.getElementById('fileInput');

if (fileInput.files.length > 1) {
    alert('You can only upload one single contract at a time.');
}

// fileInput.addEventListener('change', (event) => {
//     const selectedFile = event.target.files[0];
//     const filePath = URL.createObjectURL(selectedFile);

//     document.getElementById("filePath").value = filePath;
    
// });


function handleFilesNumber(){
    const fileInput = document.getElementById('fileInput');

    if (fileInput.files.length > 1) {
        alert('You can only upload one single contract at a time.');
        return false;
    }

}

handleFilesNumber();

// fileInput.addEventListener('change', (event) => {
//     const selectedFile = event.target.files[0];
//     const filePath = URL.createObjectURL(selectedFile);

//     document.getElementById("filePath").value = filePath;
    
// });


