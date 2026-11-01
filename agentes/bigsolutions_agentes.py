"""
BigSolutions — Equipa de agentes de IA que trabalham como um só.

Atlas (o Diretor) recebe o pedido do cliente, divide-o em tarefas e delega
cada uma no especialista certo. Os especialistas trabalham em paralelo,
o Sentinel revê, e o Atlas entrega um documento final ao cliente.

Uso:
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=...
    python bigsolutions_agentes.py "Preciso de um website para a minha padaria em Braga"
"""

from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

import anthropic

from memoria import obter_memoria

MODELO = "claude-opus-5-5"
# Em caso de recusa por política de segurança, a API volta a correr o pedido
# noutro modelo automaticamente.
BETAS = ["server-side-fallback-2026-07-01"]
FALLBACKS = "default"

client = anthropic.Anthropic()
memoria = obter_memoria()

BASE = (
    "Trabalhas na BigSolutions, uma agência digital portuguesa composta por agentes de IA "
    "supervisionados por humanos. Escreve em português de Portugal, de forma clara e concreta. "
    "Nunca inventes factos sobre o cliente: quando faltar informação, assume o mínimo, "
    "diz o que assumiste e lista as perguntas a fazer ao cliente."
)

WEB_SEARCH = {"type": "web_search_20260209", "name": "web_search", "max_uses": 6}

# --- A equipa -----------------------------------------------------------------
ESPECIALISTAS: dict[str, dict] = {
    "nova": {
        "cargo": "Estratégia & Marketing",
        "system": "És a Nova, estratega de marketing. Entregas: público-alvo, posicionamento, "
        "proposta de valor, canais prioritários, plano de campanha com orçamento e KPIs mensuráveis.",
        "tools": [WEB_SEARCH],
    },
    "pixel": {
        "cargo": "Design & Marca",
        "system": "És o Pixel, diretor de arte. Entregas: conceito visual, paleta com códigos HEX, "
        "tipografia (Google Fonts), estrutura de páginas/ecrãs e orientações para imagens.",
        "tools": [],
    },
    "forge": {
        "cargo": "Desenvolvimento (websites, apps, software)",
        "system": "És o Forge, engenheiro de software. Entregas: arquitetura técnica, stack recomendada "
        "e porquê, lista de funcionalidades (MVP vs. fase 2), estimativa em horas e código inicial quando útil.",
        "tools": [],
    },
    "echo": {
        "cargo": "Conteúdo & Redes Sociais",
        "system": "És o Echo, gestor de conteúdo. Entregas: textos (copy) prontos a publicar, "
        "calendário editorial, ideias de posts/reels por rede social, hashtags e tom de voz.",
        "tools": [],
    },
    "scout": {
        "cargo": "Sourcing & Fornecedores",
        "system": "És o Scout, especialista em sourcing. Pesquisas fornecedores, fabricantes e "
        "prestadores; comparas preço, prazo, MOQ, certificações e risco. Indica sempre as fontes "
        "e marca como 'a verificar' tudo o que não confirmaste.",
        "tools": [WEB_SEARCH],
    },
    "ledger": {
        "cargo": "Propostas & Orçamentos",
        "system": "És o Ledger, responsável comercial. Transformas o trabalho da equipa numa proposta "
        "com fases, prazos, preço em euros (com e sem IVA a 23%), condições de pagamento e próximos passos.",
        "tools": [],
    },
    "sentinel": {
        "cargo": "Qualidade & Revisão",
        "system": "És o Sentinel, revisor de qualidade. Verificas coerência entre as partes, erros, "
        "promessas irrealistas, riscos legais (RGPD, direitos de imagem) e o que falta. Responde com "
        "uma lista de correções concretas e uma nota final de 1 a 10.",
        "tools": [],
    },
}

ATLAS_SYSTEM = BASE + (
    "\n\nÉs o Atlas, Diretor da BigSolutions. Não executas o trabalho técnico: planeias, delegas e "
    "consolidas. Para cada pedido:\n"
    "1. Divide o pedido em tarefas e delega-as com a ferramenta `delegar` (podes chamar vários "
    "especialistas ao mesmo tempo; dá a cada um contexto completo, porque não veem a conversa).\n"
    "2. Quando tiveres os resultados, envia o rascunho consolidado ao `sentinel` para revisão.\n"
    "3. Aplica as correções e entrega ao cliente um documento final em Markdown com: resumo, "
    "entregáveis de cada área, proposta comercial e perguntas em aberto.\n"
    "Antes de planear, usa `recordar` para ver o que já sabemos do cliente. No fim, usa `lembrar` "
    "para guardar factos duradouros (preferências, decisões, orçamento, contactos de fornecedores).\n"
    "Equipa disponível:\n"
    + "\n".join(f"- {nome}: {e['cargo']}" for nome, e in ESPECIALISTAS.items())
)

DELEGAR_TOOL = {
    "name": "delegar",
    "description": "Atribui uma tarefa a um especialista da BigSolutions e devolve o trabalho dele.",
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "agente": {"type": "string", "enum": list(ESPECIALISTAS)},
            "tarefa": {
                "type": "string",
                "description": "Instruções completas e autónomas, incluindo o contexto do cliente.",
            },
        },
        "required": ["agente", "tarefa"],
        "additionalProperties": False,
    },
}


MEMORIA_TOOLS = [
    {
        "name": "recordar",
        "description": "Consulta a memória da agência sobre um cliente (projetos, decisões, preferências anteriores).",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {"cliente": {"type": "string"}, "consulta": {"type": "string"}},
            "required": ["cliente", "consulta"],
            "additionalProperties": False,
        },
    },
    {
        "name": "lembrar",
        "description": "Guarda um facto duradouro sobre um cliente na memória da agência.",
        "strict": True,
        "input_schema": {
            "type": "object",
            "properties": {"cliente": {"type": "string"}, "facto": {"type": "string"}},
            "required": ["cliente", "facto"],
            "additionalProperties": False,
        },
    },
]


def _texto(resposta) -> str:
    return "\n".join(b.text for b in resposta.content if b.type == "text").strip()


def executar_especialista(agente: str, tarefa: str) -> str:
    """Um especialista trabalha numa tarefa até a terminar."""
    esp = ESPECIALISTAS[agente]
    print(f"  → {agente} ({esp['cargo']}) a trabalhar…", flush=True)
    mensagens = [{"role": "user", "content": tarefa}]
    while True:
        r = client.beta.messages.create(
            model=MODELO,
            max_tokens=16000,
            system=BASE + "\n\n" + esp["system"],
            tools=esp["tools"],
            output_config={"effort": "medium"},
            betas=BETAS,
            fallbacks=FALLBACKS,
            messages=mensagens,
        )
        if r.stop_reason == "pause_turn":  # pesquisa web longa: continuar
            mensagens.append({"role": "assistant", "content": r.content})
            continue
        if r.stop_reason == "refusal":
            return f"[{agente} não pôde concluir esta tarefa por motivos de política de segurança.]"
        print(f"  ✓ {agente} terminou", flush=True)
        return _texto(r)


def atlas(pedido: str) -> str:
    """O Diretor coordena a equipa até ao documento final."""
    print("Atlas a planear o projeto…", flush=True)
    mensagens = [{"role": "user", "content": pedido}]
    while True:
        r = client.beta.messages.create(
            model=MODELO,
            max_tokens=32000,
            system=ATLAS_SYSTEM,
            tools=[DELEGAR_TOOL, *MEMORIA_TOOLS],
            output_config={"effort": "high"},
            betas=BETAS,
            fallbacks=FALLBACKS,
            messages=mensagens,
        )
        mensagens.append({"role": "assistant", "content": r.content})

        if r.stop_reason == "refusal":
            return "O pedido não pôde ser processado por motivos de política de segurança."
        if r.stop_reason != "tool_use":
            return _texto(r)

        chamadas = [b for b in r.content if b.type == "tool_use"]

        def correr(bloco):
            try:
                dados = bloco.input if isinstance(bloco.input, dict) else json.loads(bloco.input)
                if bloco.name == "recordar":
                    factos = memoria.recordar(dados["cliente"], dados["consulta"])
                    return {"type": "tool_result", "tool_use_id": bloco.id,
                            "content": "\n".join(factos) or "Sem registos para este cliente."}
                if bloco.name == "lembrar":
                    memoria.lembrar(dados["cliente"], dados["facto"], origem="atlas")
                    return {"type": "tool_result", "tool_use_id": bloco.id, "content": "Guardado."}
                return {"type": "tool_result", "tool_use_id": bloco.id,
                        "content": executar_especialista(dados["agente"], dados["tarefa"])}
            except Exception as erro:  # o Atlas decide como reagir a uma falha
                return {"type": "tool_result", "tool_use_id": bloco.id,
                        "content": f"Erro: {erro}", "is_error": True}

        # Especialistas trabalham em paralelo; todos os resultados voltam numa só mensagem.
        with ThreadPoolExecutor(max_workers=len(chamadas)) as pool:
            resultados = list(pool.map(correr, chamadas))
        mensagens.append({"role": "user", "content": resultados})


def main() -> None:
    pedido = " ".join(sys.argv[1:]) or input("Pedido do cliente: ")
    entrega = atlas(pedido)
    pasta = Path(__file__).parent / "entregas"
    pasta.mkdir(exist_ok=True)
    ficheiro = pasta / f"entrega-{datetime.now():%Y%m%d-%H%M%S}.md"
    ficheiro.write_text(entrega, encoding="utf-8")
    print(f"\nEntrega guardada em {ficheiro}\n")
    print(entrega)


if __name__ == "__main__":
    main()
