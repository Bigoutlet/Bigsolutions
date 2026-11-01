# BigSolutions

Agência digital composta por agentes de IA que trabalham como um só.

```
bigsolutions/
├── website/
│   ├── index.html          ← site completo, pronto a publicar (Vercel/Netlify/Cloudflare Pages)
│   └── conteudo.html       ← versão de origem usada na pré-visualização
├── agentes/
│   ├── bigsolutions_agentes.py  ← Atlas + 7 especialistas (Claude API)
│   ├── memoria.py               ← camada de memória → ponto de ligação à Super Memória
│   ├── requirements.txt
│   └── .env.example
└── docs/
    ├── plano-de-negocio.md
    └── redes-sociais.md
```

## Pôr os agentes a trabalhar
```bash
cd agentes
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...        # chave em console.anthropic.com
python bigsolutions_agentes.py "Preciso de um website e Instagram para a minha padaria em Braga"
```
A entrega final fica em `agentes/entregas/`.

## Ligar à Super Memória
1. Preencher a classe `SuperMemoria` em `agentes/memoria.py` com a API da Super Memória.
2. `export BIGSOLUTIONS_MEMORIA=super SUPER_MEMORIA_URL=... SUPER_MEMORIA_CHAVE=...`

Os agentes usam só `lembrar()` e `recordar()`, por isso não é preciso mudar mais nada.
