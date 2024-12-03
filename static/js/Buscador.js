
var textoBuscador = document.getElementById("label_buscador");//Cogemos el texto del buscador

var btnBusc = document.getElementById("btn_enviar");//Cogemos el boton de mandar y le damos una función
btnBusc.addEventListener("click", function (){

    let listaCanciones = document.getElementsByClassName("cancion");

    for (i = 0; i < listaCanciones.length; i++) {
        texto = listaCanciones[i].textContent
        if (texto.toLowerCase().indexOf(textoBuscador.value.toLowerCase()) == -1){
            listaCanciones[i].style.display = "none";
        }else{
            listaCanciones[i].style.display = "flex";
        }
    }
});
