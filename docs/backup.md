# Backup da BigSolutions

## O que faz parte do backup
| Pasta | Conteúdo |
|---|---|
| `website/` | Site público (`index.html`) e back office (`escritorio.html`) |
| `agentes/` | Equipa de agentes em Python e memória |
| `docs/` | Plano de negócio, redes sociais, Super Memória, este guia |

Os **dados do back office** (clientes, projetos, propostas, faturação, biblioteca) ficam guardados na tua conta claude.ai, não nestes ficheiros. Para os copiar: back office → Definições → **Exportar memória** (clientes e reuniões). A exportação completa de todos os módulos chega com a versão com servidor.

## Backup para um disco externo
**Opção 1, a mais simples:** no GitHub, abre o repositório → botão verde **Code** → **Download ZIP** → copia o ZIP para o disco.

**Opção 2, com Git (fica sempre atualizado):**
```bash
# a primeira vez, com o disco ligado
cd /Volumes/NOME_DO_DISCO          # Mac  (no Windows: E:\)
git clone https://github.com/Bigoutlet/bigsolutions.git

# das vezes seguintes
cd /Volumes/NOME_DO_DISCO/bigsolutions
git pull
```

Faz o backup pelo menos uma vez por semana e guarda o disco num sítio diferente do computador.
