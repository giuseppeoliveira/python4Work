"""
Sistema de Configuração Profissional
Permite personalizar comportamentos da aplicação via arquivo JSON
"""

import json
import os
from typing import Dict, Any
from datetime import datetime

class ConfigManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.default_config = {
            "app": {
                "name": "Python4Work Professional",
                "version": "2.0.0",
                "theme": "modern",
                "language": "pt_BR",
                "auto_backup": True,
                "backup_interval": 10,  # linhas
                "max_retries": 3,
                "timeout_seconds": 30
            },
            "ui": {
                "window_width": 1000,
                "window_height": 700,
                "show_tooltips": True,
                "show_progress_details": True,
                "animate_progress": True,
                "confirm_exit": True
            },
            "logging": {
                "level": "INFO",
                "max_file_size_mb": 10,
                "backup_count": 5,
                "log_to_console": True,
                "log_to_file": True,
                "detailed_errors": True
            },
            "security": {
                "mask_credentials": True,
                "require_env_file": True,
                "validate_ssl": True,
                "session_timeout": 3600
            },
            "performance": {
                "batch_size": 100,
                "thread_pool_size": 4,
                "memory_limit_mb": 512,
                "enable_caching": True
            }
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Carrega configurações do arquivo ou cria com padrões"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Mescla com configurações padrão para garantir completude
                    return self._merge_configs(self.default_config, config)
            except Exception as e:
                print(f"Erro ao carregar config: {e}. Usando padrões.")
        
        # Cria arquivo de configuração padrão
        self.save_config(self.default_config)
        return self.default_config.copy()
    
    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """Salva configurações no arquivo"""
        try:
            config_to_save = config or self.config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar config: {e}")
            return False
    
    def get(self, path: str, default=None):
        """Obtém valor de configuração usando notação de ponto (ex: 'app.theme')"""
        keys = path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def set(self, path: str, value: Any) -> bool:
        """Define valor de configuração usando notação de ponto"""
        keys = path.split('.')
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
        return self.save_config()
    
    def _merge_configs(self, default: Dict, custom: Dict) -> Dict:
        """Mescla configurações personalizadas com padrões"""
        result = default.copy()
        for key, value in custom.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def reset_to_defaults(self) -> bool:
        """Restaura configurações padrão"""
        self.config = self.default_config.copy()
        return self.save_config()
    
    def export_config(self, file_path: str) -> bool:
        """Exporta configurações para arquivo específico"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def import_config(self, file_path: str) -> bool:
        """Importa configurações de arquivo específico"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                new_config = json.load(f)
                self.config = self._merge_configs(self.default_config, new_config)
                return self.save_config()
        except Exception:
            return False
