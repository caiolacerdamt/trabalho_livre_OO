# Sistema de Gestão Financeira Pessoal

## Visão Geral do Projeto

Este é um projeto desenvolvido para a disciplina de Orientação a Objetos (semestre 01/2025) da Faculdade UnB Gama, ministrada pelo Prof. Henrique Moura. O objetivo principal é criar um sistema simples de gestão financeira pessoal que ajude o usuário a registrar e controlar suas receitas e despesas. O projeto foi desenvolvido individualmente e aplica os princípios de Programação Orientada a Objetos ensinados em sala de aula.

### Problema a Ser Resolvido

Muitas pessoas enfrentam dificuldades em manter um controle eficaz sobre suas finanças pessoais. Isso pode levar a gastos excessivos, falta de clareza sobre para onde o dinheiro está indo e dificuldade em planejar o futuro financeiro. Este sistema visa mitigar esses problemas, oferecendo uma ferramenta intuitiva para:
* Registrar todas as transações financeiras (receitas e despesas).
* Categorizar transações para uma análise mais detalhada.
* Visualizar o saldo atual de forma rápida.
* Consultar um extrato de transações para entender o fluxo de caixa.

## Casos de Uso

Os casos de uso abaixo descrevem as principais interações do usuário com o sistema. Eles servem como base para o desenvolvimento das funcionalidades, focando nos requisitos de Casos de Uso textuais em formato informal ou estruturado, devidamente completo[cite: 4].

### Ator Principal: Usuário

---

### **CU01: Registrar Receita**
* **Descrição:** O usuário registra uma nova entrada de dinheiro no sistema.
* **Fluxo Principal:**
    1.  O usuário acessa a funcionalidade de "Nova Transação".
    2.  O usuário seleciona o tipo "Receita".
    3.  O usuário informa o valor da receita.
    4.  O usuário insere uma breve descrição da receita (ex: "Salário", "Freelance").
    5.  O usuário seleciona a data da receita.
    6.  O usuário escolhe uma categoria existente para a receita (ex: "Salário", "Investimento").
    7.  O sistema valida os dados e adiciona a receita ao registro.
    8.  O sistema atualiza o saldo total e o extrato de transações.
    9.  O sistema persiste os dados.
* **Pós-condição:** A receita é registrada, o saldo é atualizado e os dados são salvos.

---

### **CU02: Registrar Despesa**
* **Descrição:** O usuário registra uma nova saída de dinheiro do sistema.
* **Fluxo Principal:**
    1.  O usuário acessa a funcionalidade de "Nova Transação".
    2.  O usuário seleciona o tipo "Despesa".
    3.  O usuário informa o valor da despesa.
    4.  O usuário insere uma breve descrição da despesa (ex: "Compras no Supermercado", "Aluguel").
    5.  O usuário seleciona a data da despesa.
    6.  O usuário escolhe uma categoria existente para a despesa (ex: "Alimentação", "Moradia", "Transporte").
    7.  O sistema valida os dados e adiciona a despesa ao registro.
    8.  O sistema atualiza o saldo total e o extrato de transações.
    9.  O sistema persiste os dados.
* **Pós-condição:** A despesa é registrada, o saldo é atualizado e os dados são salvos.

---

### **CU03: Visualizar Extrato de Transações**
* **Descrição:** O usuário visualiza uma lista de todas as transações registradas.
* **Fluxo Principal:**
    1.  O usuário acessa a área de extrato de transações.
    2.  O sistema exibe uma lista de todas as receitas e despesas, incluindo valor, descrição, data, categoria e tipo (Receita/Despesa).
    3.  (Opcional) O usuário pode filtrar o extrato por período (ex: mês, ano).
* **Pós-condição:** O extrato é exibido ao usuário.

---

### **CU04: Visualizar Saldo Atual**
* **Descrição:** O usuário verifica o valor total de suas finanças (receitas - despesas).
* **Fluxo Principal:**
    1.  O usuário acessa a interface principal do sistema.
    2.  O sistema calcula e exibe o saldo atual, considerando todas as receitas e despesas registradas.
* **Pós-condição:** O saldo atual é exibido ao usuário.

---

### **CU05: Gerenciar Categorias**
* **Descrição:** O usuário pode adicionar, remover ou visualizar categorias para organizar suas transações.
* **Fluxo Principal:**
    1.  O usuário acessa a funcionalidade de "Gerenciar Categorias".
    2.  O sistema exibe uma lista das categorias existentes.
    3.  **Sub-Fluxo: Adicionar Categoria**
        1.  O usuário informa um nome para a nova categoria.
        2.  O sistema valida o nome (não vazio, não duplicado).
        3.  O sistema adiciona a nova categoria e persiste os dados.
        4.  A lista de categorias é atualizada.
    4.  **Sub-Fluxo: Remover Categoria**
        1.  O usuário seleciona uma categoria da lista.
        2.  O sistema verifica se há transações associadas a essa categoria.
        3.  Se houver, o sistema impede a remoção e notifica o usuário.
        4.  Se não houver, o sistema pede confirmação ao usuário.
        5.  Se confirmado, o sistema remove a categoria e persiste os dados.
        6.  A lista de categorias é atualizada.
* **Pós-condição:** As categorias são gerenciadas e os dados são salvos.

---

## Estrutura do Projeto

O projeto segue uma arquitetura modular com os seguintes arquivos e pastas obrigatórios[cite: 9]:

* `README.md`: Este arquivo, contendo a definição do problema e os casos de uso.
* `main.py`: O ponto de entrada principal da aplicação, responsável por iniciar a interface gráfica.
* `package/`: Diretório que contém os módulos principais do sistema:
    * `models.py`: Define as classes de dados (e.g., `Transacao`, `Receita`, `Despesa`, `Categoria`).
    * `controllers.py`: Contém a lógica de negócios e gerenciamento de dados (e.g., `GerenciadorFinanceiro`).
    * `persistence.py`: Lida com a serialização e desserialização de objetos (salvar/carregar dados em JSON).
    * `views.py`: Contém a implementação da interface gráfica (Tkinter).

## Como Executar

1.  Clone este repositório.
2.  Certifique-se de ter Python 3.x instalado.
3.  Navegue até o diretório raiz do projeto.
4.  Baixe as dependências do projeto com: ```bash pip install -r requirements.txt ```
5.  Execute o arquivo `main.py`:
    ```bash
    python main.py
    ```


