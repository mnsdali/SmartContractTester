

function openInVSCode(filePath) {
    alert("dacc");
    const { exec } = require('child_process');
    const os = require('os');
    let vscodePath;
    
    switch (os.platform()) {
        case 'win32':
        vscodePath = 'E:\\Users\\USER\\AppData\\Local\\Programs\\Microsoft VS Code\\bin\\code.cmd';
        break;
        case 'darwin':
        vscodePath = '/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code';
        break;
        case 'linux':
        vscodePath = '/usr/share/code/bin/code';
        break;
        default:
        alert(`Unsupported platform`);
        return;
    }
    
    
    exec(`${vscodePath} ${filePath}`, (err, stdout, stderr) => {
        if (err) {
        alert(`Failed to open file in VS Code: ${err}`);
        }
    });
    }
    




function generateTestCases(){

    alert('generateTestCases');

}