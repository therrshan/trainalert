"""System information utilities (GPU, CPU, memory)."""
import platform
from typing import Dict, List, Any, Optional

try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class SystemInfo:
    """Collects system information for training context."""
    
    @staticmethod
    def get_gpu_info() -> List[Dict[str, Any]]:
        """
        Get GPU information.
        
        Returns:
            List of GPU information dictionaries
        """
        if not GPU_AVAILABLE:
            return []
        
        try:
            gpus = GPUtil.getGPUs()
            gpu_info = []
            
            for gpu in gpus:
                gpu_info.append({
                    'id': gpu.id,
                    'name': gpu.name,
                    'memory_total': f"{gpu.memoryTotal} MB",
                    'memory_used': f"{gpu.memoryUsed} MB",
                    'memory_free': f"{gpu.memoryFree} MB",
                    'memory_util': f"{gpu.memoryUtil * 100:.1f}%",
                    'gpu_util': f"{gpu.load * 100:.1f}%",
                    'temperature': f"{gpu.temperature}°C" if gpu.temperature else "N/A"
                })
            
            return gpu_info
        except Exception as e:
            return [{'error': str(e)}]
    
    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        """
        Get CPU information.
        
        Returns:
            Dictionary with CPU information
        """
        cpu_info = {
            'processor': platform.processor(),
            'architecture': platform.machine(),
        }
        
        if PSUTIL_AVAILABLE:
            try:
                cpu_info['cpu_count'] = psutil.cpu_count(logical=False)
                cpu_info['cpu_count_logical'] = psutil.cpu_count(logical=True)
                cpu_info['cpu_percent'] = f"{psutil.cpu_percent(interval=1)}%"
            except Exception:
                pass
        
        return cpu_info
    
    @staticmethod
    def get_memory_info() -> Dict[str, Any]:
        """
        Get memory information.
        
        Returns:
            Dictionary with memory information
        """
        if not PSUTIL_AVAILABLE:
            return {}
        
        try:
            mem = psutil.virtual_memory()
            return {
                'total': f"{mem.total / (1024**3):.2f} GB",
                'available': f"{mem.available / (1024**3):.2f} GB",
                'used': f"{mem.used / (1024**3):.2f} GB",
                'percent': f"{mem.percent}%"
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def get_system_summary() -> Dict[str, Any]:
        """
        Get complete system summary.
        
        Returns:
            Dictionary with all system information
        """
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'python_version': platform.python_version(),
            'cpu': SystemInfo.get_cpu_info(),
            'memory': SystemInfo.get_memory_info(),
            'gpu': SystemInfo.get_gpu_info()
        }
    
    @staticmethod
    def format_system_info(include_gpu: bool = True) -> str:
        """
        Format system information as readable string.
        
        Args:
            include_gpu: Whether to include GPU information
        
        Returns:
            Formatted system information string
        """
        info = SystemInfo.get_system_summary()
        
        lines = [
            "System Information:",
            f"  Platform: {info['platform']} ({info['python_version']})",
        ]
        
        # CPU info
        cpu = info.get('cpu', {})
        if cpu:
            lines.append(f"  CPU: {cpu.get('processor', 'Unknown')}")
            if 'cpu_count' in cpu:
                lines.append(f"  CPU Cores: {cpu['cpu_count']} physical, {cpu['cpu_count_logical']} logical")
            if 'cpu_percent' in cpu:
                lines.append(f"  CPU Usage: {cpu['cpu_percent']}")
        
        # Memory info
        mem = info.get('memory', {})
        if mem and 'total' in mem:
            lines.append(f"  Memory: {mem['used']} / {mem['total']} ({mem['percent']})")
        
        # GPU info
        if include_gpu:
            gpus = info.get('gpu', [])
            if gpus and not ('error' in gpus[0]):
                lines.append(f"  GPUs: {len(gpus)}")
                for i, gpu in enumerate(gpus):
                    lines.append(f"    GPU {i}: {gpu['name']}")
                    lines.append(f"      Memory: {gpu['memory_used']} / {gpu['memory_total']} ({gpu['memory_util']})")
                    lines.append(f"      Utilization: {gpu['gpu_util']}")
            elif not gpus:
                lines.append("  GPUs: None detected")
        
        return "\n".join(lines)