# Extração automática de Atestados Médicos

**Período:** 2025.1
**Aluno:** Caio Faria Diniz
**Email:** caiodiniz200204@gmail.com

---

## Objetivo

Automatizar a análise e validação de atestados médicos, reduzindo fraudes e agilizando processos internos de afastamento.

---

## Funcionalidades principais

* Extrair informações do atestado, como nome do médico, CRM, CID e período de afastamento.
* Validar se o CRM do médico está ativo utilizando APIs de conselhos médicos.
* Verificar a coerência entre o tempo de afastamento e o código CID informado.
* Gerar notificações automáticas para gestores e RH.
* Armazenar um histórico de atestados para análises futuras.

---

## Metodologia

* Aplicação de OCR e PLN para extração e categorização de dados.
* Uso de APIs externas para validar CRMs de médicos e verificar autenticidade dos atestados.
* Implementação de regras de verificação para identificar padrões suspeitos.

---

## Requisitos

* Acesso a uma base de atestados médicos para treinamento do sistema.
* Integração com bases médicas para validação de CRMs e códigos CID.
* Definição de regras internas para aceitação ou rejeição automática de atestados.

---
# Diretrizes de Uso do Repositório

## 1. Configuração da chave SSH

Antes de clonar o repositório, é necessário configurar a chave SSH para autenticação no GitHub. Para isso, siga os passos abaixo:

- **Chave SSH**: Para configurar a chave SSH, siga o tutorial disponível em [Configuração da chave SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent).

## 2. Clonagem do repositório

- **Clonagem**: Para clonar o repositório, utilize o comando `git clone git@github.com:SolidesTech/repo-name.git`

## 3. Utilização do repositório

- **Branches**:
  - Cada projeto deve ser desenvolvido em uma branch específica. A branch main não deve ser utilizada para desenvolvimento.
  - Utilize a branch `research` para o seu projeto de pesquisa.
  - Se necessário, para criar uma nova branch, utilize o comando `git checkout -b <branch>`. Exemplo: `git checkout -b dev`.
  - Para alterar de branch, utilize o comando `git checkout <branch>`. Exemplo: `git checkout research`.
- **Requirements**: 
  - Crie um arquivo `requirements.txt` com as dependências do projeto, as bibliotecas utilizadas e suas respectivas versões.

## 4. Commits

As mensagens de commit devem seguir a convenção abaixo:

1. [Conventional Commits:](https://www.conventionalcommits.org/en/v1.0.0/)
2. [Conventional Commits Messages- GitHub:](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13)

- API relevant changes
    - `feat`: Commits that add or remove a new feature
    - `fix`: Commits that fix a bug
- `refactor`: Commits that rewrite/restructure your code, however, do not change any API behavior
  - `perf`: Commits that are special refactor commits, that improve performance
- `style`: Commits that do not affect the meaning (white-space, formatting, missing semi-colons, etc.)
- `test`: Commits that add missing tests or correct existing tests
- `docs`: Commits that affect documentation only
- `build`: Commits that affect build components like build tool, CI pipeline, dependencies, project version, etc.
- `ops`: Commits that affect operational components like infrastructure, deployment, backup, recovery, etc.
- `chore`: Miscellaneous commits e.g. modifying `.gitignore`


## 5. Git Ignore

- **Arquivos**: Adicione ao arquivo `.gitignore` os arquivos que não devem ser versionados no repositório.
- Exemplos de arquivos que devem ser ignorados:
  - .env e arquivos com credenciais
  - Arquivos de mídia que não fazem parte da documentação do projeto: imagens, vídeos, etc.
  - Base de dados local e CSVs com dados sensíveis
  - Arquivos de logs e arquivos temporários
  - Qualquer arquivo que tenha um tamanho muito grande e não seja necessário para o projeto

### 6. Documentação

- **README**: O arquivo `README.md` deve conter informações sobre o projeto, como descrição, instruções de instalação e utilização, e demais informações relevantes. 
- Faça a modificação do arquivo `README.md` dentro da branch do projeto, não na branch `main`.
