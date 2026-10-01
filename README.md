# Digital Bank

API REST em Flask para clientes pessoa física (`individual`) e pessoa jurídica (`company`), com cadastro, consulta, saque e extrato.

Arquitetura em camadas: **routes → views → controllers → services → repositories → entities**.

## Funcionamento básico

O que falta para a API funcionar de ponta a ponta.

### Correções que bloqueiam o fluxo

- [ ] Devolver o `default=utc_now` em `TransactionTable.created_at`. Sem ele, todo saque falha com `IntegrityError` (`created_at` vai `NULL`).
- [ ] Definir como o cliente recebe saldo. Todo cliente nasce com `balance = 0`, então qualquer saque falha com `InsufficientBalance`. Opções: operação de depósito (o `TransactionType.DEPOSIT` já existe) ou saldo inicial no cadastro.

### Rotas

- [ ] Adapter Flask → `HttpRequest`/`HttpResponse`
  - [ ] `body` a partir de `request.get_json(silent=True)` (JSON malformado vira `None` → 400, em vez de erro do Flask)
  - [ ] `param` a partir de `request.view_args`
  - [ ] Resposta sem corpo quando `body is None` (o `204` do saque não pode enviar `null`)
- [ ] Composers/factories que montam repository → service → controller → view para cada rota
- [ ] Blueprint de individual
  - [ ] `POST /individuals`
  - [ ] `GET /individuals/<individual_id>`
  - [ ] `POST /individuals/<client_id>/withdraw`
  - [ ] `GET /individuals/<client_id>/statement`
- [ ] Blueprint de company
  - [ ] `POST /companies`
  - [ ] `GET /companies/<company_id>`
  - [ ] `POST /companies/<client_id>/withdraw`
  - [ ] `GET /companies/<client_id>/statement`
- [ ] Registrar os blueprints em `src/main/server/server.py`

> Os nomes dos parâmetros nas rotas precisam bater com o que cada view lê: `individual_id` / `company_id` nas views de get e `client_id` nas de withdraw e statement.

### Banco de dados

- [ ] Automatizar ou documentar a criação das tabelas (`Base.metadata.create_all(engine)` na subida do app, ou `sqlite3 storage.db < sql/schema.sql`)

### Testes

- [ ] Unitários de services com repositories mockados
  - [ ] Saque com sucesso (saldo atualizado e transação criada com o `client_type` certo)
  - [ ] `IndividualNotFound` / `CompanyNotFound`
  - [ ] `InsufficientBalance`
  - [ ] `WithdrawalLimitExceeded` (70% da renda para PF, 90% do faturamento para PJ)
  - [ ] Extrato de cliente inexistente → not found
- [ ] Unitários de views com controller mockado (400 / 422 / status de sucesso)
- [ ] Integração com `app.test_client()` e SQLite em memória, cobrindo todas as rotas
- [ ] Renomear `src/database/connetion_test.py` → `connection_test.py`

## Melhorias

Pontos que não impedem o funcionamento, mas melhoram a qualidade.

### Arquitetura e duplicação

- [ ] Extrair `BaseClientService` com `client_type`, `withdraw_limit_ratio`, `not_found_error` e `_reference_income()`. Hoje `withdraw`, `statement` e `get_client` estão duplicados nos dois services.
- [ ] Opcional: `__init_subclass__` na base para falhar cedo se uma subclasse esquecer alguma configuração
- [ ] Extrair `BaseClientRepository`, porque `get_client` e `update_balance` só mudam na tabela
- [ ] Corrigir resquícios de copiar e colar no `IndividualRepository` (variáveis chamadas `company`)

### Banco e consistência

- [ ] Deixar o `DBConnectionHandler` seguro com requisições simultâneas: criar o `sessionmaker` uma vez em `connect_to_db` e trocar `__enter__`/`__exit__` por um método `@contextmanager` com sessão local. Hoje o singleton guarda a sessão em `self.__session`, compartilhada entre threads.
- [ ] Tornar o saque atômico: o débito do saldo e a criação da transação devem ficar na mesma transação de banco
- [ ] Evitar condição de corrida no saque (`UPDATE ... SET balance = balance - :amount WHERE id = :id AND balance >= :amount`)
- [ ] `update_balance` não deveria falhar em silêncio quando o cliente não existe
- [ ] Ler a connection string de variável de ambiente em vez de deixá-la fixa em `connection.py`

### Domínio e validação

- [ ] Usar `Decimal` / `Numeric` para dinheiro em vez de `float` (entidades, schemas e cálculos)
- [ ] Validar os schemas de criação: `EmailStr`, `age` mínima, `monthly_income` / `monthly_revenue` ≥ 0, strings não vazias
- [ ] Opcional: `strict=True` no `WithdrawSchema` para recusar `"50.5"` como string

### Tipagem

- [ ] Parametrizar `ClientRepositoryInterface` nos services (`ClientRepositoryInterface[IndividualTable]`)
- [ ] Tipar o parâmetro `client` de `ClientRepositoryInterface.create_client` (`TypeVar` para o schema)
- [ ] `get_statement` retorna `Sequence` (de `.all()`), não `list`: converter com `list(...)` ou ajustar a anotação
- [ ] Renomear o parâmetro `monthly_revenue` de `IndividualService.calculate_withdraw_limit` (o valor recebido é `monthly_income`)

### Detalhes

- [ ] Adicionar `# pylint: disable=too-many-ancestors` em `UTCDateTime`, como já existe em `UUIDType`
- [ ] Registrar o `handle_unexpected_error` só fora do modo debug, para não esconder o traceback durante o desenvolvimento
- [ ] Tirar `debug=True` fixo do `run.py`
- [ ] Remover o roteiro do curso comentado no final do `run.py` quando o projeto estiver concluído
