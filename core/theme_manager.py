"""
Sistema de Temas Profissionais
Implementa temas visuais modernos e personalizáveis
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any

class ThemeManager:
    def __init__(self):
        self.themes = {
            'modern': {
                'name': 'Moderno',
                'description': 'Tema moderno com cores suaves',
                'colors': {
                    'primary': '#3498db',      # Azul principal
                    'secondary': '#2c3e50',    # Azul escuro
                    'success': '#27ae60',      # Verde sucesso
                    'warning': '#f39c12',      # Laranja aviso
                    'danger': '#e74c3c',       # Vermelho erro
                    'light': '#ecf0f1',        # Cinza claro
                    'dark': '#34495e',         # Cinza escuro
                    'background': '#ffffff',   # Fundo branco
                    'surface': '#f8f9fa',      # Superfície
                    'text': '#2c3e50',         # Texto principal
                    'text_secondary': '#7f8c8d', # Texto secundário
                    'border': '#bdc3c7',       # Bordas
                    'accent': '#9b59b6'        # Roxo accent
                }
            },
            'dark': {
                'name': 'Escuro',
                'description': 'Tema escuro para reduzir cansaço visual',
                'colors': {
                    'primary': '#4a90e2',
                    'secondary': '#1a1a1a',
                    'success': '#28a745',
                    'warning': '#ffc107',
                    'danger': '#dc3545',
                    'light': '#343a40',
                    'dark': '#121212',
                    'background': '#1e1e1e',
                    'surface': '#2d2d2d',
                    'text': '#ffffff',
                    'text_secondary': '#adb5bd',
                    'border': '#495057',
                    'accent': '#bb86fc'
                }
            },
            'corporate': {
                'name': 'Corporativo',
                'description': 'Tema profissional para ambiente corporativo',
                'colors': {
                    'primary': '#0056b3',
                    'secondary': '#495057',
                    'success': '#198754',
                    'warning': '#fd7e14',
                    'danger': '#dc3545',
                    'light': '#f8f9fa',
                    'dark': '#212529',
                    'background': '#ffffff',
                    'surface': '#f1f3f4',
                    'text': '#212529',
                    'text_secondary': '#6c757d',
                    'border': '#dee2e6',
                    'accent': '#6f42c1'
                }
            },
            'nature': {
                'name': 'Natureza',
                'description': 'Tema inspirado na natureza com tons verdes',
                'colors': {
                    'primary': '#28a745',
                    'secondary': '#155724',
                    'success': '#20c997',
                    'warning': '#ffc107',
                    'danger': '#dc3545',
                    'light': '#f8fff8',
                    'dark': '#0f5132',
                    'background': '#ffffff',
                    'surface': '#f0fff4',
                    'text': '#155724',
                    'text_secondary': '#6c757d',
                    'border': '#c3e6cb',
                    'accent': '#17a2b8'
                }
            }
        }
        self.current_theme = 'modern'
        self.custom_styles = {}
    
    def get_theme(self, theme_name: str = None) -> Dict[str, Any]:
        """Retorna configurações do tema"""
        theme_name = theme_name or self.current_theme
        return self.themes.get(theme_name, self.themes['modern'])
    
    def set_theme(self, theme_name: str):
        """Define tema ativo"""
        if theme_name in self.themes:
            self.current_theme = theme_name
        
    def get_color(self, color_key: str, theme_name: str = None) -> str:
        """Obtém cor específica do tema"""
        theme = self.get_theme(theme_name)
        return theme['colors'].get(color_key, '#000000')
    
    def apply_theme_to_widget(self, widget: tk.Widget, style_type: str = 'default'):
        """Aplica tema a um widget específico"""
        theme = self.get_theme()
        colors = theme['colors']
        
        style_configs = {
            'default': {
                'bg': colors['background'],
                'fg': colors['text']
            },
            'primary_button': {
                'bg': colors['primary'],
                'fg': 'white',
                'activebackground': self._darken_color(colors['primary']),
                'activeforeground': 'white',
                'relief': 'flat',
                'borderwidth': 0,
                'cursor': 'hand2'
            },
            'secondary_button': {
                'bg': colors['light'],
                'fg': colors['text'],
                'activebackground': colors['border'],
                'activeforeground': colors['text'],
                'relief': 'flat',
                'borderwidth': 1,
                'cursor': 'hand2'
            },
            'success_button': {
                'bg': colors['success'],
                'fg': 'white',
                'activebackground': self._darken_color(colors['success']),
                'activeforeground': 'white',
                'relief': 'flat',
                'borderwidth': 0,
                'cursor': 'hand2'
            },
            'warning_button': {
                'bg': colors['warning'],
                'fg': 'white',
                'activebackground': self._darken_color(colors['warning']),
                'activeforeground': 'white',
                'relief': 'flat',
                'borderwidth': 0,
                'cursor': 'hand2'
            },
            'danger_button': {
                'bg': colors['danger'],
                'fg': 'white',
                'activebackground': self._darken_color(colors['danger']),
                'activeforeground': 'white',
                'relief': 'flat',
                'borderwidth': 0,
                'cursor': 'hand2'
            },
            'card': {
                'bg': colors['surface'],
                'fg': colors['text'],
                'relief': 'solid',
                'borderwidth': 1,
                'bd': colors['border']
            },
            'title': {
                'bg': colors['background'],
                'fg': colors['secondary'],
                'font': ('Arial', 16, 'bold')
            },
            'subtitle': {
                'bg': colors['background'],
                'fg': colors['text'],
                'font': ('Arial', 12, 'bold')
            },
            'description': {
                'bg': colors['background'],
                'fg': colors['text_secondary'],
                'font': ('Arial', 9)
            },
            'progress_bar': {
                # Para ttk.Progressbar, configuramos via style
                'style_name': f'{style_type}.Horizontal.TProgressbar'
            }
        }
        
        config = style_configs.get(style_type, style_configs['default'])
        
        # Aplicar configurações ao widget
        for key, value in config.items():
            if key != 'style_name' and hasattr(widget, 'config'):
                try:
                    widget.config(**{key: value})
                except tk.TclError:
                    pass  # Ignorar propriedades não suportadas pelo widget
    
    def configure_ttk_styles(self, root: tk.Tk):
        """Configura estilos para widgets ttk"""
        style = ttk.Style(root)
        theme = self.get_theme()
        colors = theme['colors']
        
        # Configurar estilos personalizados
        styles_config = {
            'Modern.TProgressbar': {
                'configure': {
                    'background': colors['primary'],
                    'troughcolor': colors['light'],
                    'borderwidth': 0,
                    'lightcolor': colors['primary'],
                    'darkcolor': colors['primary']
                }
            },
            'Modern.TButton': {
                'configure': {
                    'background': colors['primary'],
                    'foreground': 'white',
                    'borderwidth': 0,
                    'focuscolor': colors['accent']
                },
                'map': {
                    'background': [('active', self._darken_color(colors['primary']))],
                    'foreground': [('active', 'white')]
                }
            },
            'Modern.TFrame': {
                'configure': {
                    'background': colors['background'],
                    'borderwidth': 0
                }
            },
            'Modern.TLabel': {
                'configure': {
                    'background': colors['background'],
                    'foreground': colors['text']
                }
            },
            'Card.TFrame': {
                'configure': {
                    'background': colors['surface'],
                    'relief': 'solid',
                    'borderwidth': 1
                }
            }
        }
        
        for style_name, config in styles_config.items():
            if 'configure' in config:
                style.configure(style_name, **config['configure'])
            if 'map' in config:
                style.map(style_name, **config['map'])
    
    def create_themed_window(self, root: tk.Tk, title: str = "Python4Work Professional"):
        """Cria janela com tema aplicado"""
        theme = self.get_theme()
        colors = theme['colors']
        
        # Configurar janela principal
        root.title(title)
        root.configure(bg=colors['background'])
        
        # Configurar ícone (se disponível)
        try:
            root.iconbitmap('icon.ico')
        except:
            pass
        
        # Configurar estilos ttk
        self.configure_ttk_styles(root)
        
        return root
    
    def create_card_frame(self, parent, title: str = None, **kwargs) -> tk.Frame:
        """Cria frame estilizado como card"""
        theme = self.get_theme()
        colors = theme['colors']
        
        # Frame principal do card
        card_frame = tk.Frame(parent, 
                            bg=colors['surface'],
                            relief='solid',
                            borderwidth=1,
                            **kwargs)
        
        if title:
            # Título do card
            title_frame = tk.Frame(card_frame, bg=colors['surface'])
            title_frame.pack(fill='x', padx=15, pady=(15, 5))
            
            title_label = tk.Label(title_frame, 
                                 text=title,
                                 bg=colors['surface'],
                                 fg=colors['secondary'],
                                 font=('Arial', 12, 'bold'))
            title_label.pack(anchor='w')
            
            # Linha separadora
            separator = tk.Frame(card_frame, height=1, bg=colors['border'])
            separator.pack(fill='x', padx=15, pady=(0, 10))
        
        return card_frame
    
    def create_status_label(self, parent, text: str = "Pronto", status: str = "info") -> tk.Label:
        """Cria label de status colorido"""
        theme = self.get_theme()
        colors = theme['colors']
        
        status_colors = {
            'info': colors['primary'],
            'success': colors['success'],
            'warning': colors['warning'],
            'error': colors['danger'],
            'secondary': colors['text_secondary']
        }
        
        label = tk.Label(parent,
                        text=text,
                        bg=colors['background'],
                        fg=status_colors.get(status, colors['text']),
                        font=('Arial', 10))
        
        return label
    
    def _darken_color(self, color: str, factor: float = 0.8) -> str:
        """Escurece uma cor hex"""
        try:
            # Remove # se presente
            color = color.lstrip('#')
            
            # Converte para RGB
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            
            # Aplica fator de escurecimento
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
            
            # Converte de volta para hex
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return color  # Retorna cor original se falhar
    
    def _lighten_color(self, color: str, factor: float = 1.2) -> str:
        """Clareia uma cor hex"""
        try:
            color = color.lstrip('#')
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            
            r = min(255, int(r * factor))
            g = min(255, int(g * factor))
            b = min(255, int(b * factor))
            
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return color
    
    def get_available_themes(self) -> Dict[str, str]:
        """Retorna lista de temas disponíveis"""
        return {name: theme['name'] for name, theme in self.themes.items()}
    
    def add_custom_theme(self, name: str, theme_config: Dict):
        """Adiciona tema personalizado"""
        self.themes[name] = theme_config
    
    def export_theme(self, theme_name: str, file_path: str) -> bool:
        """Exporta tema para arquivo JSON"""
        try:
            import json
            theme = self.get_theme(theme_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(theme, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def import_theme(self, file_path: str, theme_name: str = None) -> bool:
        """Importa tema de arquivo JSON"""
        try:
            import json
            with open(file_path, 'r', encoding='utf-8') as f:
                theme_config = json.load(f)
            
            if not theme_name:
                theme_name = theme_config.get('name', 'custom').lower().replace(' ', '_')
            
            self.add_custom_theme(theme_name, theme_config)
            return True
        except Exception:
            return False
