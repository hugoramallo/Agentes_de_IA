from datetime import datetime
from zoneinfo import ZoneInfo
from smolagents import ToolCallingAgent, tool, DuckDuckGoSearchTool
from smolagents.models import OpenAIServerModel  # requiere smolagents reciente

# HERRAMIENTAS PERSONALIZADAS
# El docstring es importante porque lo usa el framework para generar el esquema JSON
@tool
def respuesta_final(respuesta: str) -> str:
    """Devuelve la respuesta final del agente al usuario.

    Args:
        respuesta (str): Texto generado por el agente.

    Returns:
        str: Respuesta final formateada para el usuario.
    """
    return f"RESPUESTA FINAL: {respuesta}"

@tool
def obtener_hora_zona_horaria(zona_horaria: str) -> str:
    """Obtiene la hora local en una zona horaria dada.

    Args:
        zona_horaria (str): Identificador IANA de la zona horaria,
            por ejemplo 'Europe/Madrid' o 'America/New_York'.

    Returns:
        str: Hora local actual en formato 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now(ZoneInfo(zona_horaria)).strftime("%Y-%m-%d %H:%M:%S")

# HERRAMIENTAS DEL AGENTE

# Búsqueda en internet
duck_search = DuckDuckGoSearchTool()

# Cargo mi LLM Local GPT-OSS
llm = OpenAIServerModel(
    model_id="gpt-oss:20b",                   # El que uses en Ollama
    api_base="http://localhost:11434/v1",  # OpenAI-compatible de Ollama
    api_key="ollama",                      # dummy
    temperature=0,
    response_format={"type": "json_object"}  # fuerza JSON
)

agent = ToolCallingAgent(
    tools=[obtener_hora_zona_horaria, respuesta_final, duck_search],
    model=llm,
    max_steps=4, # Pasos en el razonamiento
)

# INSTRUCCIONES DEL AGENTE
instrucciones = (
    "Eres un agente que USA HERRAMIENTAS. "
    "Cuando necesites usar una herramienta, responde SOLO con un objeto JSON "
    'con las claves "tool_name" y "tool_args". Nada de texto adicional. '
    "Para resúmenes usa SOLO los snippets de búsqueda; NO abras URLs. "
    "Al final, formatea con 'respuesta_final'.\n\n"
)

prompt = instrucciones + ("Obtén la hora actual en 'Europe/Madrid' y en 'America/New_York' usando la tool. "
           "Calcula la diferencia en horas y finaliza llamando a 'respuesta_final' con un resumen conciso.")


prompt = instrucciones + ("Busca información en internet y haz un resumen sobre la vida de Alan Turing. Traduce al español y proporciona la fuente de la página donde has adquirido la información")

print(agent.run(prompt))