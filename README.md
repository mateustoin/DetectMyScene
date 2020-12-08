<figure class="image" align='center'>
    <img src="img/DetectMySceneHeader.png?raw=true">
    <figcaption></figcaption>
</figure>

## Índice
+ [Sobre](#sobre)
+ [Primeiros Passos](#primeiros_passos)
+ [Uso](#uso)
+ [Contribuiçōes](../CONTRIBUTING.md)

<h2 id="sobre">Sobre</h2>

O *Detect My Scene* foi um projeto realizado durante a live coding do <a href="">meu canal na Twitch</a>. O objetivo principal era realizar algum projeto assistivo, para suprir alguma necessidade. Através de discussões foi resolvido que poderíamos ajudar deficientes visuais, criando um programa que fosse capaz de descrever uma foto (que poderia ser extendido para vídeos também) através de texto ou áudio. Com isso o deficiente visual poderia tirar fotos em um ambiente ou até tirar fotos de alguma notícia ou artigo para rodar no software e ter uma breve descrição do que existe ali.

Para a criação dessa aplicação foram utilizados alguns conceitos de Inteligência Artificial e Processamento Digital de Imagens, com a biblioteca <a href="https://github.com/OlafenwaMoses/ImageAI">ImageAI</a> e alguns cálculos e aplicações implementadas do zero. O projeto é realizado em alguns passos.

Para a maioria dos testes durante o desenvolvimento do projeto, a imagem a seguir foi utilizada, além de algumas outras para validações. Os objetos identificados nas imagens testadas no desenvolvimento mostram apenas objetos que o algoritmo tem 45% ou mais de certeza de ser de fato aquilo que foi identificado.

<figure class="image" align='center'>
    <img src="img/example.jpg?raw=true">
    <figcaption>Figura 1. Imagem de teste</figcaption>
</figure>

<h3><b>Passo 1: Identificação dos objetos</b></h3>

Esse passo é realizado pela própria biblioteca utilizada (ImageAI), onde são identificados todos os objetos reconhecidos na imagem, informando o nome, probabilidade de ser aquele objeto específico e suas delimitações na imagem. Essas informações base são essenciais para os próximos passos, pois são com elas que todas as informações são cruzadas e geram novos resultados.

<figure class="image" align='center'>
    <img src="img/example_square.jpg?raw=true">
    <figcaption>Figura 2. Identificação da biblioteca</figcaption>
</figure>

<h3><b>Passo 2: </b></h3>

<h3><b>Passo 3: </b></h3>

<h3><b>Passo 4: </b></h3>

<h3><b>Passo 5: </b></h3>

link para os áudios:
https://soundcloud.com/mateus-antonio-11/sets/audios-projeto-detectmyscene

## Começando <a name = "comecando"></a>
Estas intruçōes te darão uma cópia funcional do projeto na sua máquina local para desenvolvimento e testes. Veja [deployment](#deployment) para uma descrição de como realizar o deployment deste projeto online.

### Pré-requisitos

Descreva o que é necessário para instalar este software e como instalá-lo.

```
Dê exemplos
```

### Instalação

Passo-a-passo com exemplos que reproduzam um estágio de desenvolvimento funcional.

Descreva o passo a ser tomado

```
Dê um exemplo
```

Repita

```
Até terminar
```

## Uso <a name="uso"></a>
Descreva como utilizar seu app ou sistema.

