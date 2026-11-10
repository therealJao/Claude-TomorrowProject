# Central de Acessos

**Um catálogo de atalhos para os sites e sistemas que cada setor usa no trabalho.**

Projeto acadêmico independente, desenvolvido no SENAI para apresentação à Portonave. A proposta parte de um problema simples: quando cada ferramenta fica em um endereço diferente, encontrar o portal certo toma tempo. A Central reúne esses endereços numa tela e mostra a cada pessoa os atalhos liberados para o seu setor.

[Como executar](#como-executar-no-windows) · [Como funciona](#como-funciona) · [Entenda o código](#entenda-o-código) · [Roteiro da apresentação](ROTEIRO_APRESENTACAO.md)

![Tela Meus acessos da Central, com as capas dos portais](capturas/hub-admin-maximizada.png)

## Como funciona

A ideia é a de um quarto com portais. O administrador cadastra cada atalho com nome, endereço, descrição, capa, até 4 prints e os setores que podem vê-lo. Na tela **Meus acessos**, o funcionário encontra as capas dos portais do próprio setor.

- Clicar na capa ou no nome abre o endereço original no navegador padrão.
- Com o mouse em cima da capa, aparece a faixa **Ver detalhes**. Ela leva à página do sistema, com os prints, a descrição e o botão **Abrir portal**.

| Quem usa | O que pode fazer |
| --- | --- |
| **Funcionário** | Consultar seus atalhos, ver os detalhes e os prints, e abrir os destinos. |
| **Administrador** | Cadastrar, editar e remover portais, gerenciar setores e funcionários e escolher onde cada atalho aparece. |

O cadastro fica salvo no computador entre as execuções. Cada sistema de destino continua responsável pelo seu login e pelas suas permissões.

| Capa com o mouse em cima | Página de detalhes |
| --- | --- |
| ![Faixa Ver detalhes sobre a capa](capturas/hub-hover-1024.png) | ![Página de detalhes com print grande e miniaturas](capturas/detalhes-1024.png) |

## Como executar no Windows

1. Instale o [Python](https://www.python.org/downloads/) com o componente **Tcl/Tk and IDLE**.
2. Baixe o repositório como ZIP e extraia a pasta inteira.
3. Abra **`abrir_central.bat`**. A Central abre maximizada, na tela de entrada.

Se preferir o terminal, rode na pasta do projeto:

```powershell
py central.py
```

Na primeira execução, o programa cria o `dados.json` com os setores, as contas abaixo e seis sistemas públicos já cadastrados: Site da Portonave, Portal Único Siscomex, MarineTraffic, Tábuas de maré, Portal da NF-e e eSocial. Eles ainda não têm capa nem prints; isso se adiciona pela Administração.

<details>
<summary><strong>Contas para o ensaio</strong></summary>

| Usuário | Senha | Papel |
| --- | --- | --- |
| `admin` | `admin123` | Administração |
| `teste.financeiro` | `teste123` | Financeiro |
| `teste.operacoes` | `teste123` | Operações |

As contas de teste podem ser apagadas na aba **Funcionários** depois da apresentação. A senha do `admin` também deve ser trocada.

</details>

### Capas e prints

Use **PNG de 1280 × 720**. Nesse tamanho a imagem encaixa sem bordas na capa (256 × 144), no print grande (640 × 360, ou 1280 × 720 em tela grande) e nas miniaturas (128 × 72). No Windows, **Windows + Shift + S** recorta a tela, e o recorte pode ser salvo como PNG. O Tkinter não abre JPG sem bibliotecas extras.

As imagens escolhidas são copiadas para a pasta `imagens/`, então o portal não perde a capa se o arquivo original for apagado.

## Demonstração

1. Entre como administrador e cadastre um portal com capa e prints. Libere o atalho apenas para o **Financeiro**.
2. Entre com a conta do Financeiro. Passe o mouse na capa, abra **Ver detalhes**, troque os prints pelas miniaturas e clique em **Abrir portal**.
3. Entre com a conta de Operações e confira que o portal não aparece.
4. Volte à Administração, libere o mesmo portal para **Operações** e entre novamente nessa conta. Feche e reabra a Central para conferir o cadastro salvo.

O [roteiro completo da apresentação](ROTEIRO_APRESENTACAO.md) inclui a ordem das telas e sugestões de como explicar a lógica.

## Entenda o código

**Python · Tkinter · JSON**

| Arquivo | Responsabilidade |
| --- | --- |
| [`acessos.py`](acessos.py) | Filtra os portais pelo setor do funcionário. É o melhor ponto para começar a leitura. |
| [`cadastro.py`](cadastro.py) | Carrega e salva os cadastros em `dados.json` e copia as imagens para `imagens/`. |
| [`central.py`](central.py) | Monta as telas, liga os botões às ações e abre os endereços no navegador. Está dividido em blocos: Entrada, Meus acessos, Detalhes e Administração. |

O filtro percorre os portais e inclui cada atalho quando o setor da pessoa está entre os liberados:

```python
elif usuario["setor"] in portal["setores"]:
    liberados.append(portal)
```

O clique na capa usa um `if` para saber onde o mouse estava:

```python
if evento.y > CAPA_ALTURA - FAIXA:
    tela_detalhes(portal)  # clicou na faixa
else:
    abrir_portal(portal)  # clicou na imagem
```

E abrir o portal usa a biblioteca padrão do Python:

```python
webbrowser.open(portal["endereco"])
```

Além de `if`, `elif` e `else`, o código usa `def`, listas, dicionários, `for` e `lambda` (nos botões: "quando clicar, rode isto").

## Testes

O programa foi aberto e as telas foram controladas por um roteiro de teste. Tudo passou:

- **Cadastro:** um portal com capa e 4 prints, liberado só para o Financeiro, é salvo no `dados.json`. O 5º print é recusado e as imagens vão para `imagens/`.
- **Financeiro:** a conta vê o portal. Nome e capa abrem o endereço, e a faixa aparece e some com o mouse. A faixa leva aos detalhes sem abrir o navegador, as miniaturas trocam o print grande e **Abrir portal** abre o endereço.
- **Operações:** não vê o portal até o administrador liberar. Depois de liberado, vê.
- **Persistência:** depois de fechar e reabrir, portal, permissões e funcionários novos continuam salvos.
- **Outros casos:** senha errada é recusada, funcionário não vê a Administração, e uma conta nova do Comercial vê só os sistemas do Comercial.
- **Telas:** conferidas em 1024 × 650 e em 1920 × 1080.

As capturas foram tiradas no Linux, com fonte parecida com a Segoe UI. As imagens com "TESTE" escrito foram feitas só para o teste. Os endereços dos seis sistemas iniciais não puderam ser abertos no ambiente de teste e devem ser conferidos antes da apresentação.

## Escopo acadêmico

Esta versão roda localmente. O filtro por setor organiza a **visibilidade dos atalhos na Central**; quem souber um endereço ainda consegue abri-lo direto no navegador, e por isso o login de cada sistema continua valendo. As contas são gravadas em texto no arquivo local `dados.json`. Para uma implantação interna, a autenticação e a gestão de contas precisariam ser avaliadas com a equipe de TI da empresa.

Em 1024 × 650 a tela Meus acessos mostra 6 capas; com mais portais seria preciso adicionar rolagem. O vermelho `#C8102E` é provisório e fica na variável `VERMELHO`, no começo do `central.py`.

## Apoio no desenvolvimento
