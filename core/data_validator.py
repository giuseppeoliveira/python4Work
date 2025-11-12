"""
Sistema de Validação de Dados Profissional
Valida entrada de dados com regras customizáveis
"""

import re
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
import json

class DataValidator:
    def __init__(self, logger=None):
        self.logger = logger
        self.validation_rules = {
            'cpf': {
                'pattern': r'^\d{11}$',
                'length': 11,
                'required': True,
                'description': 'CPF deve conter exatamente 11 dígitos'
            },
            'cod_cliente': {
                'type': 'int',
                'min_value': 1,
                'max_value': 999999999,
                'required': True,
                'description': 'Código do cliente deve ser um número inteiro positivo'
            },
            'cod_acordo': {
                'type': 'int',
                'min_value': 1,
                'max_value': 999999999,
                'required': True,
                'description': 'Código do acordo deve ser um número inteiro positivo'
            },
            'email': {
                'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                'required': False,
                'description': 'Email deve ter formato válido'
            },
            'telefone': {
                'pattern': r'^\d{10,11}$',
                'required': False,
                'description': 'Telefone deve conter 10 ou 11 dígitos'
            },
            'data': {
                'type': 'date',
                'format': '%Y-%m-%d',
                'required': False,
                'description': 'Data deve estar no formato YYYY-MM-DD'
            }
        }
    
    def validate_dataframe(self, df: pd.DataFrame, required_columns: List[str], 
                          optional_columns: List[str] = None) -> Tuple[bool, List[Dict]]:
        """
        Valida DataFrame completo
        
        Returns:
            Tuple[bool, List[Dict]]: (is_valid, list_of_errors)
        """
        errors = []
        
        if self.logger:
            self.logger.log_operation_start("Validação de DataFrame", 
                                          rows=len(df), 
                                          required_cols=len(required_columns))
        
        # Verificar colunas obrigatórias
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            error = {
                'type': 'missing_columns',
                'severity': 'critical',
                'message': f'Colunas obrigatórias ausentes: {", ".join(missing_cols)}',
                'columns': missing_cols
            }
            errors.append(error)
            
            if self.logger:
                self.logger.error("Colunas obrigatórias ausentes", columns=missing_cols)
            
            return False, errors
        
        # Validar dados linha por linha
        for idx, row in df.iterrows():
            row_errors = self.validate_row(row, required_columns, idx)
            errors.extend(row_errors)
        
        # Verificar duplicatas
        duplicate_errors = self._check_duplicates(df, required_columns)
        errors.extend(duplicate_errors)
        
        is_valid = len(errors) == 0
        
        if self.logger:
            if is_valid:
                self.logger.log_operation_end("Validação de DataFrame", 
                                            result="sucesso", 
                                            errors_count=0)
            else:
                self.logger.log_operation_end("Validação de DataFrame", 
                                            result="falhou", 
                                            errors_count=len(errors))
        
        return is_valid, errors
    
    def validate_row(self, row: pd.Series, required_columns: List[str], 
                    row_index: int = None) -> List[Dict]:
        """Valida uma linha específica"""
        errors = []
        
        for column in required_columns:
            if column not in row:
                continue
            
            value = row[column]
            validation_error = self.validate_field(column, value, row_index)
            
            if validation_error:
                errors.append(validation_error)
        
        return errors
    
    def validate_field(self, field_name: str, value: Any, row_index: int = None) -> Optional[Dict]:
        """Valida um campo específico"""
        # Normalizar nome do campo
        field_type = self._normalize_field_name(field_name)
        
        if field_type not in self.validation_rules:
            return None  # Campo não tem regras de validação
        
        rules = self.validation_rules[field_type]
        
        # Verificar se é obrigatório e está vazio
        if rules.get('required', False) and (pd.isna(value) or str(value).strip() == ''):
            return {
                'type': 'required_field',
                'severity': 'error',
                'field': field_name,
                'row': row_index,
                'message': f'Campo {field_name} é obrigatório',
                'value': value,
                'rule': rules.get('description', '')
            }
        
        # Se valor está vazio e não é obrigatório, não validar
        if pd.isna(value) or str(value).strip() == '':
            return None
        
        # Validações por tipo
        if rules.get('type') == 'int':
            return self._validate_integer(field_name, value, rules, row_index)
        elif rules.get('type') == 'date':
            return self._validate_date(field_name, value, rules, row_index)
        elif 'pattern' in rules:
            return self._validate_pattern(field_name, value, rules, row_index)
        
        return None
    
    def _validate_integer(self, field_name: str, value: Any, rules: Dict, row_index: int = None) -> Optional[Dict]:
        """Valida campo inteiro"""
        try:
            int_value = int(float(str(value)))  # Converte via float para lidar com decimais
            
            if 'min_value' in rules and int_value < rules['min_value']:
                return {
                    'type': 'min_value',
                    'severity': 'error',
                    'field': field_name,
                    'row': row_index,
                    'message': f'{field_name} deve ser maior ou igual a {rules["min_value"]}',
                    'value': value,
                    'rule': rules.get('description', '')
                }
            
            if 'max_value' in rules and int_value > rules['max_value']:
                return {
                    'type': 'max_value',
                    'severity': 'error',
                    'field': field_name,
                    'row': row_index,
                    'message': f'{field_name} deve ser menor ou igual a {rules["max_value"]}',
                    'value': value,
                    'rule': rules.get('description', '')
                }
            
        except (ValueError, TypeError):
            return {
                'type': 'invalid_type',
                'severity': 'error',
                'field': field_name,
                'row': row_index,
                'message': f'{field_name} deve ser um número inteiro',
                'value': value,
                'rule': rules.get('description', '')
            }
        
        return None
    
    def _validate_date(self, field_name: str, value: Any, rules: Dict, row_index: int = None) -> Optional[Dict]:
        """Valida campo de data"""
        try:
            if isinstance(value, datetime):
                return None  # Já é uma data válida
            
            date_format = rules.get('format', '%Y-%m-%d')
            datetime.strptime(str(value), date_format)
            
        except (ValueError, TypeError):
            return {
                'type': 'invalid_date',
                'severity': 'error',
                'field': field_name,
                'row': row_index,
                'message': f'{field_name} deve estar no formato {rules.get("format", "válido")}',
                'value': value,
                'rule': rules.get('description', '')
            }
        
        return None
    
    def _validate_pattern(self, field_name: str, value: Any, rules: Dict, row_index: int = None) -> Optional[Dict]:
        """Valida campo com padrão regex"""
        pattern = rules['pattern']
        
        # Limpar valor para validação
        clean_value = re.sub(r'[^\d]', '', str(value)) if field_name.lower() in ['cpf', 'telefone'] else str(value)
        
        if not re.match(pattern, clean_value):
            return {
                'type': 'invalid_pattern',
                'severity': 'error',
                'field': field_name,
                'row': row_index,
                'message': f'{field_name} não atende ao formato esperado',
                'value': value,
                'rule': rules.get('description', '')
            }
        
        # Validação específica para CPF
        if field_name.lower() == 'cpf':
            if not self._validate_cpf(clean_value):
                return {
                    'type': 'invalid_cpf',
                    'severity': 'error',
                    'field': field_name,
                    'row': row_index,
                    'message': 'CPF inválido (dígitos verificadores incorretos)',
                    'value': value,
                    'rule': 'CPF deve ter dígitos verificadores válidos'
                }
        
        return None
    
    def validate_cpf(self, cpf: str, strict: bool = False) -> bool:
        """
        Método público para validar CPF
        Args:
            cpf (str): CPF para validar (pode conter pontos e traços)
            strict (bool): Se True, faz validação rigorosa dos dígitos verificadores
        Returns:
            bool: True se CPF é válido, False caso contrário
        """
        if not cpf:
            return False
            
        # Limpar CPF removendo pontos, traços e espaços
        clean_cpf = re.sub(r'[^\d]', '', str(cpf))
        
        # Se o CPF tem menos de 11 dígitos, preencher com zeros à esquerda
        # Isso é comum quando o Excel remove zeros iniciais
        if len(clean_cpf) < 11 and len(clean_cpf) > 0:
            clean_cpf = clean_cpf.zfill(11)
            # Log apenas se o logger estiver disponível
            if self.logger:
                self.logger.info(f"CPF '{cpf}' ajustado para: '{clean_cpf}'")
        
        # Verificar se tem exatamente 11 dígitos após ajuste
        if len(clean_cpf) != 11:
            return False
        
        # Verificar se não é uma sequência de números iguais (ex: 11111111111)
        if clean_cpf == clean_cpf[0] * 11:
            return False
        
        # Verificar se não é um CPF óbvio inválido (ex: 00000000000)
        if clean_cpf in ['00000000000', '11111111111', '22222222222', 
                        '33333333333', '44444444444', '55555555555',
                        '66666666666', '77777777777', '88888888888', '99999999999']:
            return False
        
        # Validação rigorosa apenas se solicitada
        if strict:
            return self._validate_cpf(clean_cpf)
            
        # Para processamento em lote, aceitar CPFs com formato correto
        return True  # Aceita qualquer CPF com 11 dígitos que não seja sequência repetida
    
    def normalize_cpf(self, cpf: str) -> str:
        """
        Normaliza e corrige um CPF, adicionando zeros à esquerda se necessário
        Args:
            cpf (str): CPF para normalizar
        Returns:
            str: CPF normalizado com 11 dígitos ou string vazia se inválido
        """
        if not cpf:
            return ""
            
        # Limpar CPF removendo pontos, traços e espaços
        clean_cpf = re.sub(r'[^\d]', '', str(cpf))
        
        # Se o CPF tem menos de 11 dígitos, preencher com zeros à esquerda
        if len(clean_cpf) < 11 and len(clean_cpf) > 0:
            clean_cpf = clean_cpf.zfill(11)
        
        # Verificar se tem exatamente 11 dígitos após ajuste
        if len(clean_cpf) != 11:
            return ""
        
        # Verificar se não é uma sequência de números iguais ou inválidos
        if clean_cpf == clean_cpf[0] * 11 or clean_cpf in [
            '00000000000', '11111111111', '22222222222', '33333333333', 
            '44444444444', '55555555555', '66666666666', '77777777777', 
            '88888888888', '99999999999'
        ]:
            return ""
            
        return clean_cpf
    
    def _validate_cpf(self, cpf: str) -> bool:
        """Valida dígitos verificadores do CPF"""
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        
        def calc_digit(cpf_partial):
            total = sum(int(digit) * weight for digit, weight in zip(cpf_partial, range(len(cpf_partial) + 1, 1, -1)))
            remainder = total % 11
            return '0' if remainder < 2 else str(11 - remainder)
        
        first_digit = calc_digit(cpf[:9])
        second_digit = calc_digit(cpf[:9] + first_digit)
        
        return cpf[-2:] == first_digit + second_digit
    
    def _check_duplicates(self, df: pd.DataFrame, key_columns: List[str]) -> List[Dict]:
        """Verifica registros duplicados"""
        errors = []
        
        # Verificar se todas as colunas-chave existem
        existing_keys = [col for col in key_columns if col in df.columns]
        if not existing_keys:
            return errors
        
        # Encontrar duplicatas
        duplicates = df.duplicated(subset=existing_keys, keep=False)
        if duplicates.any():
            duplicate_groups = df[duplicates].groupby(existing_keys).size()
            
            for keys, count in duplicate_groups.items():
                if not isinstance(keys, tuple):
                    keys = (keys,)
                
                key_dict = dict(zip(existing_keys, keys))
                
                errors.append({
                    'type': 'duplicate_records',
                    'severity': 'warning',
                    'message': f'Encontrados {count} registros duplicados',
                    'keys': key_dict,
                    'count': count
                })
        
        return errors
    
    def _normalize_field_name(self, field_name: str) -> str:
        """Normaliza nome do campo para busca nas regras"""
        normalized = field_name.lower().strip()
        
        # Mapeamentos específicos
        mappings = {
            'codigo_cliente': 'cod_cliente',
            'codigo_acordo': 'cod_acordo',
            'cpf_cnpj': 'cpf',
            'documento': 'cpf',
            'data_vencimento': 'data',
            'data_nascimento': 'data'
        }
        
        return mappings.get(normalized, normalized)
    
    def generate_validation_report(self, errors: List[Dict]) -> Dict:
        """Gera relatório detalhado de validação"""
        if not errors:
            return {
                'status': 'success',
                'total_errors': 0,
                'summary': 'Todos os dados estão válidos',
                'errors_by_type': {},
                'errors_by_severity': {}
            }
        
        errors_by_type = {}
        errors_by_severity = {}
        
        for error in errors:
            error_type = error.get('type', 'unknown')
            severity = error.get('severity', 'error')
            
            errors_by_type[error_type] = errors_by_type.get(error_type, 0) + 1
            errors_by_severity[severity] = errors_by_severity.get(severity, 0) + 1
        
        return {
            'status': 'error' if errors_by_severity.get('error', 0) > 0 or errors_by_severity.get('critical', 0) > 0 else 'warning',
            'total_errors': len(errors),
            'summary': f'Encontrados {len(errors)} problemas de validação',
            'errors_by_type': errors_by_type,
            'errors_by_severity': errors_by_severity,
            'details': errors
        }
    
    def add_custom_rule(self, field_name: str, rule: Dict):
        """Adiciona regra de validação customizada"""
        self.validation_rules[field_name.lower()] = rule
        
        if self.logger:
            self.logger.info(f"Regra de validação adicionada para campo: {field_name}")
    
    def export_validation_rules(self, file_path: str) -> bool:
        """Exporta regras de validação para arquivo JSON"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.validation_rules, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            if self.logger:
                self.logger.error("Erro ao exportar regras de validação", exception=e)
            return False
