// Acciones de playlists (hacer click en una playlist, crear una nueva playlist, etc)
$(document).on("click", ".boton-playlist", (e) => {
	const elemento = $(e.target).closest(".boton-playlist");
	const playlistID = $(elemento).data("playlist-id");
	reemplazarContenido(`/playlist/${playlistID}`);
})
