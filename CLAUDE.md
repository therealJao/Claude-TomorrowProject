# Central de Acessos: instruções para o Claude

Projeto de alunos do SENAI, apresentado à Portonave. É um programa em Python + Tkinter para Windows: cada funcionário entra com usuário e senha e vê as capas dos sistemas (sites) liberados para o setor dele. Clicar abre o endereço no navegador.

## Quem está programando

Alunos com **2 dias de curso de Python**. Eles sabem `print`, `input`, `int()`, `float()`, `if`, `elif` e `else`. Eles precisam conseguir **ler, explicar e mudar** cada linha na frente da banca.

## Regras para o código

- Português em tudo: nomes de variáveis, funções, comentários e textos da tela.
- Só funções (`def`). Nada de classes.
- Prefira o que eles já conhecem: `if/elif/else`, variáveis, `for` simples, listas e dicionários.
- **Evite**: `os.path`, `os.replace`, `sys`, `shutil`, `with`, compreensão de lista (`[x for x in ...]`), `try/except` (só onde for indispensável para o programa não fechar com erro), decoradores, `*args`, type hints, f-strings complicadas.
- Comentários curtos que explicam **por que**, em linguagem de aluno, não de manual.
- Não deixe o código bagunçado de propósito para "parecer humano". Simples e claro, sim; errado ou confuso, não.
- Antes de usar algo novo, pergunte: dá para fazer com `if` e `for`? Se der, faça assim.

## Arquivos

| Arquivo | O que faz |
| --- | --- |
| `acessos.py` | A regra: quais portais cada pessoa vê (pelo setor). |
| `cadastro.py` | Lê e grava o `dados.json`. A variável `PASTA` aponta para uma pasta da rede no modo ao vivo. |
| `central.py` | Todas as telas. Blocos: 1. Entrada, 2. Meus acessos, 3. Detalhes, 4. Administração, 5. Ao vivo. |
| `dados.json` | Setores, usuários e portais. Vem com 6 sistemas públicos e contas de teste. |

A única biblioteca de fora é o **Pillow** (`requirements.txt`), usado só para a imagem preencher o espaço (`ImageOps.fit`). Não adicione outras.

## Regras de visual (do guia "Anti-cara de IA" que eles seguem)

- Branco predomina; vermelho `#C8102E` só em botões principais, item selecionado e pequenos detalhes.
- Sem cards com borda, badges, sombras, gradientes, ícones decorativos, separadores "·" ou caixas vazias enormes.
- Uma ação principal por tela (botão vermelho). As outras são cinza ou texto.
- Botões arredondados (desenhados em `Canvas` pela função `botao_redondo`). Campos com fundo cinza-claro, sem contorno escuro.
- Textos dizem o que acontece ("Salvar portal", "Abrir portal"), sem frases de marketing.
- Imagens (capa e prints) preenchem todo o espaço, sem borda rosa sobrando.
- Testar em janela maximizada e em 1024 × 650: nada pode ficar cortado.

## Como funciona o "ao vivo"

A cada 3 segundos, `acompanhar_mudancas` lê o `dados.json` como texto e compara com a última leitura. Se mudou, recarrega e redesenha a tela, menos quando a pessoa está num formulário. Só um administrador deve editar por vez.

## Como testar

Não há testes automáticos no repositório. Para conferir, rode `py central.py` e faça o fluxo:

1. `admin` / `admin123` → Administração → Novo portal, liberado só para Financeiro.
2. `teste.financeiro` / `teste123` vê o portal; Detalhes mostra os prints; Abrir portal abre o navegador.
3. `teste.operacoes` / `teste123` **não** vê.
4. Libere para Operações → agora vê.
5. Feche e abra de novo: continua salvo.

Testes deixam o `dados.json` alterado. Antes de fazer commit, confira com `git diff dados.json` e volte ao original se for só teste (`git checkout dados.json`).
