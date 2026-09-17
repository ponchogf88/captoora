"""
CAPTOORA STUDIO - AGENTE DE PROSPECCIÓN Y AUTOMATIZACIÓN WEB
Powered by browser-use & Playwright
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno si existe .env
load_dotenv()

async def run_agent(task_prompt: str):
    print("\n" + "="*60)
    print("🚀 INICIANDO AGENTE AUTÓNOMO DE CAPTOORA (browser-use)")
    print("="*60)
    print(f"🎯 Tarea asignada:\n{task_prompt}\n")

    # Verificar si existe alguna API Key configurada
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("⚠️ AVISO: No se detectó ninguna API Key en tu entorno (.env).")
        print("Para que el agente de browser-use piense y tome decisiones autónomas,")
        print("necesitas configurar una clave de IA en el archivo .env (por ejemplo GEMINI_API_KEY o OPENAI_API_KEY).")
        print("\nPuedes obtener una clave gratuita de Google Gemini en: https://aistudio.google.com/")
        print("="*60)
        return

    try:
        from browser_use import Agent
        from browser_use.browser.browser import Browser, BrowserConfig

        # Seleccionar modelo según la clave disponible
        llm = None
        if os.getenv("GEMINI_API_KEY"):
            from langchain_google_genai import ChatGoogleGenerativeAI
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
            print("✅ Conectado con Google Gemini 1.5 Flash")
        elif os.getenv("OPENAI_API_KEY"):
            from langchain_openai import ChatOpenAI
            llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
            print("✅ Conectado con OpenAI GPT-4o-mini")

        # Configuración del navegador (modo visible para que veas lo que hace el agente)
        browser = Browser(config=BrowserConfig(headless=False))

        agent = Agent(
            task=task_prompt,
            llm=llm,
            browser=browser
        )

        print("\n🌐 Abriendo navegador y ejecutando tarea paso a paso...")
        history = await agent.run(max_steps=20)
        print("\n" + "="*60)
        print("🎉 TAREA COMPLETADA CON ÉXITO")
        print("="*60)
        print(history)

    except Exception as e:
        print(f"\n❌ Ocurrió un detalle al ejecutar: {e}")
        print("Si te falta alguna dependencia de langchain, instálala con: pip install langchain-google-genai langchain-openai")

def main():
    print("""
============================================================
       CAPTOORA STUDIO - MENÚ DE AUTOMATIZACIÓN (browser-use)
============================================================
1. Monitorear tours y experiencias fotográficas en Airbnb Monterrey
2. Investigar spots y tendencias de fotografía urbana en Monterrey
3. Buscar restaurantes locales para ofrecer fotografía gastronómica
4. Escribir una tarea personalizada para el agente
5. Salir
============================================================
""")
    opcion = input("Selecciona una opción (1-5): ").strip()

    if opcion == "1":
        task = "Entra a airbnb.com, busca experiencias fotográficas o photo walks en Monterrey, Nuevo León, México, y anota los 3 tours con mejores reseñas y sus precios en USD."
    elif opcion == "2":
        task = "Entra a google.com y busca 'mejores lugares para fotos urbanas en Barrio Antiguo y Fundidora Monterrey', y resume los 5 spots más recomendados."
    elif opcion == "3":
        task = "Entra a Google Maps, busca 'restaurantes en San Pedro Garza Garcia Monterrey', revisa 3 restaurantes con muchas reseñas y extrae su nombre y página web o redes."
    elif opcion == "4":
        task = input("\nEscribe la tarea exacta que quieres que el agente haga en el navegador:\n> ").strip()
    else:
        print("Saliendo...")
        return

    asyncio.run(run_agent(task))

if __name__ == "__main__":
    main()
