function handComplete(event){
    alert(`Задача с id: ${event.target.getAttribute("data-id")} выполнена`);
}


window.onload = function(){
    document.querySelectorAll(".btn").forEach(btn => btn.addEventListener("click", handComplete))
}