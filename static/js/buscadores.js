document.addEventListener("click", function(e) {
	let textoBuscador = document.getElementById("input-buscador"); //Cogemos el texto del buscador

	if (e.target.id === "boton-buscar-cancion") {
		let listaCanciones = document.getElementsByClassName("cancion");

		for (i = 0; i < listaCanciones.length; i++) {
			let texto = listaCanciones[i].textContent

			if (texto.toLowerCase().indexOf(textoBuscador.value.toLowerCase()) == -1) {
				listaCanciones[i].style.display = "none";
			} else {
				listaCanciones[i].style.display = ""; // Quitar "esconder"
			}
		}
	} else if (e.target.id === "boton-buscar-playlist") {
		let listaPlaylists = document.getElementsByClassName("boton-playlist");

		for (i = 0; i < listaPlaylists.length; i++) { //Comparamos los titulos con el texto del buscador.
			let texto = listaPlaylists[i].textContent

			if (texto.toLowerCase().indexOf(textoBuscador.value.toLowerCase()) == -1) { //Si no coincide, lo hace invisible
				listaPlaylists[i].style.display = "none";
			} else { //Si coincide, se muestra
				listaPlaylists[i].style.display = ""; // Quitar "esconder"
			}
		}
	}
});
