const formatearSegundos = (duracionSegundos) => {
	const minutos = Math.floor(duracionSegundos / 60).toFixed(0)
	const segundos = Math.floor(duracionSegundos - minutos * 60).toFixed(0)

	const segundosVisual = segundos.toString().length == 1 ? `0${segundos}` : segundos

	return `${minutos}:${segundosVisual}`
}

$(document).ready(() => {
	let reproductor = {
		pausado: true,
		audioDom: null,
	}

	// Codigo principal del reproductor
	console.log("Reproductor iniciado [una vez solamente].")

	const elementoReproductor = $(".reproductor")

	const reproducirCancion = (datosCancion) => {
		$(".cancion").removeClass("activa")

		if (reproductor.audioDom !== null) {
			reproductor.audioDom.pause()
			reproductor.audioDom = null
		}

		reproductor.audioDom = new Audio(datosCancion.url)
		reproductor.audioDom.play()
		if (reproductor.pausado)
			clickPlayPausa()

		$(`.cancion[data-cancion-id=${datosCancion.id}]`).addClass("activa")

		$(elementoReproductor).find(".titulo-cancion").text(datosCancion.titulo)
		$(elementoReproductor).find(".artista-cancion").text(datosCancion.artistas.join(", "))
	}

	const clickPlayPausa = () => {
		if (reproductor.audioDom === null) return;

		reproductor.pausado = !reproductor.pausado
		if (reproductor.pausado) {
			$(".parte-controles button#playPausa").addClass("pausado")
			reproductor.audioDom.pause()
		} else {
			$(".parte-controles button#playPausa").removeClass("pausado")
			reproductor.audioDom.play()
		}
	}

	let frameIdx = 0;
	const iterar = () => {
		if (reproductor.audioDom !== null) {
			const duracion = reproductor.audioDom.duration;
			const actual = reproductor.audioDom.currentTime;

			$(elementoReproductor).find(".tiempo-maximo").text(formatearSegundos(duracion))

			const progreso = actual / duracion
			$(".parte-controles .progreso .barra-progreso").css("--progreso", `${progreso * 100}%`)
			$(".parte-controles .progreso .tiempo-actual").text(formatearSegundos(actual))

			if (reproductor.audioDom.ended) {
				console.log("Audio fin")
			}
		} else {
			$(".parte-controles .progreso .tiempo-actual").text(formatearSegundos(0))
			$(".parte-controles .progreso .tiempo-maximo").text(formatearSegundos(0))
		}

		// Logica aqui
		frameIdx = requestAnimationFrame(iterar);
	}
	frameIdx = requestAnimationFrame(iterar)

	// reproducirCancion({
	// 	id: "...",
	// 	titulo: "El titulo",
	// 	artistas: ["El artista"],
	// 	url: "/audio",
	// })

	// Eventos/clicks del DOM
	$(".parte-controles button#playPausa").on("click", () => {
		clickPlayPausa()
	})

	$(".cancion").on("click", (e) => {
		const cancionId = $(e.target).data("cancion-id")

		$.ajax({
			url: `/api/audio/informacion/${cancionId}`,
			success: function(datos) {
				console.log(datos)
				reproducirCancion({
					id: cancionId,
					titulo: datos.nombre,
					artistas: datos.artistas,
					url: `/api/audio/archivo/${cancionId}`
				})
			},
			error: function(xhr, estado, error) {
				console.error("Error al conseguir informacion de la cancion: ", error)
			}
		})
	})
})
