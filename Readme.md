
# 📊 EasyCollector Automation – Instruções de Uso

Este projeto automatiza a consulta de informações de dívida ativa e status de acordo para uma lista de CPFs em um arquivo Excel. O processo é dividido em duas etapas (dois scripts):

---

## ✅ ETAPA 1 – Obter Dívida por CPF

**Script:** `obter_divida_cpf.py`  
**Objetivo:** Consultar a dívida ativa de cada CPF da planilha e preencher os campos `cod_cliente`, `cod_acordo`, `status`, e `observacao`.

### Como usar:

1. **Abrir o script `obter_divida_cpf.py`.**
2. **Selecionar o arquivo Excel (.xlsx)** com os CPFs que deseja consultar.
   - A planilha deve conter a coluna chamada exatamente `cpf`.
3. O script realizará as consultas automaticamente e preencherá os seguintes campos:
   - `cod_cliente`
   - `cod_acordo`
   - `status` (`Encontrado`, `Investigar`, etc.)
   - `observacao` (`Encontrado com sucesso`, `Não encontrado`, etc.)
4. O Excel será salvo automaticamente a cada linha processada no local especificado por você.
5. Um log de erros será salvo como `log_obter_divida.txt` na mesma pasta do Excel.
6. Ao final, será exibido um resumo das ocorrências por status.

---

## ✅ ETAPA 2 – Consultar Acordo

**Script:** `consultar_acordo.py`  
**Objetivo:** Consultar o status do acordo usando os campos `cod_cliente` e `cod_acordo` preenchidos na Etapa 1.

### Como usar:

1. **Rodar o script `consultar_acordo.py`.**
2. **Selecionar o arquivo Excel que foi salvo na Etapa 1.**
   - Ele deve conter as colunas `cod_cliente` e `cod_acordo`.
3. O script fará uma consulta ao status do acordo e preencherá a nova coluna:
   - `status_acordo`
4. O Excel será salvo continuamente durante o processo.
5. Um log de erros será salvo como `log_consultar_acordo.txt`.
6. Barra de progresso e contadores de linhas processadas estão incluídos na interface.

---

## 🔄 Requisitos

- Python 3.9 ou superior.
- Pacotes necessários (instalar com `pip install` se necessário):
  ```bash
  pip install pandas requests beautifulsoup4 openpyxl
  ```

---

## 📝 Observações

- Certifique-se de que os arquivos Excel não estejam abertos no Excel durante o processamento para evitar erros de permissão.
- O botão “Parar” salva o progresso atual antes de interromper.
- O botão “Cancelar” encerra sem salvar os dados processados.
- Em caso de erro HTTP, timeouts ou respostas inválidas, o log detalhado indicará linha por linha.

---

## 📁 Arquivos Gerados

- Excel atualizado com os resultados (na pasta escolhida).
- Logs:
  - `log_obter_divida.txt`
  - `log_consultar_acordo.txt`
