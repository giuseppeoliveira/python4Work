"""
NoLog Core - Módulo principal para prevenção de logout automático
"""
import ctypes
import time
import json
import winsound
from pathlib import Path
from typing import Dict, Any
import pyautogui


class NoLogCore:
    """Classe principal para gerenciar a prevenção de logout"""
    
    # Constantes do Windows para prevenir suspensão
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    ES_DISPLAY_REQUIRED = 0x00000002
    ES_AWAYMODE_REQUIRED = 0x00000040
    
    def __init__(self, config_path: str = "config.json"):
        """
        Inicializa o NoLogCore
        
        Args:
            config_path: Caminho para o arquivo de configuração
        """
        self.config = self._load_config(config_path)
        self.running = False
        self.total_actions = 0
        
        # Configurações de segurança do pyautogui
        pyautogui.FAILSAFE = True  # Mover mouse para canto superior esquerdo para parar
        pyautogui.PAUSE = 0.1
    
    def play_sound(self, sound_type: str):
        """
        Toca um som de notificação
        
        Args:
            sound_type: 'start' para iniciar, 'stop' para parar
        """
        # Verifica se o som está habilitado na configuração
        if not self.config.get('sound_enabled', True):
            return
            
        try:
            if sound_type == 'start':
                # Som de sucesso/início (frequência 800Hz, 200ms)
                winsound.Beep(800, 200)
                time.sleep(0.05)
                winsound.Beep(1000, 150)
            elif sound_type == 'stop':
                # Som de parada (frequência 600Hz, 200ms)
                winsound.Beep(600, 200)
        except Exception as e:
            # Se falhar, não interrompe o funcionamento
            pass
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Carrega configurações do arquivo JSON"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Configurações padrão (sempre usar se não encontrar arquivo)
            return {
                "interval_seconds": 60,
                "mouse_movement": True,
                "key_press": True,
                "prevent_sleep": True,
                "movement_distance": 1,
                "sound_enabled": True
            }
    
    def prevent_sleep_mode(self, enable: bool = True):
        """
        Previne que o Windows entre em modo de suspensão
        Funciona sem privilégios de administrador
        
        Args:
            enable: True para ativar prevenção, False para desativar
        """
        if not self.config.get("prevent_sleep", True):
            return
        
        try:
            if enable:
                # Previne suspensão do sistema e da tela
                ctypes.windll.kernel32.SetThreadExecutionState(
                    self.ES_CONTINUOUS | 
                    self.ES_SYSTEM_REQUIRED | 
                    self.ES_DISPLAY_REQUIRED
                )
            else:
                # Restaura comportamento normal
                ctypes.windll.kernel32.SetThreadExecutionState(
                    self.ES_CONTINUOUS
                )
        except Exception as e:
            # Se falhar (falta de permissões), continua sem essa funcionalidade
            print(f"Aviso: Não foi possível prevenir suspensão: {e}")
            print("A aplicação continuará funcionando normalmente.")
    
    def simulate_activity(self):
        """Simula atividade do usuário"""
        try:
            # Movimento de mouse sutil
            if self.config.get("mouse_movement", True):
                current_x, current_y = pyautogui.position()
                distance = self.config.get("movement_distance", 1)
                
                # Move o mouse sutilmente e volta
                pyautogui.moveRel(distance, distance, duration=0.1)
                pyautogui.moveRel(-distance, -distance, duration=0.1)
            
            # Pressiona tecla Shift (não imprime nada)
            if self.config.get("key_press", True):
                pyautogui.press('shift')
            
            self.total_actions += 1
            return True
            
        except Exception as e:
            print(f"Erro ao simular atividade: {e}")
            return False
    
    def start(self, callback=None):
        """
        Inicia o loop de prevenção de logout
        
        Args:
            callback: Função opcional para chamar a cada iteração
        """
        self.running = True
        self.prevent_sleep_mode(True)
        
        # Toca som de início
        self.play_sound('start')
        
        print("🟢 NoLog iniciado!")
        print(f"⏱️  Intervalo: {self.config['interval_seconds']} segundos")
        print("💡 Pressione Ctrl+C ou mova o mouse para o canto superior esquerdo para parar\n")
        
        try:
            while self.running:
                success = self.simulate_activity()
                
                if callback:
                    callback(success, self.total_actions)
                
                time.sleep(self.config['interval_seconds'])
                
        except KeyboardInterrupt:
            print("\n⚠️  Interrompido pelo usuário")
        except pyautogui.FailSafeException:
            print("\n⚠️  Failsafe ativado - mouse movido para canto da tela")
        finally:
            self.stop()
    
    def stop(self):
        """Para o serviço de prevenção"""
        self.running = False
        self.prevent_sleep_mode(False)
        
        # Toca som de parada
        self.play_sound('stop')
        
        print(f"\n🔴 NoLog parado!")
        print(f"📊 Total de ações executadas: {self.total_actions}")
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna o status atual do serviço"""
        return {
            "running": self.running,
            "total_actions": self.total_actions,
            "config": self.config
        }


if __name__ == "__main__":
    # Teste básico
    nolog = NoLogCore()
    nolog.start()
