# Central de Acessos

Um programa para Windows, feito em Python com Tkinter, que reúne num só lugar os atalhos para os sistemas da empresa.

Pense num quarto com portais. A empresa coloca um portal no quarto, e ele leva ao site ou sistema que já existe no endereço cadastrado. Cada funcionário vê só os portais liberados para o seu setor.

Ao clicar num portal, a Central abre o endereço no navegador, igual a clicar num link. O login e as permissões continuam sendo do sistema de destino. A Central só decide **quais atalhos cada setor enxerga**.

![Tela Meus acessos](capturas/meus-acessos-maximizada.png)

---

## Como abrir no Windows

1. Instale o Python em <https://www.python.org/downloads/>. Na instalação, deixe marcada a opção **"tcl/tk and IDLE"** (ela já vem marcada).
2. Baixe esta pasta inteira.
3. Dê dois cliques em **`abrir_central.bat`**.

Também dá para abrir pelo terminal, dentro da pasta:

```bash
py central.py
```

A janela abre maximizada, na tela de entrada.

### Contas de exemplo (só para o ensaio)

| Usuário | Senha | Quem é |
|---|---|---|
| `admin` | `admin123` | Administrador: vê todos os portais e a área de Administração |
| `ana` | `ana123` | Funcionária do Financeiro |
| `bruno` | `bruno123` | Funcionário de Operações |

Os portais que vêm prontos terminam com "(exemplo)" e apontam para `example.com`, um endereço reservado para testes. A empresa troca tudo isso pela tela de Administração.

---

## Por qual arquivo começar a estudar

São só três arquivos de código. Leiam nesta ordem:

| Ordem | Arquivo | O que tem | Tamanho |
|---|---|---|---|
| 1 | `acessos.py` | A **regra**: quais portais cada pessoa vê | 14 linhas |
| 2 | `cadastro.py` | **Salvar e carregar** os dados no arquivo `dados.json` | 54 linhas |
| 3 | `central.py` | **As telas**: entrada, Meus acessos, Detalhes e Administração | o maior |

O `central.py` é dividido em blocos com títulos (`1. ENTRADA`, `2. MEUS ACESSOS`, `3. ADMINISTRAÇÃO`). Dá para estudar um bloco por vez.

---

## O caminho de um portal (do cadastro ao navegador)

Este é o ponto principal para explicar na apresentação.

**1. O administrador cadastra.** Na tela de Administração ele clica em **Novo portal** e preenche nome, endereço, descrição, imagem e setores. Quem cuida disso é a função `janela_portal` em `central.py`.

**2. O programa confere e salva.** Ao clicar em **Salvar portal**, a função `salvar_portal`:
- confere com `if` se o nome foi preenchido, se o endereço começa com `http://` ou `https://` e se algum setor foi marcado;
- monta o portal como um dicionário, por exemplo:
  ```python
  {"nome": "Portal de Notas", "endereco": "https://...", "descricao": "...",
   "imagem": "", "setores": ["Financeiro"]}
  ```
- coloca o dicionário na lista `dados["portais"]` e chama `cadastro.salvar(dados)`, que grava tudo em **`dados.json`**.

Como fica gravado no arquivo, o cadastro continua lá quando o programa fecha e abre de novo.

**3. A regra filtra por setor.** Quando a Ana (Financeiro) entra, a tela pede ao `acessos.py` os portais dela:

```python
elif usuario["setor"] in portal["setores"]:
    liberados.append(portal)
```

Se `"Financeiro"` está na lista de setores do portal, ele aparece para ela. Se não está, fica de fora. O Bruno (Operações) não vê o Portal de Notas até o administrador marcar "Operações" também.

**4. O navegador abre.** Clicar no nome ou na imagem chama `abrir_portal`, que faz só isto:

```python
webbrowser.open(portal["endereco"])
```

É o mesmo que clicar num link: abre o navegador padrão no endereço original.

---

## O que é novo além de if, elif, else, print e input

O Tkinter obriga a usar quatro coisas que talvez vocês ainda não tenham visto. Elas aparecem o tempo todo no código:

| O que é | Exemplo no projeto | Em uma frase |
|---|---|---|
| **`def` (função)** | `def abrir_portal(portal):` | Um bloco de código com nome, que roda quando é chamado. Cada tela é uma função. |
| **Lista `[ ]`** | `["Financeiro", "Operações"]` | Vários valores guardados em ordem. |
| **Dicionário `{ }`** | `portal["nome"]` | Valores guardados com um nome (a "chave"). |
| **`for`** | `for portal in portais:` | Repete o bloco para cada item da lista. |

E uma quinta, que aparece nos botões:

- **`lambda`**: `command=lambda: abrir_portal(portal)` quer dizer "quando clicar, rode `abrir_portal(portal)`". Sem o `lambda`, a função rodaria na hora em que o botão é criado, e não no clique.

---

## Onde ficam os dados

- **`dados.json`**: setores, funcionários e portais. É criado na primeira vez que o programa abre, já com os exemplos. Para voltar ao começo, feche o programa e apague este arquivo.
- **`imagens/`**: o ícone padrão (`portal_padrao.png`). As imagens dos portais precisam ser **PNG ou GIF**, que é o que o Tkinter abre sem instalar nada.

## Limites desta versão (falem disso se perguntarem)

- **As senhas ficam escritas no `dados.json`.** Quem abrir o arquivo consegue ler. Para um protótipo de sala de aula serve. Num uso real, as senhas seriam guardadas como hash, ou o login viria do sistema da empresa.
- **A Central esconde atalhos, mas não protege os sistemas.** Quem souber o endereço consegue digitar direto no navegador. Por isso o login de cada sistema continua valendo: é ele que protege de verdade.
- **Não tem barra de rolagem em "Meus acessos".** Numa tela 1024 × 650 cabem cerca de 9 portais (3 por linha). Acima disso, seria preciso adicionar rolagem.
- **O vermelho (`#C8102E`) é provisório**, inspirado na Portonave. Se vocês receberem o manual da marca, troquem o valor de `VERMELHO` no começo do `central.py`.

---

## Testes feitos antes da entrega

Rodamos o programa de verdade, com telas e cliques, e conferimos cada passo:

| # | Teste | Resultado |
|---|---|---|
| 1 | Admin cadastra o "Portal de Notas (exemplo)" liberado só para Financeiro | ✅ salvo no `dados.json` só com Financeiro |
| 2 | Ana (Financeiro) entra e vê o portal | ✅ |
| 2 | "Detalhes" mostra a descrição; "Abrir portal" abre o endereço | ✅ |
| 2 | Clicar no nome e clicar na imagem abrem `https://example.com/notas` | ✅ testado com cliques reais do mouse |
| 3 | Bruno (Operações) entra e **não** vê o portal | ✅ |
| 4 | Admin edita o portal, marca Operações; Bruno passa a ver | ✅ |
| 5 | Fecha e reabre o programa: portal e permissões continuam | ✅ |
| extra | Senha errada mostra "Usuário ou senha incorretos." | ✅ |
| extra | Endereço sem `http://` é recusado com aviso | ✅ |
| extra | Funcionário não vê o menu Administração | ✅ |
| extra | Telas conferidas maximizada (1920 × 1080) e em 1024 × 650 | ✅ |

As capturas estão na pasta `capturas/`. Elas foram tiradas no Linux, então a fonte é um pouco diferente da Segoe UI que aparece no Windows.

---

Roteiro da apresentação: [`ROTEIRO_APRESENTACAO.md`](ROTEIRO_APRESENTACAO.md)
