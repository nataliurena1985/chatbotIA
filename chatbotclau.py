import openai, PyPDF2, requests, tempfile, os

openai.api_key = os.getenv("OPENAI_API_KEY")

def descargar_pdf(url):
    r = requests.get(url)
    r.raise_for_status()
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp.write(r.content)
    temp.close()
    return temp.name

def extraer_texto_pdf(ruta):
    lector = PyPDF2.PdfReader(ruta)
    texto = ""
    for pag in lector.pages:
        texto += pag.extract_text() or ""
    return texto

url = "https://services.google.com/fh/files/misc/ciso-guide-to-security-transformation.pdf"
ruta = descargar_pdf(url)
contenido = extraer_texto_pdf(ruta)

if not contenido.strip():
    print("⚠️ Archivo vacío o ilegible."); exit()

mensajes = [
    {"role": "system", "content": "Responde solo según el documento cargado."},
    {"role": "user", "content": contenido[:4000]}
]

print("🤖 Listo. Preguntame sobre el PDF (escribe 'salir' para terminar).")

while True:
    pregunta = input("\nTú: ")
    if pregunta.lower() in ["salir", "exit"]: break
    mensajes.append({"role": "user", "content": pregunta})
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4.0-mini",
            messages=mensajes,
            temperature=0.5,
            max_tokens=600
        )
        texto = respuesta.choices[0].message.content
        print("\nBot:", texto)
        mensajes.append({"role": "assistant", "content": texto})
    except Exception as e:
        print("❌ Error API:", e)
