const formatearSegundos = (duracionSegundos) => {
	if (isNaN(duracionSegundos)) return "0:00"

	const minutos = Math.floor(duracionSegundos / 60).toFixed(0)
	const segundos = Math.floor(duracionSegundos - minutos * 60).toFixed(0)

	const segundosVisual = segundos.toString().length == 1 ? `0${segundos}` : segundos

	return `${minutos}:${segundosVisual}`
}

class Reproductor {
	constructor() {
		this.pausado = true
		this.audioDom = null
		this.cancionActual = null

		this.volumenActual = 1.0

		this.playlistActual = null
		this.indiceCancionActual = null

		this.arrastrandoBarra = false
		this.arrastrandoBarraVolumen = false

		this.inicializarEventos()
		this.animFrame = requestAnimationFrame(() => this.domRender())
	}

	inicializarEventos() {
		$(".parte-controles button#playPausa").on("click", () => {
			this.reproducirPararCancion()
		})
		$(".parte-controles button#anterior").on("click", () => {
			this.anteriorCancion()
		})
		$(".parte-controles button#siguiente").on("click", () => {
			this.siguienteCancion()
		})

		$(".parte-controles .barra").on("mousedown", (e) => {
			this.arrastrandoBarra = true;
			this.clickEnBarra(e.pageX)
		})

		$(".parte-volumen .barra").on("mousedown", (e) => {
			this.arrastrandoBarraVolumen = true;
			this.clickEnBarraVolumen(e.pageX)
		})

		$(document).on("mouseup", (e) => {
			this.arrastrandoBarra = false;
			this.arrastrandoBarraVolumen = false;
		})

		$(document).on("mousemove", (e) => {
			this.clickEnBarra(e.pageX)
			this.clickEnBarraVolumen(e.pageX)
		})
	}

	clickEnBarra(ratonX) {
		if (this.audioDom === null || !this.arrastrandoBarra) return;

		const barraX = $(".parte-controles .barra").offset().left;

		const x = ratonX - barraX;

		const barraAncho = $(".parte-controles .barra").width();

		const nuevoProgreso = Math.max(0.00, Math.min(x / barraAncho, 100.00))
		this.audioDom.currentTime = this.audioDom.duration * nuevoProgreso;
	}

	clickEnBarraVolumen(ratonX) {
		if (this.audioDom === null || !this.arrastrandoBarraVolumen) return;

		const barraX = $(".parte-volumen .barra").offset().left;
		const x = ratonX - barraX;
		const barraAncho = $(".parte-volumen .barra").width();

		const nuevoVolumen = Math.max(0.00, Math.min(x / barraAncho, 1.00))

		this.volumenActual = nuevoVolumen;
		this.audioDom.volume = nuevoVolumen;
	}

	async domRender() {
		// Actualizar la informacion necesaria. Se ejecuta una vez por frame
		if (this.audioDom !== null) {
			const duracion = this.audioDom.duration;
			const actual = this.audioDom.currentTime;

			$(".reproductor").find(".tiempo-maximo").text(formatearSegundos(duracion))

			const progreso = actual / duracion
			$(".parte-controles .progreso .barra-progreso").css("--progreso", `${progreso * 100}%`)
			$(".parte-controles .progreso .tiempo-actual").text(formatearSegundos(actual))

			$(".parte-volumen .barra-progreso").css("--progreso", `${this.audioDom.volume * 100}%`)
			$(".parte-volumen .volumen-porcentaje").text(`${Math.floor(this.audioDom.volume * 100)}%`);

			if (this.audioDom.ended) {
				const cancionReproducida = await this.siguienteCancion()

				// Sucede cuando acaba una cancion que no
				// esta en la playlist.
				if (!cancionReproducida) {
					$(".parte-controles .progreso .barra-progreso").css("--progreso", `0%`)

					this.audioDom.pause();
					this.audioDom.currentTime = 0;

					this.pausado = true;
				}
			}

			$(".parte-controles button#playPausa").toggleClass("pausado", this.pausado)
		} else {
			$(".parte-controles .progreso .tiempo-actual").text(formatearSegundos(0))
			$(".parte-controles .progreso .tiempo-maximo").text(formatearSegundos(0))
		}


		$(".parte-controles button#playPausa").prop("disabled", this.audioDom === null)

		$(".parte-controles button#anterior").prop("disabled", !this.playlistActual || this.audioDom === null)
		$(".parte-controles button#siguiente").prop("disabled", !this.playlistActual || this.audioDom === null)

		$(".parte-controles .progreso").toggleClass("deshabilitado", this.audioDom === null)

		this.animFrame = requestAnimationFrame(() => this.domRender())
	}

	async reproducirCancion(id, playlistId = -1) {
		if (playlistId === -1) {
			const quitarPlaylist = this.playlistActual !== null
			this.reproducirCancionUnica(id, quitarPlaylist)
		} else
			this.reproducirPlaylist(id, playlistId)
	}

	async reproducirCancionUnica(id, quitarPlaylist = false) {
		// Si se hace click en una cancion fuera de una playlist,
		// se quita la playlist actual (si se esta reproduciendo).
		if (quitarPlaylist) {
			this.playlistActual = null;
			this.indiceCancionActual = null;
		}

		// Conseguir informacion sobre la cancion
		let cancion = {
			id,
			url: `/api/cancion/${id}/archivo`
		}

		await $.ajax({
			url: `/api/cancion/${id}/informacion`,
			success: function(datos) {
				cancion.titulo = datos.nombre
				cancion.artistas = datos.artistas
			},
			error: function(xhr, estado, error) {
				console.error("Error al conseguir informacion de la cancion: ", error)
			}
		})

		this.cancionActual = cancion

		// Si hay una cancion reproduciendose, pararla y eliminarla
		if (this.audioDom !== null) {
			this.audioDom.pause()
			this.audioDom = null
		}

		// Crear nuevo elemento de <Audio> con la url de la cancion
		this.audioDom = new Audio(cancion.url)
		this.audioDom.volume = this.volumenActual
		this.audioDom.play()
		if (this.pausado)
			this.reproducirPararCancion()

		// Actualizar informacion del reproductor
		$(".reproductor .parte-informacion").removeClass("vacia")
		$(".reproductor .parte-informacion .titulo-cancion").text(cancion.titulo)
		$(".reproductor .parte-informacion .artista-cancion").text(cancion.artistas.join(", "))
		$(".reproductor .parte-informacion .cover-cancion").css("--cover", `url('/api/cancion/${cancion.id}/cover')`)

		// Colocar como activa en la pagina a la cancion actual
		this.gestionarCambioPagina()
	}

	async reproducirPlaylist(cancionId, playlistId) {
		await $.ajax({
			url: `/api/playlist/${playlistId}/informacion`,
			success: async (datos) => {
				this.playlistActual = {
					id: playlistId,
					canciones: datos["canciones"]
				}
			},
			error: function(xhr, estado, error) {
				console.error("Error al conseguir informacion de la playlist: ", error)
			}
		})

		// Buscar la ID especifica de la cancion clickeada
		let indice = this.playlistActual.canciones.findIndex((cancion) => {
			return cancion["id"] === cancionId;
		})

		if (indice === -1)
			indice = 0;

		this.indiceCancionActual = indice;
		const id = this.playlistActual.canciones[indice]["id"];
		this.reproducirCancionUnica(id)
	}

	async anteriorCancion() {
		if (this.playlistActual === null)
			return;

		this.indiceCancionActual--;
		if (this.indiceCancionActual < 0)
			this.indiceCancionActual = this.playlistActual.canciones.length - 1;

		await this.reproducirCancionUnica(this.playlistActual.canciones[this.indiceCancionActual]["id"])
	}

	async siguienteCancion() {
		if (this.playlistActual === null)
			return false;

		this.indiceCancionActual++;
		if (this.indiceCancionActual >= this.playlistActual.canciones.length)
			this.indiceCancionActual = 0;

		await this.reproducirCancionUnica(this.playlistActual.canciones[this.indiceCancionActual]["id"])
		return true;
	}


	reproducirPararCancion() {
		if (this.audioDom === null) return;

		this.pausado = !this.pausado
		if (this.pausado) {
			this.audioDom.pause()
		} else {
			this.audioDom.play()
		}
	}

	gestionarCambioPagina() {
		if (this.cancionActual === null) return;

		// Quitar activa en todas las canciones de HTML
		$(".cancion").removeClass("activa")

		// Colocar el estado de la cancion clickeada como activa
		if (this.playlistActual === null)
			$(`.cancion[data-cancion-id=${this.cancionActual.id}]:not([data-playlist-id])`).addClass("activa")
		else
			$(`.cancion[data-cancion-id=${this.cancionActual.id}][data-playlist-id=${this.playlistActual.id}]`).addClass("activa")
	}
}
