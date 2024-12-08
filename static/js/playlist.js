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
	const playlistId = $("#playlist-guardar").data("playlist-id")

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
