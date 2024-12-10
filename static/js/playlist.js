// Acciones de playlist (hacer click en reproducir playlist, reproducir cancion, elimiar cancion, etc)

//		<div class="imagen" id="playlist-cover" style="--imagen:url('{{ playlist.cover }}');"></div>
//			<h1 id="playlist-nombre">{{ playlist.nombre }}</h1>
//			<input placeholder="Nombre de la playlist..." id="input-playlist-nombre" />
//		<div>
//			<button class="cancelar">Cancelar</button>
//			<button>Guardar informacion</button>
//		</div>


$(document).on("click", "#playlist-editar", (e) => {
	$("header.principal").removeClass("mostrar")
	$("header.edicion").addClass("mostrar")

	$("#input-playlist-nombre").val($("#playlist-nombre").text())
	$("#input-playlist-cover").val($("#playlist-cover").attr("src"))
})

$(document).on("click", "#playlist-eliminar", async (e) => {
	const playlistId = $("#contenido").data("playlist-id")

	await $.ajax({
		url: `/api/playlist/${playlistId}/eliminar`,
		method: "GET",
		success: function(datos) {
			reemplazarContenido("/playlists")
		},
		error: function(xhr, estado, error) {
			alert(`Error al eliminar la playlist: \"${xhr.responseText}\"`);
		}
	})
})

$(document).on("click", "#playlist-anyadir", async (e) => {
	const playlistId = $("#contenido").data("playlist-id")

	// Mostrar modal de listado de canciones
	await $.ajax({
		url: `/api/playlist/${playlistId}/cancionesAnyadibles`,
		method: "GET",
		contentType: "application/json",
		success: function(datos) {
			let canciones = datos["canciones"]

			if (canciones.length == 0)
				return alert("¡Ya has añadido todas las canciones!")

			let cancionesString = canciones.map((cancion) => (
				`<div class="cancion no-clickable" style="align-items:center;">
					<div class="cover" style="--cover:url('/api/cancion/${cancion.id}/cover')"></div>
						<div class="informacion" style="flex:1;">
							<span class="titulo">${cancion.nombre}</span>
						</div>
					<button style="height:30px;" class="playlist-anyadir-cancion" data-cancion-id="${cancion.id}">Añadir</button>
				</div>`
			)).join("")

			$("body").append(`
		<div id="playlist-anyadir-modal" style="position:absolute;left:0;top:0;width:100%;height:100%;display:flex;justify-content:center;align-items:center;background-color:rgba(0, 0, 0, .6);">
			<div style="background-color:#18181b;padding:10px;border-radius:10px;border:1px solid #222;width:500px;">
				<h1>Añadir una canción</h1>
				<div style="display:flex;flex-direction:column;max-height:500px;overflow-y:auto;">
					${cancionesString}
				</div>
				<button class="boton-cancelar" style="margin-top:10px;" id="playlist-anyadir-salir">
					Salir
				</button>
			</div>
		</div>
		`)
		},
		error: function(xhr, estado, error) {
			alert(`Error al cargar las canciones añadibles a la playlist: \"${xhr.responseText}\"`);
		}
	})

})

$(document).on("click", ".playlist-anyadir-cancion", async (e) => {
	const playlistId = $("#contenido").data("playlist-id")
	const cancionId = $(e.target).data("cancion-id")

	// Mostrar modal de listado de canciones
	await $.ajax({
		url: `/api/playlist/${playlistId}/anyadirCancion/${cancionId}`,
		method: "GET",
		contentType: "application/json",
		success: function(datos) {
			$("#playlist-anyadir-modal").remove()
			reemplazarContenido(`/playlist/${playlistId}`)
		},
		error: function(xhr, estado, error) {
			alert(`Error al añadir la cancion a la playlist: \"${xhr.responseText}\"`);
		}
	})
})

$(document).on("click", ".playlist-eliminar-cancion", async (e) => {
	const playlistId = $("#contenido").data("playlist-id")
	const cancionId = $(e.target).data("cancion-id")

	// Mostrar modal de listado de canciones
	await $.ajax({
		url: `/api/playlist/${playlistId}/eliminarCancion/${cancionId}`,
		method: "GET",
		contentType: "application/json",
		success: function(datos) {
			reemplazarContenido(`/playlist/${playlistId}`)
		},
		error: function(xhr, estado, error) {
			alert(`Error al eliminar la cancion de la playlist: \"${xhr.responseText}\"`);
		}
	})
})

$(document).on("click", "#playlist-anyadir-modal", async (e) => {
	const elemento = $(e.target);
	if (elemento.attr("id") === "playlist-anyadir-modal")
		$("#playlist-anyadir-modal").remove()
})

$(document).on("click", "#playlist-anyadir-salir", async (e) => {
	$("#playlist-anyadir-modal").remove()
})

const cerrarModoEdicion = () => {
	$("header.principal").addClass("mostrar")
	$("header.edicion").removeClass("mostrar")
}

$(document).on("click", "#playlist-guardar", async (e) => {
	const nuevoNombre = $("#input-playlist-nombre").val()
	if (nuevoNombre.trim() === "") {
		alert("El nombre de la playlist no puede estar vacío!");
		return;
	}

	const nuevaCover = $("#input-playlist-cover").val()
	const playlistId = $("#contenido").data("playlist-id")

	// Intentar guardar datos
	await $.ajax({
		url: `/api/playlist/${playlistId}/actualizarInformacion`,
		method: "POST",
		contentType: "application/json",
		data: JSON.stringify({
			nombre: nuevoNombre,
			cover: nuevaCover,
		}),
		success: function(datos) {
			$("#playlist-nombre").text(nuevoNombre)
			$("#playlist-cover").attr("src", nuevaCover)
			cerrarModoEdicion()
		},
		error: function(xhr, estado, error) {
			alert(`Error al actualizar la informacion de la playlist: \"${xhr.responseText}\"`);
			cerrarModoEdicion()
		}
	})
})

$(document).on("click", "#playlist-cancelar", (e) => {
	cerrarModoEdicion()
})
