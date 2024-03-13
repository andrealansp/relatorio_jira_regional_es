document.querySelectorAll('.nav-link').forEach
(link=> {
    if(link.href === window.location.href){
        link.setAttribute('aria-current', 'page')
        link.classList.add('active')
    }
})

function toogle_pdf(){
var pdf_div = document.getElementById("relatorio")
var visualizar_div = document.getElementById("visualizar")
if (pdf_div.style.display==="none"){
pdf_div.style.display = "block";
visualizar_div.style.display = "none"

} else {
    pdf_div.style.display = "none";
    visualizar_div.style.display = "block"
  }
}

