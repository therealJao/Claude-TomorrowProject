# Roteiro da apresentação

Cerca de **7 minutos**. Antes de começar:

- Adicionem capa e prints em pelo menos 2 ou 3 sistemas, para a tela ficar com cara de pronta.
- Cliquem em cada portal uma vez para conferir que o endereço abre.
- Deixem o programa aberto na tela de entrada.

## 1. O problema (1 min)

> "Cada setor do terminal usa vários sistemas, e cada um fica num endereço diferente. A Central junta esses atalhos num lugar só, e cada setor vê só o que é dele."

> "Pensem num quarto com portais. Cada portal leva a um sistema que já existe. A Central não substitui o sistema: o login dele continua valendo."

## 2. O funcionário (2 min)

1. Entrem com `teste.operacoes` / `teste123`.
2. Passem o mouse numa capa: aparece **Ver detalhes**.
3. Cliquem na faixa: abre a página do sistema, com os prints. Cliquem nas miniaturas para trocar o print.
4. Cliquem em **Abrir portal**: abre o navegador.

## 3. O administrador (2 min)

1. **Sair** → `admin` / `admin123` → **Administração** → **Novo portal**.
2. Cadastrem um sistema ao vivo. Escolham a capa e um print, e marquem **só Financeiro**.
3. **Salvar portal**.

## 4. A prova do filtro (1 min 30 s)

1. **Sair** → `teste.financeiro` → o portal novo **aparece**.
2. **Sair** → `teste.operacoes` → **não aparece**.
3. **Sair** → `admin` → **Editar** → marquem **Operações** → **Salvar**.
4. **Sair** → `teste.operacoes` → agora **aparece**.
5. Fechem a janela e abram de novo: continua tudo lá.

## Extra: ao vivo em dois computadores (1 min, se der tempo)

Antes, coloquem o mesmo caminho de pasta da rede no `PASTA` do `cadastro.py` dos dois computadores (veja o README).

1. No computador A, deixem aberto `teste.operacoes`.
2. No computador B, o `admin` libera um portal para Operações e clica em **Salvar portal**.
3. Em até 3 segundos, o portal aparece sozinho no computador A.

> "Os dois programas leem o mesmo arquivo na rede. A cada 3 segundos cada um confere se o arquivo mudou."

## 5. Por dentro (30 s)

Mostrem o `acessos.py`:

```python
elif usuario["setor"] in portal["setores"]:
    liberados.append(portal)
```

> "Essa é a regra inteira: se o setor da pessoa está na lista do portal, ele aparece. Tudo fica salvo no arquivo dados.json."

## Perguntas que podem aparecer

**"E se alguém digitar o endereço direto?"**
> "Consegue abrir. Quem protege o sistema é o login dele. A Central organiza os caminhos."

**"As senhas estão seguras?"**
> "No protótipo elas ficam no arquivo de dados. Numa versão real, o login viria do sistema da empresa."

**"Vocês usaram IA?"**
> Respondam com sinceridade. Por exemplo: "Usamos como ferramenta, e depois estudamos cada parte para conseguir explicar e mudar o código."
