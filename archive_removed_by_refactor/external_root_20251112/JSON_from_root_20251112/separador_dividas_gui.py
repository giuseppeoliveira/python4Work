"""
Separador de Dívidas XML - Interface Gráfica
Extrai e separa cada bloco <DividaAtiva> em formato JSON legível
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import xml.etree.ElementTree as ET
import json
from datetime import datetime
import os


class SeparadorDividasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Separador de Dívidas XML - Easy Collector")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Criar interface
        self.criar_interface()
        
        # Centralizar janela
        self.centralizar_janela()
    
    def configurar_estilo(self):
        """Configura o estilo da interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo dos botões
        style.configure('Action.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       padding=10,
                       background='#3498db',
                       foreground='white')
        
        style.map('Action.TButton',
                 background=[('active', '#2980b9')])
        
        # Estilo dos labels
        style.configure('Title.TLabel',
                       font=('Segoe UI', 14, 'bold'),
                       background='#2c3e50',
                       foreground='white')
        
        style.configure('Info.TLabel',
                       font=('Segoe UI', 10),
                       background='#2c3e50',
                       foreground='#ecf0f1')
    
    def criar_interface(self):
        """Cria a interface gráfica"""
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        titulo = ttk.Label(main_frame,
                          text="🔧 Separador de Dívidas XML",
                          style='Title.TLabel')
        titulo.pack(pady=(0, 10))
        
        # Instruções
        instrucoes = ttk.Label(main_frame,
                              text="Cole o XML completo abaixo e clique em 'Processar'",
                              style='Info.TLabel')
        instrucoes.pack(pady=(0, 15))
        
        # Frame para área de texto
        text_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RIDGE, bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Label da área de texto
        label_xml = tk.Label(text_frame,
                            text="Cole o XML aqui:",
                            font=('Segoe UI', 10, 'bold'),
                            bg='#34495e',
                            fg='white')
        label_xml.pack(anchor=tk.W, padx=10, pady=(10, 5))
        
        # Área de texto para XML
        self.text_xml = scrolledtext.ScrolledText(
            text_frame,
            font=('Consolas', 10),
            bg='#2c3e50',
            fg='#ecf0f1',
            insertbackground='white',
            selectbackground='#3498db',
            wrap=tk.WORD,
            height=20
        )
        self.text_xml.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Frame para botões
        btn_frame = tk.Frame(main_frame, bg='#2c3e50')
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botão Processar
        self.btn_processar = ttk.Button(
            btn_frame,
            text="▶ PROCESSAR XML",
            style='Action.TButton',
            command=self.processar_xml
        )
        self.btn_processar.pack(side=tk.LEFT, padx=(0, 10), ipadx=20)
        
        # Botão Limpar
        btn_limpar = ttk.Button(
            btn_frame,
            text="🗑 LIMPAR",
            command=self.limpar_campos
        )
        btn_limpar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão Sair
        btn_sair = ttk.Button(
            btn_frame,
            text="✖ SAIR",
            command=self.root.quit
        )
        btn_sair.pack(side=tk.RIGHT)
        
        # Frame para status
        status_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RIDGE, bd=2)
        status_frame.pack(fill=tk.X)
        
        # Label de status
        self.label_status = tk.Label(
            status_frame,
            text="Aguardando XML...",
            font=('Segoe UI', 10),
            bg='#34495e',
            fg='#ecf0f1',
            anchor=tk.W,
            padx=10,
            pady=10
        )
        self.label_status.pack(fill=tk.X)
    
    def centralizar_janela(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def limpar_xml(self, texto):
        """Remove texto antes do XML e limpa duplicados"""
        # Remover texto antes do XML
        inicio_xml = texto.find('<?xml')
        if inicio_xml == -1:
            inicio_xml = texto.find('<string')
        
        if inicio_xml > 0:
            texto = texto[inicio_xml:]
        
        # Procurar pelo final do XML (</string>)
        fim_xml = texto.find('</string>')
        if fim_xml != -1:
            fim_xml = texto.find('>', fim_xml) + 1
            texto = texto[:fim_xml]
        
        return texto.strip()
    
    def extrair_dividas(self, xml_string):
        """Extrai todos os blocos DividaAtiva como dicionários"""
        try:
            # Limpar XML
            xml_string = self.limpar_xml(xml_string)
            
            # Parse do XML
            root = ET.fromstring(xml_string)
            
            # Remover namespace
            for elem in root.iter():
                if '}' in elem.tag:
                    elem.tag = elem.tag.split('}', 1)[1]
            
            # Buscar cliente
            clientes = root.findall('.//ClienteDivida')
            if not clientes:
                return None, "Nenhum cliente encontrado no XML"
            
            # Extrair ID do cliente
            id_cliente_elem = clientes[0].find('IdCliente')
            id_cliente = id_cliente_elem.text if id_cliente_elem is not None else "N/A"
            
            # Buscar todas as dívidas
            dividas = clientes[0].findall('.//DividaAtiva')
            
            if not dividas:
                return None, "Nenhuma dívida encontrada no XML"
            
            # Processar cada dívida
            lista_dividas = []
            
            for idx, divida in enumerate(dividas, 1):
                divida_dict = {
                    'BLOCO': idx,
                    'IdCliente': id_cliente
                }
                
                # Extrair todos os campos da dívida
                for child in divida:
                    tag = child.tag
                    valor = child.text if child.text else ""
                    divida_dict[tag] = valor
                
                lista_dividas.append(divida_dict)
            
            return lista_dividas, None
            
        except Exception as e:
            return None, f"Erro ao processar XML: {str(e)}"
    
    def formatar_divida_json(self, divida):
        """Formata uma dívida como JSON legível"""
        return json.dumps(divida, indent=2, ensure_ascii=False)
    
    def salvar_arquivo(self, conteudo):
        """Abre diálogo para salvar arquivo TXT"""
        arquivo = filedialog.asksaveasfilename(
            title="Salvar Dívidas Separadas",
            defaultextension=".txt",
            filetypes=[
                ("Arquivo de Texto", "*.txt"),
                ("Todos os arquivos", "*.*")
            ],
            initialfile=f"dividas_separadas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        
        if arquivo:
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(conteudo)
                return arquivo
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar arquivo:\n{e}")
                return None
        
        return None
    
    def processar_xml(self):
        """Processa o XML e separa as dívidas"""
        
        # Obter texto do XML
        xml_text = self.text_xml.get("1.0", tk.END).strip()
        
        if not xml_text:
            messagebox.showwarning("Aviso", "Por favor, cole o XML antes de processar!")
            return
        
        # Atualizar status
        self.label_status.config(text="🔄 Processando XML...")
        self.root.update()
        
        # Extrair dívidas
        dividas, erro = self.extrair_dividas(xml_text)
        
        if erro:
            self.label_status.config(text=f"❌ Erro: {erro}")
            messagebox.showerror("Erro", erro)
            return
        
        # Criar conteúdo do arquivo
        conteudo_linhas = []
        
        # Cabeçalho
        conteudo_linhas.append("=" * 80)
        conteudo_linhas.append("DÍVIDAS SEPARADAS - EASY COLLECTOR")
        conteudo_linhas.append("=" * 80)
        conteudo_linhas.append(f"Data de Extração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        conteudo_linhas.append(f"Total de Dívidas: {len(dividas)}")
        conteudo_linhas.append(f"ID Cliente: {dividas[0]['IdCliente']}")
        conteudo_linhas.append("=" * 80)
        conteudo_linhas.append("")
        
        # Adicionar cada dívida
        for divida in dividas:
            bloco_num = divida['BLOCO']
            conteudo_linhas.append("")
            conteudo_linhas.append("/" * 80)
            conteudo_linhas.append(f"BLOCO {bloco_num} - DÍVIDA")
            conteudo_linhas.append("/" * 80)
            conteudo_linhas.append("")
            conteudo_linhas.append(self.formatar_divida_json(divida))
            conteudo_linhas.append("")
        
        # Rodapé
        conteudo_linhas.append("")
        conteudo_linhas.append("=" * 80)
        conteudo_linhas.append("FIM DO ARQUIVO")
        conteudo_linhas.append("=" * 80)
        
        conteudo_completo = '\n'.join(conteudo_linhas)
        
        # Salvar arquivo
        arquivo_salvo = self.salvar_arquivo(conteudo_completo)
        
        if arquivo_salvo:
            self.label_status.config(
                text=f"✅ Processado! {len(dividas)} dívidas salvas em: {os.path.basename(arquivo_salvo)}"
            )
            messagebox.showinfo(
                "Sucesso",
                f"✅ Processamento concluído!\n\n"
                f"Total de dívidas: {len(dividas)}\n"
                f"Arquivo salvo em:\n{arquivo_salvo}"
            )
        else:
            self.label_status.config(text="⚠️ Processamento cancelado")
    
    def limpar_campos(self):
        """Limpa todos os campos"""
        self.text_xml.delete("1.0", tk.END)
        self.label_status.config(text="Aguardando XML...")


def main():
    root = tk.Tk()
    app = SeparadorDividasGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
