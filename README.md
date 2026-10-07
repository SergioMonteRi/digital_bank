# Digital Bank

API REST em Flask para clientes pessoa física (`individual`) e pessoa jurídica (`company`), com cadastro, consulta, saque e extrato.

Arquitetura em camadas: **routes → views → controllers → services → repositories → entities**.

## Configuração

A connection string do banco vem da variável de ambiente `DATABASE_URL`, que é obrigatória: sem ela, o app não sobe.

Para configurar localmente, copie o exemplo e ajuste o valor se precisar:

```bash
cp .env.example .env
```

O `run.py` carrega o `.env` antes de importar o app. O arquivo `.env` não vai para o git.

Nos testes, o `conftest.py` da raiz define a `DATABASE_URL` com um SQLite em memória, então o `.env` não é necessário para rodar o `pytest`.

## Funcionamento básico

O que falta para a API funcionar de ponta a ponta.

### Testes

- [ ] Integração com `app.test_client()` e SQLite em memória, cobrindo todas as rotas

## Melhorias

Pontos que não impedem o funcionamento, mas melhoram a qualidade.

### Arquitetura e duplicação

- [ ] Extrair `BaseClientService` com `client_type`, `withdraw_limit_ratio`, `not_found_error` e `_reference_income()`. Hoje `withdraw`, `statement` e `get_client` estão duplicados nos dois services.
- [ ] Opcional: `__init_subclass__` na base para falhar cedo se uma subclasse esquecer alguma configuração
- [ ] Extrair `BaseClientRepository`, porque `get_client` e `update_balance` só mudam na tabela
- [ ] Corrigir resquícios de copiar e colar no `IndividualRepository` (variáveis chamadas `company`)
