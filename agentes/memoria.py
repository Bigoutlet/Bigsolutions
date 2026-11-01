"""
Camada de memória da BigSolutions — ponto de ligação à "Super Memória".

Os agentes só conhecem a interface `Memoria` (lembrar / recordar).
Hoje usa-se `MemoriaLocal` (ficheiro JSON). Para ligar a Super Memória,
implementa `SuperMemoria` (abaixo) com a API dessa aplicação e define
BIGSOLUTIONS_MEMORIA=super. Nada mais no código dos agentes muda.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Protocol


class Memoria(Protocol):
    def lembrar(self, cliente: str, facto: str, origem: str) -> None: ...
    def recordar(self, cliente: str, consulta: str = "") -> list[str]: ...


class MemoriaLocal:
    """Memória simples em JSON: um histórico de factos por cliente."""

    def __init__(self, ficheiro: Path | None = None):
        self.ficheiro = ficheiro or Path(__file__).parent / "memoria.json"
        try:
            self.dados = json.loads(self.ficheiro.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            self.dados = {}

    def lembrar(self, cliente: str, facto: str, origem: str) -> None:
        self.dados.setdefault(cliente.lower(), []).append(
            {"facto": facto, "origem": origem, "data": datetime.now().isoformat(timespec="seconds")}
        )
        self.ficheiro.write_text(json.dumps(self.dados, ensure_ascii=False, indent=2), encoding="utf-8")

    def recordar(self, cliente: str, consulta: str = "") -> list[str]:
        factos = self.dados.get(cliente.lower(), [])
        termos = consulta.lower().split()
        return [
            f"{f['data']} ({f['origem']}): {f['facto']}"
            for f in factos
            if not termos or any(t in f["facto"].lower() for t in termos)
        ]


    # --- formato partilhado com o back office e a Super Memória ---
    FORMATO = "bigsolutions-memoria/1"

    def exportar(self) -> dict:
        """Devolve a memória no formato bigsolutions-memoria/1."""
        return {
            "formato": self.FORMATO,
            "exportadoEm": datetime.now().isoformat(timespec="seconds"),
            "agencia": {"nome": "BigSolutions"},
            "entidades": [
                {"tipo": "cliente", "id": nome, "nome": nome,
                 "factos": [{"texto": f["facto"], "origem": f["origem"], "data": f["data"]} for f in factos]}
                for nome, factos in self.dados.items()
            ],
            "reunioes": [],
        }

    def importar(self, dados: dict) -> int:
        """Junta factos de um ficheiro bigsolutions-memoria/1, sem duplicar. Devolve quantos entraram."""
        if dados.get("formato") != self.FORMATO:
            raise ValueError("Ficheiro fora do formato bigsolutions-memoria/1")
        novos = 0
        for e in dados.get("entidades", []):
            if e.get("tipo") != "cliente" or not e.get("nome"):
                continue
            atuais = self.dados.setdefault(e["nome"].lower(), [])
            vistos = {f["facto"] for f in atuais}
            for f in e.get("factos", []):
                if f.get("texto") and f["texto"] not in vistos:
                    atuais.append({"facto": f["texto"], "origem": f.get("origem", "importado"),
                                   "data": f.get("data", datetime.now().isoformat(timespec="seconds"))})
                    vistos.add(f["texto"])
                    novos += 1
        self.ficheiro.write_text(json.dumps(self.dados, ensure_ascii=False, indent=2), encoding="utf-8")
        return novos

class SuperMemoria:
    """Adaptador para a aplicação Super Memória (por implementar).

    Preencher com as chamadas à API da Super Memória, por exemplo:
      lembrar  -> POST {SUPER_MEMORIA_URL}/memorias  {cliente, facto, origem}
      recordar -> GET  {SUPER_MEMORIA_URL}/memorias?cliente=...&q=...
    """

    def __init__(self):
        self.url = os.environ["SUPER_MEMORIA_URL"]
        self.chave = os.environ.get("SUPER_MEMORIA_CHAVE", "")

    def lembrar(self, cliente: str, facto: str, origem: str) -> None:
        raise NotImplementedError("Ligar à API da Super Memória")

    def recordar(self, cliente: str, consulta: str = "") -> list[str]:
        raise NotImplementedError("Ligar à API da Super Memória")


def obter_memoria() -> Memoria:
    if os.environ.get("BIGSOLUTIONS_MEMORIA") == "super":
        return SuperMemoria()
    return MemoriaLocal()
