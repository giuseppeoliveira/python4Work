"""
Sistema de Logging Profissional
Implementa logging estruturado com rotação e níveis configuráveis
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Optional
import json
from pathlib import Path

class LoggerProfissional:
    def __init__(self, name: str = "Python4Work", config_manager=None):
        self.name = name
        self.config = config_manager
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Evita duplicação de handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Configura handlers de logging"""
        # Criar diretório de logs
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configurações do config_manager ou padrões
        if self.config:
            log_level = self.config.get("logging.level", "INFO")
            max_size_mb = self.config.get("logging.max_file_size_mb", 10)
            backup_count = self.config.get("logging.backup_count", 5)
            log_to_console = self.config.get("logging.log_to_console", True)
            log_to_file = self.config.get("logging.log_to_file", True)
        else:
            log_level = "INFO"
            max_size_mb = 10
            backup_count = 5
            log_to_console = True
            log_to_file = True
        
        # Formato detalhado
        detailed_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(funcName)s() | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Formato simples para console
        simple_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        
        # Handler para arquivo com rotação
        if log_to_file:
            file_handler = logging.handlers.RotatingFileHandler(
                log_dir / f"{self.name.lower()}.log",
                maxBytes=max_size_mb * 1024 * 1024,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(getattr(logging, log_level.upper()))
            file_handler.setFormatter(detailed_formatter)
            self.logger.addHandler(file_handler)
        
        # Handler para console
        if log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(simple_formatter)
            self.logger.addHandler(console_handler)
        
        # Handler para erros críticos (sempre ativo)
        error_handler = logging.handlers.RotatingFileHandler(
            log_dir / f"{self.name.lower()}_errors.log",
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(error_handler)
    
    def info(self, message: str, **kwargs):
        """Log informativo"""
        self.logger.info(self._format_message(message, **kwargs))
    
    def warning(self, message: str, **kwargs):
        """Log de aviso"""
        self.logger.warning(self._format_message(message, **kwargs))
    
    def error(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """Log de erro"""
        formatted_msg = self._format_message(message, **kwargs)
        if exception:
            formatted_msg += f" | Exception: {type(exception).__name__}: {str(exception)}"
        self.logger.error(formatted_msg, exc_info=exception is not None)
    
    def debug(self, message: str, **kwargs):
        """Log de debug"""
        self.logger.debug(self._format_message(message, **kwargs))
    
    def critical(self, message: str, exception: Optional[Exception] = None, **kwargs):
        """Log crítico"""
        formatted_msg = self._format_message(message, **kwargs)
        if exception:
            formatted_msg += f" | Exception: {type(exception).__name__}: {str(exception)}"
        self.logger.critical(formatted_msg, exc_info=exception is not None)
    
    def log_operation_start(self, operation: str, **context):
        """Log início de operação"""
        self.info(f"🚀 INÍCIO: {operation}", **context)
    
    def log_operation_end(self, operation: str, duration: float = None, **context):
        """Log fim de operação"""
        duration_str = f" | Duração: {duration:.2f}s" if duration else ""
        self.info(f"✅ FIM: {operation}{duration_str}", **context)
    
    def log_operation_error(self, operation: str, exception: Exception, **context):
        """Log erro em operação"""
        self.error(f"❌ ERRO: {operation}", exception=exception, **context)
    
    def log_progress(self, current: int, total: int, operation: str = "Processamento"):
        """Log progresso de operação"""
        percentage = (current / total * 100) if total > 0 else 0
        self.info(f"📊 {operation}: {current}/{total} ({percentage:.1f}%)")
    
    def log_user_action(self, action: str, **context):
        """Log ação do usuário"""
        self.info(f"👤 USUÁRIO: {action}", **context)
    
    def log_api_call(self, url: str, method: str = "POST", status_code: int = None, **context):
        """Log chamada de API"""
        status_str = f" | Status: {status_code}" if status_code else ""
        self.info(f"🌐 API: {method} {url}{status_str}", **context)
    
    def log_file_operation(self, operation: str, file_path: str, **context):
        """Log operação de arquivo"""
        self.info(f"📁 ARQUIVO: {operation} | {file_path}", **context)
    
    def _format_message(self, message: str, **kwargs) -> str:
        """Formata mensagem com contexto adicional"""
        if kwargs:
            context_parts = []
            for key, value in kwargs.items():
                # Mascarar informações sensíveis
                if 'senha' in key.lower() or 'password' in key.lower():
                    value = '*' * len(str(value)) if value else 'None'
                context_parts.append(f"{key}={value}")
            
            if context_parts:
                message += f" | {' | '.join(context_parts)}"
        
        return message
    
    def create_session_log(self, session_id: str):
        """Cria log específico para uma sessão"""
        return SessionLogger(self, session_id)

class SessionLogger:
    """Logger específico para uma sessão de trabalho"""
    
    def __init__(self, parent_logger: 'LoggerProfissional', session_id: str):
        self.parent = parent_logger
        self.session_id = session_id
        self.start_time = datetime.now()
        self.operations = []
        
        self.parent.info(f"🎯 SESSÃO INICIADA: {session_id}")
    
    def log_operation(self, operation: str, status: str = "success", **context):
        """Log operação na sessão"""
        self.operations.append({
            "operation": operation,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "context": context
        })
        
        status_emoji = "✅" if status == "success" else "❌" if status == "error" else "⚠️"
        self.parent.info(f"{status_emoji} [{self.session_id}] {operation}", **context)
    
    def finalize_session(self, summary: dict = None):
        """Finaliza sessão com resumo"""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        summary_data = {
            "session_id": self.session_id,
            "duration_seconds": duration,
            "operations_count": len(self.operations),
            "operations": self.operations,
            "custom_summary": summary or {}
        }
        
        # Salvar resumo da sessão
        session_dir = Path("logs/sessions")
        session_dir.mkdir(exist_ok=True)
        
        session_file = session_dir / f"session_{self.session_id}_{self.start_time.strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            self.parent.error("Erro ao salvar resumo da sessão", exception=e)
        
        self.parent.info(f"🏁 SESSÃO FINALIZADA: {self.session_id} | Duração: {duration:.2f}s | Operações: {len(self.operations)}")
        
        return summary_data
