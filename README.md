# Watchlist Tracker

Sobre:   
    A aplicação realiza o polling de uma rota no Yahoo Finance, popula uma base e, baseado nos limites (superiores e inferiores) pre-definidos pelo cliente é enviado um email informando se é o momento adequado para comprar ou vender aquele ativo.  

### Local
Requisitos:  
>    Python 3.7

Para instalar rode o seguinte:  
>    make install

Para executar o Django:  
>    make run-django

Para o Job:  
>    make run-huey

Para rodar ambos :
>   make run

Para matar os processos:
>   make stop

---
### Docker