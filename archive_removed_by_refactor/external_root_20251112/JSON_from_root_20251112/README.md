# 📄 Separador de Dívidas XML - Easy Collector

Aplicação com interface gráfica para extrair e separar blocos `<DividaAtiva>` de XML do Easy Collector, convertendo cada dívida em formato JSON legível e salvando em arquivo TXT.

---

## 🎯 O que faz?

Esta aplicação processa XML do sistema **Easy Collector** e:

1. ✅ Extrai todos os blocos `<DividaAtiva>` do XML
2. ✅ Converte cada bloco em formato **JSON legível**
3. ✅ Separa visualmente cada dívida com cabeçalhos
4. ✅ Salva tudo em um **arquivo TXT** no local escolhido por você
5. ✅ Exibe resumo com total de dívidas e ID do cliente

---

## 🚀 Como Rodar

### Pelo Terminal (PowerShell):

```powershell
cd "c:\Users\giuseppe_oliveira\Desktop\Python4Work\JSON"
python separador_dividas_gui.py
```

### Clicando duas vezes:
- Clique duas vezes no arquivo `separador_dividas_gui.py`

---

## 📋 Como Usar

1. **Copie o XML do navegador**
   - Acesse o Easy Collector
   - Copie TODO o XML (incluindo `<string xmlns=...>`)

2. **Cole na aplicação**
   - Cole o XML na área de texto grande
   - Não precisa limpar o texto antes, a aplicação faz isso

3. **Processe**
   - Clique no botão **"▶ PROCESSAR XML"**
   - Aguarde o processamento

4. **Salve**
   - Escolha onde salvar o arquivo TXT
   - O nome padrão será: `dividas_separadas_AAAAMMDD_HHMMSS.txt`

5. **Pronto!**
   - Abra o arquivo TXT gerado
   - Cada dívida estará separada e formatada

---

## 📂 Estrutura do XML Esperado

O XML deve começar com:

```xml
<string xmlns="http://easycollector.wedoo.com.br/easycollectorws/">
  <ArrayOfClienteDivida>
    <ClienteDivida>
      <IdCliente>6778770</IdCliente>
      <DividaCollection>
        <DividaAtiva>
          <!-- Dados da dívida aqui -->
        </DividaAtiva>
        <DividaAtiva>
          <!-- Próxima dívida -->
        </DividaAtiva>
        <!-- ... mais dívidas ... -->
      </DividaCollection>
    </ClienteDivida>
  </ArrayOfClienteDivida>
</string>
```

---

## 📝 Formato do Arquivo TXT Gerado

```
================================================================================
DÍVIDAS SEPARADAS - EASY COLLECTOR
================================================================================
Data de Extração: 23/10/2025 15:30:45
Total de Dívidas: 17
ID Cliente: 6778770
================================================================================

////////////////////////////////////////////////////////////////////////////////
BLOCO 1 - DÍVIDA
////////////////////////////////////////////////////////////////////////////////

{
  "BLOCO": 1,
  "IdCliente": "6778770",
  "Marcado": "false",
  "TipoDivida": "Original",
  "Identificador": "53008589",
  "NumeroPrestacao": "1",
  "DataVencimento": "2026-02-28T00:00:00",
  "ValorDividaIntegral": "8865.21",
  "ValorCorrecao": "6379.19",
  "Atraso": "-129",
  "NmCedente": "FICOU FACIL - CARTEIRA",
  "NmProduto": "CCB FICOU FACIL ESTOQUE - CARTEIRA",
  ...
}

////////////////////////////////////////////////////////////////////////////////
BLOCO 2 - DÍVIDA
////////////////////////////////////////////////////////////////////////////////

{
  "BLOCO": 2,
  "IdCliente": "6778770",
  ...
}

... (continua para todas as dívidas)

================================================================================
FIM DO ARQUIVO
================================================================================
```

---

## 🔧 Campos Extraídos de Cada Dívida

Todos os campos do bloco `<DividaAtiva>` são extraídos, incluindo:

### 📊 Identificação:
- `IdCliente` - ID do cliente
- `Identificador` - Identificador da dívida
- `NumeroPrestacao` - Número da prestação
- `IdDivida` - ID único da dívida
- `IdContrato` - ID do contrato
- `IdAcordo` - ID do acordo (se houver)
- `DividaCedente` - Código da dívida no cedente

### 💰 Valores:
- `ValorDividaIntegral` - Valor original
- `ValorDividaCalculo` - Valor para cálculo
- `ValorCorrecao` - Valor da correção
- `ValorJuros` - Valor dos juros
- `ValorMulta` - Valor da multa
- `ValorMinimo` - Valor mínimo
- `ValorAtualizado` - Valor atualizado
- `ValorDescontoPrincipal` - Desconto no principal
- `ValorDescontoJuros` - Desconto nos juros

### 📅 Datas:
- `DataVencimento` - Data de vencimento
- `DataPagamento` - Data de pagamento
- `DataInclusao` - Data de inclusão
- `DataCorrecao` - Data da correção

### ℹ️ Informações:
- `TipoDivida` - Tipo (Original, ParcelaAcordo, etc)
- `Marcado` - Se está marcado
- `Atraso` - Dias de atraso (negativo = a vencer)
- `TipoFatura` - Tipo de fatura
- `NmCedente` - Nome do cedente
- `NmProduto` - Nome do produto
- `nmAssessoria` - Nome da assessoria
- `idProduto` - ID do produto
- `IdCedente` - ID do cedente

---

## ⚙️ Configurações

### 🎨 Personalizar Aparência

Edite o arquivo `separador_dividas_gui.py`:

**Tamanho da janela (linha ~24):**
```python
self.root.geometry("900x700")  # Largura x Altura
```

**Cores (linhas ~25-26):**
```python
self.root.configure(bg='#2c3e50')  # Cor de fundo
```

**Fonte da área de texto (linha ~78):**
```python
font=('Consolas', 10),  # Fonte e tamanho
```

### 📝 Personalizar Formato do Arquivo

**Nome padrão do arquivo (linha ~215):**
```python
initialfile=f"dividas_separadas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
```

**Cabeçalho do arquivo (linhas ~243-251):**
```python
conteudo_linhas.append("=" * 80)
conteudo_linhas.append("DÍVIDAS SEPARADAS - EASY COLLECTOR")
```

**Separador de blocos (linhas ~256-258):**
```python
conteudo_linhas.append("/" * 80)
conteudo_linhas.append(f"BLOCO {bloco_num} - DÍVIDA")
```

### 🔢 Alterar Indentação do JSON

**Indentação do JSON (linha ~174):**
```python
return json.dumps(divida, indent=2, ensure_ascii=False)
# indent=2 significa 2 espaços
# Mude para indent=4 para 4 espaços
```

---

## 🐛 Solução de Problemas

### ❌ Erro: "Nenhum cliente encontrado no XML"
**Causa:** XML incompleto ou formato incorreto  
**Solução:** Certifique-se de copiar TODO o XML, incluindo `<string xmlns=...>` no início

### ❌ Erro: "Nenhuma dívida encontrada no XML"
**Causa:** XML não contém blocos `<DividaAtiva>`  
**Solução:** Verifique se o XML tem dívidas para extrair

### ❌ Janela não abre
**Causa:** Python não instalado ou tkinter ausente  
**Solução:** 
```powershell
# Verificar Python
python --version

# Testar tkinter
python -c "import tkinter"
```

### ❌ Arquivo não salva
**Causa:** Sem permissão na pasta escolhida  
**Solução:** Escolha outra pasta (ex: Desktop, Documentos)

---

## 📦 Dependências

- **Python 3.6+** (instalado)
- **tkinter** (vem com Python)
- **xml.etree.ElementTree** (biblioteca padrão)
- **json** (biblioteca padrão)
- **datetime** (biblioteca padrão)

**Nenhuma instalação adicional necessária!** ✅

---

## 💡 Dicas

1. **XML duplicado?** A aplicação remove automaticamente XML duplicado
2. **Texto antes do XML?** A aplicação ignora texto antes de `<string xmlns=`
3. **Muitas dívidas?** O arquivo TXT pode ficar grande, mas abre normalmente
4. **Quer JSON puro?** Mude a extensão de `.txt` para `.json` ao salvar
5. **Backup automático?** Os arquivos têm timestamp no nome para não sobrescrever

---

## 🎯 Casos de Uso

- ✅ Análise individual de cada dívida
- ✅ Comparação entre prestações
- ✅ Exportação para outros sistemas
- ✅ Backup de informações de dívidas
- ✅ Auditoria de dados
- ✅ Preparação para importação em planilhas

---

## 📞 Suporte

Se tiver problemas:
1. Verifique se copiou TODO o XML
2. Confira se o XML tem o formato esperado
3. Teste com um XML menor primeiro
4. Verifique as mensagens de erro na tela

---

## 🚀 Versão

**v1.0** - 23/10/2025
- Interface gráfica intuitiva
- Processamento automático de XML
- Exportação para TXT com JSON formatado
- Suporte a múltiplas dívidas
- Remoção automática de duplicatas

---

## 📄 Arquivo Principal

- `separador_dividas_gui.py` - Aplicação completa (único arquivo necessário)

**É só esse arquivo!** Nada mais é necessário para rodar. 🎉
