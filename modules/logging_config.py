#!/usr/bin/env python3
"""
Centralized Logging Configuration
Provides consistent logging across all modules with detailed operation tracking
"""

import logging
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import sys

class DetailedFormatter(logging.Formatter):
    """Enhanced formatter with operation context"""
    
    def format(self, record):
        # Add timestamp
        record.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        # Add module context
        if hasattr(record, 'module_context'):
            record.context = f"[{record.module_context}]"
        else:
            record.context = f"[{record.name}]"
        
        # Add operation type
        if hasattr(record, 'operation'):
            record.op = f"→{record.operation}"
        else:
            record.op = ""
        
        # Format: TIMESTAMP [MODULE]→OPERATION LEVEL: MESSAGE
        format_str = "%(timestamp)s %(context)s%(op)s %(levelname)s: %(message)s"
        formatter = logging.Formatter(format_str)
        return formatter.format(record)

class OperationLogger:
    """Enhanced logger for detailed operation tracking"""
    
    def __init__(self, name: str, module_context: str = None):
        self.logger = logging.getLogger(name)
        self.module_context = module_context or name
        self.operation_stack = []
        self.metrics = {
            'operations_count': 0,
            'errors_count': 0,
            'warnings_count': 0,
            'start_time': datetime.now(),
            'operations_log': []
        }
    
    # Delegate standard logging methods to the underlying logger
    def info(self, message, *args, **kwargs):
        """Standard info logging"""
        return self.logger.info(message, *args, **kwargs)
    
    def error(self, message, *args, **kwargs):
        """Standard error logging"""
        self.metrics['errors_count'] += 1
        return self.logger.error(message, *args, **kwargs)
    
    def warning(self, message, *args, **kwargs):
        """Standard warning logging"""
        self.metrics['warnings_count'] += 1
        return self.logger.warning(message, *args, **kwargs)
    
    def debug(self, message, *args, **kwargs):
        """Standard debug logging"""
        return self.logger.debug(message, *args, **kwargs)
    
    def start_operation(self, operation: str, **kwargs):
        """Start tracking an operation"""
        self.operation_stack.append({
            'name': operation,
            'start_time': datetime.now(),
            'details': kwargs
        })
        self.metrics['operations_count'] += 1
        
        extra = {
            'module_context': self.module_context,
            'operation': operation
        }
        
        details_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()]) if kwargs else ""
        message = f"Starting operation: {operation}"
        if details_str:
            message += f" ({details_str})"
            
        self.logger.info(message, extra=extra)
        return operation
    
    def end_operation(self, operation: str, success: bool = True, **kwargs):
        """End tracking an operation"""
        end_time = datetime.now()
        
        # Find and remove operation from stack
        op_data = None
        for i, op in enumerate(self.operation_stack):
            if op['name'] == operation:
                op_data = self.operation_stack.pop(i)
                break
        
        if op_data:
            duration = (end_time - op_data['start_time']).total_seconds()
        else:
            duration = 0
        
        extra = {
            'module_context': self.module_context,
            'operation': operation
        }
        
        status = "✅ SUCCESS" if success else "❌ FAILED"
        details_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()]) if kwargs else ""
        message = f"Completed operation: {operation} [{status}] ({duration:.3f}s)"
        if details_str:
            message += f" - {details_str}"
        
        # Log operation completion
        self.metrics['operations_log'].append({
            'operation': operation,
            'success': success,
            'duration_seconds': duration,
            'timestamp': end_time.isoformat(),
            'details': kwargs
        })
        
        if success:
            self.logger.info(message, extra=extra)
        else:
            self.logger.error(message, extra=extra)
            self.metrics['errors_count'] += 1
    
    def log_validation(self, validation_type: str, result: Dict[str, Any], **kwargs):
        """Log validation results in detail"""
        extra = {
            'module_context': self.module_context,
            'operation': f"validate_{validation_type}"
        }
        
        is_valid = result.get('is_valid', result.get('is_authentic', False))
        status = "✅ PASS" if is_valid else "❌ FAIL"
        
        message = f"Validation {validation_type}: {status}"
        
        # Add details
        details = []
        if 'issues' in result and result['issues']:
            details.append(f"Issues: {len(result['issues'])}")
        if 'suggestions' in result and result['suggestions']:
            details.append(f"Suggestions: {len(result['suggestions'])}")
        if 'word_count' in result:
            details.append(f"Words: {result['word_count']}")
        if 'char_count' in result:
            details.append(f"Chars: {result['char_count']}")
        
        if details:
            message += f" ({', '.join(details)})"
        
        # Log detailed issues/suggestions at debug level
        if result.get('issues'):
            self.logger.debug(f"Validation issues for {validation_type}: {result['issues']}", extra=extra)
        if result.get('suggestions'):
            self.logger.debug(f"Validation suggestions for {validation_type}: {result['suggestions']}", extra=extra)
        
        if is_valid:
            self.logger.info(message, extra=extra)
        else:
            self.logger.warning(message, extra=extra)
            self.metrics['warnings_count'] += 1
    
    def log_metric(self, metric_name: str, value: Any, **kwargs):
        """Log performance or business metrics"""
        extra = {
            'module_context': self.module_context,
            'operation': f"metric_{metric_name}"
        }
        
        details_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()]) if kwargs else ""
        message = f"📊 {metric_name}: {value}"
        if details_str:
            message += f" ({details_str})"
        
        self.logger.info(message, extra=extra)
    
    def log_data_extraction(self, source: str, data_type: str, count: int, **kwargs):
        """Log data extraction operations"""
        extra = {
            'module_context': self.module_context,
            'operation': f"extract_{data_type}"
        }
        
        message = f"📄 Extracted {data_type} from {source}: {count} items"
        if kwargs:
            details = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
            message += f" ({details})"
        
        self.logger.info(message, extra=extra)
    
    def log_generation(self, content_type: str, model: str, tokens: int, cost: float, **kwargs):
        """Log LLM generation operations"""
        extra = {
            'module_context': self.module_context,
            'operation': f"generate_{content_type}"
        }
        
        message = f"🤖 Generated {content_type} using {model}: {tokens} tokens, ${cost:.4f}"
        if kwargs:
            details = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
            message += f" ({details})"
        
        self.logger.info(message, extra=extra)
    
    def log_file_operation(self, operation: str, file_path: str, size_bytes: int = None, **kwargs):
        """Log file operations"""
        extra = {
            'module_context': self.module_context,
            'operation': f"file_{operation}"
        }
        
        message = f"📁 {operation.capitalize()} file: {file_path}"
        if size_bytes is not None:
            size_kb = size_bytes / 1024
            message += f" ({size_kb:.1f}KB)"
        
        if kwargs:
            details = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
            message += f" - {details}"
        
        self.logger.info(message, extra=extra)
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get operation metrics summary"""
        duration = (datetime.now() - self.metrics['start_time']).total_seconds()
        
        return {
            'module': self.module_context,
            'total_operations': self.metrics['operations_count'],
            'errors_count': self.metrics['errors_count'],
            'warnings_count': self.metrics['warnings_count'],
            'total_duration_seconds': duration,
            'operations_per_second': self.metrics['operations_count'] / duration if duration > 0 else 0,
            'error_rate': self.metrics['errors_count'] / max(self.metrics['operations_count'], 1),
            'recent_operations': self.metrics['operations_log'][-10:]  # Last 10 operations
        }

def setup_logging(log_level: str = "INFO", log_file: str = None, console_output: bool = True) -> None:
    """Setup centralized logging configuration"""
    
    # Convert string level to logging constant
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Clear any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Setup console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(DetailedFormatter())
        root_logger.addHandler(console_handler)
    
    # Setup file handler if specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(DetailedFormatter())
        root_logger.addHandler(file_handler)

def get_logger(name: str, module_context: str = None) -> OperationLogger:
    """Get an enhanced logger instance"""
    return OperationLogger(name, module_context)

# Setup default logging
def initialize_application_logging():
    """Initialize logging for the entire application"""
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Create timestamped log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"aply_application_{timestamp}.log"
    
    # Setup with INFO level and both console/file output
    setup_logging(
        log_level="INFO",
        log_file=str(log_file),
        console_output=True
    )
    
    # Log startup
    logger = get_logger(__name__, "logging_config")
    logger.start_operation("application_startup")
    logger.log_metric("log_file_created", str(log_file))
    logger.end_operation("application_startup", success=True)
    
    return str(log_file)

# Auto-initialize when imported
if __name__ != "__main__":
    initialize_application_logging()