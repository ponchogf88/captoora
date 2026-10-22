import os
import subprocess

script = [
    ("Eddy (Español (México))", "¡Hola Poncho! Bienvenidos a esta sesión ejecutiva especial de Captoora Studio. Si vienes manejando, relájate, pon atención al camino y escucha con calma porque aquí desglosamos todo el plan maestro para este 31 de octubre."),
    ("Paulina", "Totalmente. Y es que lo que se viene es una producción de primer nivel: veinticinco influencers de Farmasi en tu estudio de Colinas de San Jerónimo. Pero para que esto no sea un dolor de cabeza, hay reglas operativas y un candado muy inteligente que acabas de plantear."),
    ("Eddy (Español (México))", "Exacto, Valeria. Hablemos de lo primero: la lista previa de las veinticinco invitadas. Poncho tiene toda la razón: no podemos permitir que vengan veinticinco chicas a tomarse fotos gratis y que al final solo cinco te etiqueten. Eso no es negocio."),
    ("Paulina", "Para nada. El protocolo exige que la líder de Farmasi te entregue cuarenta y ocho horas antes del evento la lista nominal completa: nombre completo, teléfono y cuenta oficial de Instagram de cada una de las veinticinco chicas. Esto te permite dos cosas fundamentales."),
    ("Eddy (Español (México))", "La primera: tener listo su contrato impreso con sus datos para que solo lleguen a firmar en treinta segundos con tu hermana. Y la segunda: auditar sus perfiles antes de que pisen el estudio."),
    ("Paulina", "Y aquí entra el candado maestro de entrega que protege a Poncho: la regla de oro de la liberación de fotos. Durante el evento, ellas van a ver sus fotos en la pantalla de la televisión en vivo, pero el material en alta resolución sin marca de agua no se envía de inmediato."),
    ("Eddy (Español (México))", "Exacto. Se les envía un enlace con vistas previas en miniatura con sello de agua de Captoora. El contrato estipula que para recibir su galería oficial descargable en cuatro ka, tienen que subir su historia y su video etiquetando a arroba captoora y a Alfonso Gutiérrez. En cuanto el sistema verifica la etiqueta, se libera su paquete final. Así aseguras cien por ciento de cumplimiento."),
    ("Paulina", "Ahora hablemos de la experiencia del día del evento. Tu casa se divide en dos mundos completamente independientes. En la planta baja está el área social, el chill out y la barra de mimosas. Y aquí tu hermana juega un papel protagónico como anfitriona vip."),
    ("Eddy (Español (México))", "Tener a tu hermana recibiéndolas con una sonrisa, sirviendo las mimosas frías con popotes oro rosa para que no se les despinte el labial, genera una vibra de confianza y confort que ningún fotógrafo solitario puede dar. Mientras seis chicas están arriba contigo disparando, las otras diecinueve están abajo disfrutando, conviviendo y haciéndose selfies en el espejo."),
    ("Paulina", "Y en la planta alta están tus dos escenarios de rodaje. El set número uno es el ciclorama blanco puro para la sesión deportiva y wellness. Inspirada en la sesión de Karla, con mancuernas, tapete y los suplementos de Nutriplus. Iluminación brillante que resalta la energía y el tono muscular."),
    ("Eddy (Español (México))", "Y el set número dos, que es tu gran idea: el set oscuro de Beauty CEO con la Gran Mesa de madera. Esta mesa expandible funciona como vitrina de lujo para los productos Dr. C. Tuna y labiales. Las chicas se paran erguidas, recargan el codo en la mesa y ponen el dedo en la frente o la mano en el mentón. Esa pose soberbia de directoria ejecutiva les fascina porque proyecta estatus y liderazgo de equipo."),
    ("Paulina", "El ritmo de disparo con tu Nikon D3500 y flashes Godox es de siete minutos cronometrados por modelo. Con las poses prediseñadas, tú no tienes que pensar nada en el momento; solo diriges la mirada, disparas y despachas."),
    ("Eddy (Español (México))", "A la una y cuarto de la tarde ocurre el clímax: la foto grupal de todas en el ciclorama brindando con sus copas arriba. Y justo ahí, cuando la energía y la emoción están al máximo, viene la fase cuatro: los testimonios ping pong."),
    ("Paulina", "Con tu celular en tripié y micrófono de solapa inalámbrico, les haces cuatro preguntas rápidas de cuarenta y cinco segundos a cada una: cómo se sintieron, cómo vivieron la dirección de poses de Poncho y por qué recomiendan Captoora Studio."),
    ("Eddy (Español (México))", "Al final de la jornada tienes en tu disco duro veinticinco testimonios en video listos. La estrategia es publicarlos a razón de dos testimonios por semana, los martes y jueves. Eso te da doce semanas consecutivas, tres meses enteros de prueba social y credibilidad para cerrar clientes en Monterrey."),
    ("Paulina", "El contrato de una página bajo la ley de derechos de autor ya está listo para imprimir. La lista previa garantiza el control, y tus dos sets están preparados. Poncho, tienes una producción de clase mundial en tus manos. Concéntrate en tu camino, maneja con cuidado y prepárate para brillar este treinta y uno de octubre.")
]

temp_files = []
for idx, (voice, text) in enumerate(script):
    filename = f"/tmp/pod_part_{idx:02d}.aiff"
    print(f"Generando parte {idx+1}/{len(script)} con voz {voice}...")
    cmd = ["say", "-v", voice, "-o", filename, text]
    subprocess.run(cmd, check=True)
    temp_files.append(filename)

# Concatenar todo usando sox o ffmpeg o afconvert
output_m4a = "/Users/user/captoora/PODCAST_CAPTOORA_EVENTO_FARMASI_31_OCTUBRE.m4a"
file_list_txt = "/tmp/podcast_parts.txt"
with open(file_list_txt, "w") as f:
    for tf in temp_files:
        f.write(f"file '{tf}'\n")

print("Uniendo partes del podcast...")
concat_cmd = f"ffmpeg -y -f concat -safe 0 -i {file_list_txt} -c:a aac -b:a 128k '{output_m4a}'"
os.system(concat_cmd)

# Limpiar temporales
for tf in temp_files:
    if os.path.exists(tf):
        os.remove(tf)

print(f"Podcast maestro generado en: {output_m4a}")
