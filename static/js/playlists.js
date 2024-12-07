// Acciones de playlists (hacer click en una playlist, crear una nueva playlist, etc)
$(document).on("click", ".boton-playlist", (e) => {
	const playlistID = $(e.target).data("playlist-id");
	reemplazarContenido(`/playlist/${playlistID}`);
})



