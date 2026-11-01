# BigSolutions — Plano de Negócio

## 1. Conceito
Agência digital onde o trabalho é feito por uma equipa de agentes de IA especializados, coordenados por um agente diretor (Atlas) e **supervisionados por pelo menos um humano** que aprova cada entrega. Resultado: rapidez e preço de freelancer com a abrangência de uma agência completa.

**Proposta de valor:** "Uma equipa inteira de IA a trabalhar como uma só no seu projeto. Proposta em 24 h."

## 2. Serviços e preços de lançamento (sem IVA)
| Serviço | Preço | Agentes | Margem estimada* |
|---|---|---|---|
| Website (até 6 páginas) | desde 690 € | Forge, Pixel, Echo | 70–80 % |
| Loja online | desde 1 290 € | Forge, Pixel | 65–75 % |
| App / software à medida (MVP) | desde 3 500 € | Forge, Sentinel | 55–70 % |
| Gestão de redes sociais | 390 €/mês | Echo, Nova | 75 % |
| Anúncios Meta/Google | 290 €/mês + verba | Nova | 80 % |
| Pesquisa de sourcing | 290 € / pesquisa | Scout | 85 % |
| Negociação de sourcing | 5 % da encomenda | Scout, Ledger | — |
| Agentes de IA para empresas | desde 1 900 € + 99 €/mês | Forge | 60–75 % |

*Custos de API, alojamento e horas de revisão humana. Validar com os primeiros 10 projetos.

## 3. Clientes-alvo (por ordem de prioridade)
1. **PME locais** (restauração, comércio, clínicas, imobiliárias) sem site ou com site antigo.
2. **Pequenas marcas de e-commerce** que precisam de fornecedores e marketing.
3. **Startups** que precisam de um MVP rápido.
4. Mais tarde: Brasil e PALOP (mesma língua, mesma equipa de agentes).

## 4. Operação: como a equipa de IA trabalha
- **Atlas** recebe o briefing, consulta a memória do cliente e divide em tarefas.
- **Especialistas** (Nova, Pixel, Forge, Echo, Scout, Ledger) trabalham em paralelo.
- **Sentinel** revê; **o responsável humano aprova** antes de enviar ao cliente.
- **Memória**: tudo o que se aprende sobre o cliente fica guardado e será partilhado com a aplicação **Super Memória** (ver `agentes/memoria.py`).

Código de referência: `agentes/bigsolutions_agentes.py`.

## 5. Ferramentas recomendadas
| Necessidade | Ferramenta |
|---|---|
| Cérebro dos agentes | Claude API (Anthropic) |
| Alojamento de websites | Vercel, Netlify ou Cloudflare Pages |
| Formulários / CRM | HubSpot (gratuito) ou Notion |
| Faturação (PT) | InvoiceXpress, Moloni ou Vendus (certificados AT) |
| Pagamentos | Stripe, MB Way, Multibanco (via Eupago/Ifthenpay) |
| Agendamento de posts | Meta Business Suite, Buffer |
| Email profissional | Google Workspace ou Zoho |

## 6. Passos legais e administrativos (Portugal)
- [ ] Verificar e registar o nome: certificado de admissibilidade (RNPC) e marca no INPI.
- [ ] Registar domínios: `bigsolutions.pt` e `.ai`/`.com`. O nome "BigSolutions" é comum: confirmar a disponibilidade antes de investir na marca.
- [ ] Abrir atividade (trabalhador independente) ou constituir Lda. ("Empresa na Hora").
- [ ] CAE sugeridos: 62010 (programação), 73110 (publicidade), 70220 (consultoria).
- [ ] Política de privacidade e termos (RGPD), e aviso de que a agência usa IA (Regulamento Europeu de IA).
- [ ] Seguro de responsabilidade civil profissional.

## 7. Roteiro de 90 dias
| Semana | Objetivo |
|---|---|
| 1–2 | Registos legais, domínio, email, website no ar, perfis nas redes sociais |
| 3–4 | Portefólio: 3 projetos de demonstração (ex.: padaria, clínica, loja) |
| 5–8 | Primeiros 5 clientes (rede de contactos + prospeção por LinkedIn/email) |
| 9–12 | Testemunhos, casos de estudo, anúncios pagos, ligação à Super Memória |

**Meta ao fim de 90 dias:** 10 clientes, 4 000 €/mês de receita recorrente.

## 8. Riscos e mitigação
| Risco | Mitigação |
|---|---|
| Erros da IA chegam ao cliente | Revisão humana obrigatória (Sentinel + responsável) |
| Dados de clientes | RGPD, contratos de tratamento de dados, nada sensível em prompts |
| Dependência de um fornecedor de IA | Camada de agentes separada do resto do negócio |
| Preço demasiado baixo | Rever preços após os primeiros 10 projetos |
