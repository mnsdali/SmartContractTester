const hoorayText = document.getElementById("hooray-text");
const imageContainer = document.getElementById("image-container");
const hoorayImage = document.getElementById("hooray-image");

hoorayText.addEventListener("mousemove", function(event) {
  var x = event.clientX;
  var y = event.clientY;
  x+=20;
  y-=40;
  imageContainer.style.display = "block";
  imageContainer.style.left = `${x}px`;
  imageContainer.style.top = `${y}px`;
  clearTimeout(hideTimeout);
});

hoorayText.addEventListener("mouseleave", function() {
  hideTimeout = setTimeout(function() {
    imageContainer.style.display = "none";
  }, 1);});


const compileBtn = document.getElementById("compileBtn");
const imageContainer2 = document.getElementById("image-container2");
const compileImage = document.getElementById("compile-deploy-image");
  
compileBtn.addEventListener("mousemove", function(event) {
    var x = event.clientX;
    var y = event.clientY;
    x+=20;
    y-=40;
    imageContainer2.style.display = "block";
    imageContainer2.style.left = `${x}px`;
    imageContainer2.style.top = `${y}px`;
    clearTimeout(hideTimeout);
  });
  
  compileBtn.addEventListener("mouseleave", function() {
    hideTimeout = setTimeout(function() {
      imageContainer2.style.display = "none";
    }, 1);});
  
const auditBtn = document.getElementById("auditBtn");
const imageContainer3 = document.getElementById("image-container3");
const auditImage = document.getElementById("audit-image");
  
auditBtn.addEventListener("mousemove", function(event) {
    var x = event.clientX;
    var y = event.clientY;
    x+=20;
    y-=40;
    imageContainer3.style.display = "block";
    imageContainer3.style.left = `${x}px`;
    imageContainer3.style.top = `${y}px`;
    clearTimeout(hideTimeout);
  });
  
auditBtn.addEventListener("mouseleave", function() {
    hideTimeout = setTimeout(function() {
      imageContainer3.style.display = "none";
    }, 1);});

function showAuditorContent(){
   document.getElementById("auditorContent").classList.remove('hidden');
}




// audit_btn.addEventListener('click', () => {
//   alert("I was here");
//   loading.style.display = "flex";
//   chatContainer.style.display="none";
//   setTimeout(() => {
//     alert("gone");
//     loading.style.display = "none";
//     chatContainer.style.display="block";
//   }, 15000); // Set the timeout to 5 seconds (5000 milliseconds)
// });
//  audit_btn.addEventListener('change', () => {
//      alert(audit_btn.disabled);
//       loading.style.display = (audit_btn.disabled) ? "flex" : "none";

// });

auditBtn.addEventListener('click', () =>{

  const auditor = document.getElementById("auditorContent");
  auditor.style.display= "block";
});