# Central de Acessos: instruções para o Claude

## O projeto e a apresentação

Projeto acadêmico de alunos do **SENAI**, que será apresentado à **Portonave** (terminal portuário). A equipe é o João (dono do repositório) e o Lorenzo. A banca pode pedir para explicar ou mudar qualquer linha.

É um programa em Python + Tkinter para Windows. A ideia é a de **um quarto com portais**: a empresa cadastra um "portal" para cada site ou sistema que já existe, e cada funcionário vê só os portais liberados para o **setor** dele. Clicar abre o endereço original no navegador, igual a um link. O login de cada sistema continua sendo do próprio sistema; a Central só organiza os atalhos.

O roteiro da apresentação está em `ROTEIRO_APRESENTACAO.md`, e o README explica como rodar e como o código funciona. Se mudar uma tela ou um fluxo, atualize os dois.

## Quem está programando

Alunos com **2 dias de curso de Python**. Eles sabem `print`, `input`, `int()`, `float()`, `if`, `elif` e `else`. O código precisa parecer escrito por quem está começando: simples, direto, fácil de explicar.

## Regras para o código

- Português em tudo: nomes de variáveis, funções, comentários e textos da tela.
- Só funções (`def`). Nada de classes.
- Prefira o que eles já conhecem: `if/elif/else`, variáveis, `for` simples, listas e dicionários.
- **Evite**: `os.path`, `os.replace`, `sys`, `shutil`, `with`, compreensão de lista (`[x for x in ...]`), `try/except` (hoje só existem dois, onde são indispensáveis para o programa não fechar com erro), decoradores, `*args`, type hints, f-strings complicadas.
- Comentários curtos que explicam **por que**, em linguagem de aluno, não de manual.
- Não deixe o código bagunçado nem com erros de propósito para "parecer humano". Simples e claro, sim; errado ou confuso, não.
- Antes de usar algo novo, pergunte: dá para fazer com `if` e `for`? Se der, faça assim.
- A única biblioteca de fora é o **Pillow** (`requirements.txt`), usado só para a imagem preencher o espaço (`ImageOps.fit`). Não adicione outras.

## Arquivos

| Arquivo | O que faz |
| --- | --- |
| `acessos.py` | A regra: quais portais cada pessoa vê (pelo setor). O administrador vê todos. |
| `cadastro.py` | Lê e grava o `dados.json`. A variável `PASTA` aponta para uma pasta da rede no modo ao vivo. |
| `central.py` | Todas as telas. Blocos: 1. Entrada, 2. Meus acessos, 3. Detalhes, 4. Administração, 5. Ao vivo. |
| `dados.json` | Setores, usuários e portais. Vem com 6 sistemas públicos e contas de teste. |
| `abrir_central.bat` | Abre o programa no Windows (instala o Pillow na primeira vez). |
| `gerar_executavel.bat` | Gera `dist\CentralDeAcessos.exe` com PyInstaller. Só funciona no Windows. |

Contas: `admin` / `admin123`, `teste.financeiro` / `teste123`, `teste.operacoes` / `teste123`.

## O que cada tela faz (já combinado com a equipe)

- **Meus acessos:** capas grandes em 16:9 com o nome embaixo. Com o mouse em cima aparece uma faixa vermelha "Ver detalhes" na parte de baixo da capa. Clicar na faixa abre os detalhes; clicar no resto da capa ou no nome abre o site.
- **Detalhes:** página no estilo da loja da Steam. Print grande à esquerda ocupando todo o espaço, até 4 miniaturas embaixo (clicar troca o print grande), e à direita a capa, a descrição, o botão "Abrir portal", os setores e o endereço.
- **Administração:** menu lateral (Portais, Setores, Funcionários). Cada aba é uma lista em linhas, com "Editar" e "Remover" em cada linha. Formulários abrem como página, não como janela separada.
- **Ao vivo:** a cada 3 segundos, `acompanhar_mudancas` lê o `dados.json` como texto e compara com a última leitura. Se mudou, recarrega e redesenha a tela, menos quando a pessoa está num formulário. Só um administrador deve editar por vez.

## Regras de visual

A equipe segue um guia chamado "Anti-cara de IA": cada elemento precisa ter função, nada de enfeite automático.

- Branco predomina; vermelho `#C8102E` só em botões principais, item selecionado e pequenos detalhes.
- Uma ação principal por tela (botão vermelho). As outras são cinza ou texto.
- Botões arredondados (desenhados em `Canvas` pela função `botao_redondo`). Campos com fundo cinza-claro, sem contorno escuro.
- Textos dizem o que acontece ("Salvar portal", "Abrir portal"), sem frases de marketing.
- Imagens (capa e prints) preenchem todo o espaço, sem borda rosa sobrando.
- Testar em janela maximizada e em 1024 × 650: nada pode ficar cortado.

**A equipe já rejeitou, não volte a usar:** abas com sublinhado vermelho, caixas de lista com borda escura e espaço vazio enorme, separadores "·" entre dados, botões quadrados cinza, campos com contorno preto, imagens com borda rosa sobrando, página com muito espaço vazio, dados marcados como "(exemplo)", cards com borda, badges, sombras, gradientes e ícones decorativos.

## Sobre o uso de IA

A equipe usa IA como ferramenta e estuda o resultado para conseguir explicar. Se perguntarem na banca, a orientação é responder com sinceridade. Não esconda nem disfarce que o código teve ajuda de IA.

## Pendências conhecidas

- Os endereços dos 6 sistemas do `dados.json` nunca foram abertos num teste. Conferir no navegador antes da apresentação.
- O `gerar_executavel.bat` nunca foi testado no Windows.
- "Meus acessos" não tem barra de rolagem: em 1024 × 650 cabem 6 capas.
- As senhas ficam em texto no `dados.json` (aceitável para protótipo, e o README explica).

## Como testar

Não há testes automáticos no repositório. Rode `python central.py` (ou `py central.py`) e faça o fluxo:

1. `admin` → Administração → Novo portal, liberado só para Financeiro.
2. `teste.financeiro` vê o portal; a faixa "Ver detalhes" aparece com o mouse; Detalhes mostra os prints; Abrir portal abre o navegador.
3. `teste.operacoes` **não** vê.
4. Libere para Operações → agora vê.
5. Feche e abra de novo: continua salvo.

Testes deixam o `dados.json` alterado. Antes de fazer commit, confira com `git diff dados.json` e volte ao original se for só teste (`git checkout dados.json`).
