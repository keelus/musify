// Script de ejemplo para cambiar el contenido del cuerpo sin refrescar.
// Por ahora solo sirve para ir a la playlist, hay que extenderlo.

// Actualiza el titulo dinamicamente dependiendo el contenido de la URL.
// Se ejecuta al cambiar de URL y al visitar por primera vez.
const actualizarTitulo = (rutaDestino) => {
	if (rutaDestino === "/") {
		document.title = "Canciones - Musify"
		return;
	}
	if (rutaDestino === "/playlists") {
		document.title = "Tus playlists - Musify"
		return;
	}

	if (rutaDestino.indexOf("/playlist/") !== -1) {
		const playlistID = rutaDestino.replace("/playlist/", "");
		document.title = `Playlist [${playlistID}] - Musify`
		return;
	}

	document.title = "Musify";
}

const reemplazarContenido = async (rutaDestino) => {
	if (rutaDestino === "/") {
		$(".boton-seccion[data-seccion-destino='canciones']").addClass("activo")
		$(".boton-seccion[data-seccion-destino='playlists']").removeClass("activo")
	} else if (rutaDestino === "/playlists") {
		$(".boton-seccion[data-seccion-destino='canciones']").removeClass("activo")
		$(".boton-seccion[data-seccion-destino='playlists']").addClass("activo")
		document.title = "Tus playlists - Musify"
	} else {
		$(".boton-seccion[data-seccion-destino='canciones']").removeClass("activo")
		$(".boton-seccion[data-seccion-destino='playlists']").removeClass("activo")
	}

	// Vaciamos el contenedor
	$("main#contenedor").html("")
	// TODO: Se podria agregar un "cargando" o algo similar

	// Reemplazamos la URL sin refrescar la pagina
	window.history.replaceState(null, document.title, rutaDestino)

	// Actualizamos el titulo de la pestaña
	actualizarTitulo(rutaDestino);

	// Hacemos una peticion normal, pero colocamos un 
	// header HTTP extra para que Django nos devuelva
	// solamente el contenido reducido, y no la
	// pagina index con el contenido.
	$.ajax({
		url: rutaDestino,
		headers: {
			"Reducido": "true",
		},
		success: function(datos) {
			$("main#contenedor").html(datos)
			document.dispatchEvent(new Event("cambioDePagina"))
		},
		error: function(xhr, estado, error) {
			console.error("Error al cargar el contenido: ", error)
		}
	})
}

$(".boton-seccion").on("click", (e) => {
	const seccionDestino = $(e.target).data("seccion-destino")
	switch (seccionDestino) {
		case "canciones":
			reemplazarContenido("/"); // Indice es alias de canciones
			break;
		case "playlists":
			reemplazarContenido("/playlists");
			break;
		case "playlist":
			const playlistId = $(e.target).data("playlist-id")
			reemplazarContenido(`/playlist/${playlistId}`);
			break;
	}
})

$(document).ready(() => {
	actualizarTitulo(document.location.pathname);

	const reproductor = new Reproductor();

	$(document).on("click", ".cancion", (e) => {
		const elementoCancion = $(e.target).closest(".cancion")
		const cancionId = $(elementoCancion).data("cancion-id")
		const playlistId = $(elementoCancion).data("playlist-id")

		if (playlistId === undefined)
			reproductor.reproducirCancion(cancionId)
		else
			reproductor.reproducirCancion(cancionId, playlistId)
	})

	$(document).on("cambioDePagina", () => reproductor.gestionarCambioPagina())
})
