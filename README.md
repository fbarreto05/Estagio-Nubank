# [**Estágio Nubank**](https://estagio.nubank.com.br/) &middot; [![Python](https://img.shields.io/static/v1?label=Python&message=3.11.15&color=ffff00&style=for-the-badge&logo=python)](https://www.python.org/)

[![Nubank](media/nubank-logo.png)](https://nubank.com.br/)

&#10024; Exercício desenvolvido para a fase de **dinâmica em grupo** do **programa de estágio da Nubank** &#10024;

<hr/>

## Enunciado &#x1F4C4;
![Enunciado](exercise.png)

## Como Usar &#x1f5a5;
* Rode o arquivo nubank.py em seu computador por meio de um interpretador de Python 3.11.15 ou superior.
* Um menu de opções irá aparecer, a partir dele, insira o valor correspondente à operação que deseja iniciar.
0. Encerra a execução do sistema.
1. Mostra os dados da conta, com estado atual e limite disponível.
2. Mostra o histórico de transações da conta, com valor, destinatário e horário para cada uma.
3. Realiza uma transação, com o valor e destinatário inseridos.
4. Muda o valor do limite disponível para o valor inserido.
5. Ativa ou inativa a conta, dependendo de seu estado atual.

## Funcionamento da Transação &#x1F4B2;
* A função de transações do sistema de pagamentos da Nubank irá receber como parâmetros o valor da transação e seu destinatário, e terá acesso aos dados da conta de quem solicitou a operação.
* O sistema então irá verificar se informações são válidas para a conclusão da transação, de acordo com as exigências de negócio descritas no [enunciado](#enunciado-) da questão.
* Caso não haja nenhuma violação das exigências, a transação é realizada, o seu valor (que deve ser positivo) é subtraído do limite disponível da conta e seus dados são incluídos no início do histórico de transações da conta que a solicitou.

## Testes &#x270F;
* Os testes unitários podem ser encontrados no arquivo test_nubank.py e executados por um interpretador de Python 3.11.15 ou superior.
* Os testes verificam se todas as exigências estão sendo cumpridas em diferentes casos de transação, e se as exceções esperadas estão sendo identificadas corretamente.
