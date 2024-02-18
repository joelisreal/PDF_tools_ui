// Toggle navigation visibility when clicking on h1
// document.querySelector('header h1').addEventListener('click', function() {
//     document.querySelector('nav').classList.toggle('show');
// });

function myFunction() {
    var x = document.getElementById("myLinks");
    if (x.style.display === "block") {
      x.style.display = "none";
    } else {
      x.style.display = "block";
    }
  }