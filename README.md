# Python4Work Professional 🚀

Sistema profissional integrado para automação de processos financeiros com interface gráfica avançada.

## 📋 Funcionalidades

### 🎯 Principais Recursos
- **Obter Dívida por CPF**: Consulta e preenche códigos de cliente e acordo baseado em correspondência por data
- **Consultar Acordo**: Verifica status de acordos usando códigos previamente obtidos
- **Extrair JSON**: Processa requisições e extrai dados estruturados
- **Converter CSV/XLSX**: Conversão bidirecional entre formatos
- **Resolver Duplicatas**: Sistema inteligente para resolver registros duplicados baseado em regras
- **🛡️ NoLog**: Mantém sua sessão ativa impedindo bloqueio de tela e timeout automático
- **🔧 Separador de Dívidas**: Extrai e separa dívidas de XML do Easy Collector em formato JSON legível

### ✨ Características Avançadas
- **Correspondência por Data**: Sistema inteligente que correlaciona `data_pagamento` do Excel com `DataPagamento` da API
- **Processamento em Lote**: Performance otimizada com ThreadPoolExecutor (até 15 threads paralelas)
- **Validação Robusta**: Sistema de validação multicamadas para garantir integridade dos dados
- **Interface Profissional**: Tema moderno com barra de progresso e controles avançados
- **Sistema de Logging**: Logs estruturados para auditoria e debug
- **Gestão de Sessões**: Pool de conexões HTTP reutilizáveis para melhor performance

## 🛠 Tecnologias Utilizadas

- **Python 3.8+**
- **Tkinter**: Interface gráfica nativa
- **Pandas**: Manipulação de dados Excel/CSV
- **Requests**: Comunicação HTTP otimizada
- **BeautifulSoup**: Parsing XML/HTML
- **ThreadPoolExecutor**: Processamento paralelo
- **Dotenv**: Gestão segura de credenciais

## ⚙️ Configuração

### 1. Instalação de Dependências
```bash
pip install -r requirements.txt
```

### 2. Configuração de Environment
Crie um arquivo `.env` na raiz do projeto:
```env
LOGIN=seu_usuario
SENHA=sua_senha
URL=http://endereco_da_api/consultar
URL_DIVIDA=http://endereco_da_api/obter_divida
```

### 3. Execução
```bash
python main.py
```

## 📊 Como Usar

### Fluxo Recomendado

#### 1. Obter Dívida por CPF
- **Entrada**: Excel com colunas `cpf`, `data_pagamento`, `cod_cliente`
- **Processo**: Sistema consulta API e preenche `cod_acordo` baseado na correspondência por data
- **Saída**: Excel atualizado com códigos preenchidos

#### 2. Consultar Acordo
- **Entrada**: Excel resultante da etapa anterior (com `cod_cliente` e `cod_acordo` preenchidos)
- **Processo**: Consulta status dos acordos na API
- **Saída**: Excel com status e informações detalhadas dos acordos

### Estrutura do Excel

#### Para "Obter Dívida por CPF":
```
cpf | data_pagamento | cod_cliente | cod_acordo
14416204 | 2025-08-04 | 6778571 | 0
```

#### Após processamento:
```
cpf | data_pagamento | cod_cliente | cod_acordo | status | observacao
14416204 | 2025-08-04 | 6778571 | 59213193 | Update | Atualizado - cod_acordo: 59213193
```

### 🛡️ NoLog - Manter Sessão Ativa

Ferramenta que mantém sua sessão ativa impedindo bloqueio de tela e timeout automático.

**Recursos:**
- ✅ Movimento sutil do mouse a cada intervalo configurável
- ✅ Pressiona tecla Shift (não gera caracteres)
- ✅ Previne suspensão do sistema e da tela
- ✅ Interface visual com contador de ações
- ✅ Sons de notificação (pode ser desabilitado)
- ✅ Botão único LIGA/DESLIGA
- ✅ Failsafe: mova mouse para canto da tela para parar

**Configuração padrão:**
- Intervalo: 60 segundos
- Movimento de mouse: 1 pixel
- Sons: Habilitados

**Como usar:**
1. Clique no card "🛡️ NoLog - Manter Sessão"
2. Clique no botão "▶ INICIAR PROTEÇÃO"
3. A proteção ficará ativa mantendo sua sessão
4. Clique em "■ PARAR PROTEÇÃO" quando terminar

### 🔧 Separador de Dívidas XML

Extrai e separa cada bloco `<DividaAtiva>` de XMLs do Easy Collector em formato JSON legível.

**Recursos:**
- ✅ Cola XML direto na interface
- ✅ Remove texto duplicado ou inválido automaticamente
- ✅ Extrai todos os blocos `<DividaAtiva>` individualmente
- ✅ Converte cada bloco para JSON formatado (indent=2)
- ✅ Salva em arquivo TXT com separadores visuais
- ✅ Mais de 70 campos extraídos por dívida

**Como usar:**
1. Clique no card "🔧 Separador de Dívidas"
2. Cole o XML do Easy Collector na área de texto
3. Clique em "▶ PROCESSAR XML"
4. Escolha onde salvar o arquivo TXT
5. Cada dívida estará separada em blocos JSON legíveis

**Campos extraídos incluem:**
- Identificação: IdDivida, NumeroInscricao, OrigemDebito
- Valores: ValorConsolidado, ValorPrincipal, ValorMulta, ValorJuros
- Datas: DataInscricao, DataVencimento, DataConstituicao
- E mais de 60 outros campos relevantes

## 🔧 Arquitetura do Sistema

### Estrutura de Diretórios
```
python4Work/
├── main.py                 # Ponto de entrada da aplicação
├── config.json             # Configurações do sistema
├── requirements.txt        # Dependências Python
├── .env                    # Variáveis de ambiente (não versionado)
├── core/                   # Módulos principais
│   ├── config_manager.py   # Gestão de configurações
│   ├── professional_logger.py # Sistema de logging
│   ├── data_validator.py   # Validação de dados
│   └── theme_manager.py    # Gestão de temas visuais
├── src/                    # Lógica de negócio
│   ├── obter_divida_cpf.py # Processamento de CPFs
│   ├── consultar_acordo.py # Consulta de acordos
│   ├── extrair_json_corpo_requisicao.py
│   ├── conversor_csv_xlsx.py
│   ├── filtrar_duplicatas.py # Resolver duplicatas
│   ├── nolog/              # Módulo NoLog (manter sessão ativa)
│   │   ├── nolog_core.py
│   │   └── nolog_gui.py
│   └── separador_dividas/  # Módulo Separador de Dívidas XML
│       └── separador_dividas_gui.py
├── interfaces/             # Interface gráfica
│   └── interface_profissional.py
├── data/                   # Dados e modelos
│   └── Modelos/           # Templates Excel
└── logs/                   # Arquivos de log
    └── sessions/          # Logs por sessão
```

### Componentes Principais

#### 1. Sistema de Correspondência por Data
- Correlaciona `data_pagamento` do Excel com `DataPagamento` da API XML
- Busca inteligente em múltiplos blocos `<DividaAtiva>`
- Fallback para busca global caso não encontre correspondência exata

#### 2. Processamento Paralelo
- Pool de 15 workers para processamento simultâneo
- Batches de 25 registros para otimização de memória
- Sistema de retry automático para falhas de rede

#### 3. Validação Multicamadas
- Validação de entrada (CPF, códigos, datas)
- Validação de resposta da API
- Validação de integridade dos dados processados

## 🚨 Tratamento de Erros

### Cenários Comuns

#### "Dados inválidos" no Consultar Acordo
- **Causa**: `cod_cliente` ou `cod_acordo` são 0, vazios ou inválidos
- **Solução**: Execute primeiro "Obter Dívida por CPF" para preencher os códigos

#### CPF não encontrado
- **Causa**: CPF não existe na base ou dados inconsistentes
- **Status**: "Investigar" com observação "Não Encontrado na API"

#### Erro de conexão
- **Tratamento**: Retry automático com backoff exponencial
- **Logs**: Detalhamento completo para debugging

## 📈 Performance

### Otimizações Implementadas
- **Pool de Conexões**: Reutilização de sessões HTTP
- **Processamento Paralelo**: Até 15 threads simultâneas
- **Cache de Sessões**: Redução de overhead de autenticação
- **Timeout Otimizado**: 5s por requisição para balance performance/confiabilidade
- **Batching Inteligente**: Processamento em lotes de 25 registros

### Métricas Típicas
- **Throughput**: ~300-500 CPFs/minuto (dependendo da latência da API)
- **Uso de Memória**: ~50-100MB para arquivos de até 10.000 registros
- **Taxa de Sucesso**: >95% em condições normais de rede

## 🔒 Segurança

- **Credenciais**: Armazenadas em `.env` (não versionado)
- **Validação de Entrada**: Sanitização de todos os inputs
- **Logs Seguros**: Credenciais mascaradas nos logs
- **Sessões Isoladas**: Cada execução usa sessão única

## 📝 Changelog

### v2.0.0 (Agosto 2025)
- ✅ **Correspondência por Data**: Sistema inteligente de correlação Excel ↔ API
- ✅ **Performance Otimizada**: Processamento paralelo com ThreadPoolExecutor
- ✅ **Interface Profissional**: Novo tema e controles avançados
- ✅ **Validação Robusta**: Sistema multicamadas de validação
- ✅ **Logging Estruturado**: Auditoria completa de operações
- ✅ **Pool de Conexões**: Reutilização otimizada de sessões HTTP

### v1.x
- Funcionalidades básicas de consulta
- Interface simples
- Processamento sequencial

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é proprietário. Todos os direitos reservados.

---

**Desenvolvido com ❤️ para automação de processos financeiros**