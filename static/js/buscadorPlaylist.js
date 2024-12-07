var textoBuscador = document.getElementById("label_buscador");//Cogemos el texto del buscador

var btnBusc = document.getElementById("btn_enviar");//Cogemos el boton de mandar y le damos una función
btnBusc.addEventListener("click", function (){

    let listaPlaylist = document.getElementsByClassName("boton-playlist");
    for (i = 0; i < listaPlaylist.length; i++) {//Comparamos los titulos con el texto del buscador.
        texto = listaPlaylist[i].textContent
        if (texto.toLowerCase().indexOf(textoBuscador.value.toLowerCase()) == -1){//Si no coincide, lo hace invisible
            listaPlaylist[i].style.display = "none";
        }else{ //Si coincide, se muestra
            listaPlaylist[i].style.display = "flex";
        }
    }
});