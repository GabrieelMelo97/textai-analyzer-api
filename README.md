# Text Analysis API

## Sobre
A Text Analysis API é uma aplicação FastAPI que utiliza Inteligência Artificial Generativa através do modelo DeepSeek e LangGraph para análise avançada de textos. Combinando o poder dos Large Language Models (LLMs) com uma arquitetura moderna de microsserviços, a API realiza classificação de texto, extração de entidades e geração de resumos de forma eficiente e escalável. O sistema é projetado para processar e analisar textos em português, aproveitando as capacidades da IA Generativa para fornecer insights precisos e contextualizados.

## Funcionalidades
- 🔍 **Classificação de Texto**: Categoriza textos em diferentes classes (Notícias, Blog, Pesquisa, Outro)
- 🏷️ **Extração de Entidades**: Identifica e extrai entidades como Pessoas, Organizações e Locais
- 📝 **Geração de Resumos**: Cria resumos concisos dos textos fornecidos
- 🔑 **Autenticação via API Key**: Sistema seguro de autenticação
- ⚡ **Cache em Memória**: Otimização de performance para textos repetidos
- 🚦 **Rate Limiting**: Controle de taxa de requisições por API key

## Estrutura
```
.
├── app/
│   ├── api/
│   │   └── endpoints.py      # Endpoints da API
│   ├── core/
│   │   ├── config.py        # Configurações
│   │   ├── logging.py       # Sistema de logs
│   │   ├── rate_limiter.py  # Limitador de taxa
│   │   └── security.py      # Segurança e autenticação
│   ├── schemas/
│   │   └── text_analysis.py # Modelos Pydantic
│   ├── services/
│   │   └── text_analysis_service.py # Serviço de análise
│   └── main.py              # Aplicação principal
├── tests/                   # Testes automatizados
├── poetry.lock             # Lock de dependências
└── pyproject.toml          # Configuração do projeto
```

## Requisitos
- Python 3.9+
- Poetry (gerenciador de dependências)
- Chave de API do DeepSeek

## Instalação
1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/text-analysis-api.git
cd text-analysis-api
```

2. Instale as dependências com Poetry:
```bash
poetry install
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

## Como Usar
1. Inicie o servidor:
```bash
poetry run uvicorn app.main:app --reload
```

2. Faça uma requisição para analisar um texto:
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "X-API-Key: sua-api-key" \
  -H "Content-Type: application/json" \
  -d '{"text": "Seu texto para análise aqui"}'
```

3. Exemplo de resposta:
```json
{
  "classification": "Notícias",
  "entities": ["Pessoa1", "Organização1", "Local1"],
  "summary": "Resumo do texto"
}
```

## Testes
O projeto utiliza pytest para testes automatizados. Para executar os testes:

```bash
poetry run pytest
```

Para executar os testes com cobertura:
```bash
poetry run pytest --cov=app
```

## Contribuindo
1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---
⚠️ **Nota**: Certifique-se de ter uma chave de API válida do DeepSeek configurada no arquivo `.env` antes de executar a aplicação.