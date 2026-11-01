# Ligação à Super Memória

A BigSolutions guarda o que sabe sobre cada cliente (factos, preferências, decisões, entregas aprovadas) e partilha essa memória num formato comum: **`bigsolutions-memoria/1`**.

## Onde o formato é usado
| Sítio | Como |
|---|---|
| Back office (Definições → Memória) | Botões **Exportar memória** e **Importar ficheiro** |
| Agentes em Python (`agentes/memoria.py`) | `MemoriaLocal.exportar()` e `MemoriaLocal.importar(dados)` |
| Super Memória | Deve ler e escrever este mesmo formato |

## Formato
```json
{
  "formato": "bigsolutions-memoria/1",
  "exportadoEm": "2026-11-01T10:00:00Z",
  "agencia": { "nome": "BigSolutions" },
  "entidades": [
    {
      "tipo": "cliente",
      "id": "abc123",
      "nome": "Padaria Trigo Dourado",
      "empresa": "Trigo Dourado Lda",
      "contacto": "ana@trigo.pt",
      "setor": "Restauração",
      "estado": "ativo",
      "factos": [
        { "texto": "Quer encomendas para recolha na loja", "origem": "pedido", "data": "2026-11-01T09:12:00Z" }
      ]
    }
  ],
  "reunioes": [
    { "tema": "Plano de lançamento", "resumo": "…", "decisoes": ["…"], "data": "2026-11-01T11:00:00Z" }
  ]
}
```

Regras da importação: os clientes são encontrados pelo `id` ou pelo nome; factos com o mesmo texto não são duplicados; cada cliente guarda no máximo 60 factos (os mais recentes).

## Ligação direta (próximo passo)
O back office corre dentro do claude.ai e não pode chamar outras aplicações. Na versão com servidor:
1. A Super Memória expõe `GET /memorias?cliente=` e `POST /memorias` (ou equivalente).
2. Preenche-se a classe `SuperMemoria` em `agentes/memoria.py` com essas chamadas.
3. O back office sincroniza automaticamente sempre que um facto é guardado.
