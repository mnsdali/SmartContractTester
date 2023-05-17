const inputs = document.querySelectorAll('input[type="text"]');
    
// Define a regex pattern for allowed characters
const patternArray = /^[a-zA-Z0-9,. \-]+$/;
const patternAlphaNum = /^[a-zA-Z0-9. \-]+$/;

// Add an event listener to the input element
for (input of inputs)
{
    input.addEventListener('input', (event) => {
        
        // Get the current value of the input
        let value = event.target.value;
        
        // Test the value against the regex pattern
        if (event.target.classList.contains('arr')){
            if ( !patternArray.test(value)  || value.includes('--') || value.includes(',,') 
                        || value.includes('  ') || value.includes('..') || value.includes(' ,') ) {
            // If the value does not match the pattern, remove the last character
                        event.target.value = value.slice(0, -1);
            }
        }else{
            if (!patternAlphaNum.test(value) || value.includes('--') || value.includes(',,') 
                        || value.includes('  ') || value.includes('..')  || value.includes(' ,') ) {
            // If the value does not match the pattern, remove the last character
            event.target.value = value.slice(0, -1);
            }
        }
        
    });
}