# Roteiro da apresentação: Central de Acessos

Tempo total: cerca de **7 minutos**. Deixem o programa aberto antes de começar, na tela de entrada.

Antes do ensaio, apaguem o `dados.json` para começar só com os exemplos.

---

## 1. O problema (1 min)

> "Numa empresa grande, cada setor usa vários sistemas diferentes, cada um num endereço. O funcionário precisa lembrar onde fica cada um. A Central de Acessos junta esses atalhos num lugar só, e cada setor vê apenas o que é dele."

Usem a imagem do quarto com portais:

> "É como um quarto com portais. A empresa coloca um portal, e ele leva ao sistema que já existe. A Central não substitui o sistema: o login dele continua valendo."

## 2. O funcionário (1 min 30 s)

1. Entrem com **`ana` / `ana123`** (Financeiro).
2. Mostrem a tela **Meus acessos**: só imagem, nome e "Detalhes".
3. Cliquem em **Detalhes** num portal → aparece a descrição → **Abrir portal** abre o navegador.

> "Os links do ensaio são exemplos. A empresa cadastra os endereços dela."

## 3. O administrador (2 min)

1. **Sair** → entrem com **`admin` / `admin123`**.
2. **Administração → Novo portal**:
   - Nome: `Portal de Notas (exemplo)`
   - Endereço: `https://example.com/notas`
   - Descrição: `Consulta e emissão de notas fiscais.`
   - Marquem **só Financeiro** → **Salvar portal**.

## 4. A prova do filtro por setor (1 min 30 s)

1. **Sair** → `ana` / `ana123` → o Portal de Notas **aparece**.
2. **Sair** → `bruno` / `bruno123` (Operações) → o portal **não aparece**.
3. **Sair** → `admin` → **Editar** o portal → marquem **Operações** → **Salvar**.
4. **Sair** → `bruno` → agora **aparece**.
5. Fechem a janela e abram de novo → continua tudo salvo.

## 5. Como funciona por dentro (1 min)

Abram o `acessos.py` (14 linhas) e mostrem:

```python
elif usuario["setor"] in portal["setores"]:
    liberados.append(portal)
```

> "Essa é a regra inteira. Se o setor da pessoa está na lista de setores do portal, ele aparece."

Depois, uma frase sobre o resto:

> "O `cadastro.py` salva tudo no arquivo `dados.json`. Por isso nada se perde quando o programa fecha. E abrir o portal é uma linha: `webbrowser.open(endereco)`."

---

## Perguntas que podem aparecer

**"E se alguém digitar o endereço direto no navegador?"**
> "Consegue. A Central organiza os atalhos, mas quem protege o sistema é o login dele. Por isso o login continua no sistema de destino."

**"As senhas estão seguras?"**
> "Nesta versão de protótipo, não: elas ficam no arquivo `dados.json`. Numa versão real, o login viria do sistema da empresa."

**"Vocês usaram IA?"**
> Respondam com sinceridade. Por exemplo: "Usamos IA como ferramenta para montar o código, e depois estudamos cada parte para conseguir explicar e alterar."
