// Acciones de playlists (hacer click en una playlist, crear una nueva playlist, etc)
$(document).on("click", ".boton-playlist", (e) => {
	const elemento = $(e.target).closest(".boton-playlist");
	const playlistID = $(elemento).data("playlist-id");
	reemplazarContenido(`/playlist/${playlistID}`);
})

$(document).on("click", "#boton-crear-playlist", async (e) => {
	await $.ajax({
		url: `/api/playlist/crear`,
		method: "POST",
		contentType: "application/json",
		success: function(playlistID) {
			reemplazarContenido(`/playlist/${playlistID}`);
		},
		error: function(xhr, estado, error) {
			alert(`Error al actualizar la informacion de la playlist: \"${xhr.responseText}\"`);
		}
	})
})
