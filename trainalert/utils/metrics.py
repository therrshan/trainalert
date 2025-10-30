"""Metric tracking and storage utilities."""
from typing import Dict, List, Any, Optional
from datetime import datetime
import time


class MetricTracker:
    """Tracks training metrics over time."""
    
    def __init__(self):
        self.metrics: Dict[str, List[float]] = {}
        self.epochs: List[int] = []
        self.timestamps: List[float] = []
        self.start_time = time.time()
        self.best_metrics: Dict[str, Dict[str, Any]] = {}
        
    def log(self, metric_name: str, value: float, epoch: Optional[int] = None):
        """
        Log a metric value.
        
        Args:
            metric_name: Name of the metric
            value: Metric value
            epoch: Optional epoch number
        """
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        
        self.metrics[metric_name].append(value)
        self.timestamps.append(time.time())
        
        if epoch is not None and epoch not in self.epochs:
            self.epochs.append(epoch)
        
        # Track best metrics
        self._update_best_metric(metric_name, value, epoch)
    
    def _update_best_metric(self, metric_name: str, value: float, epoch: Optional[int]):
        """Update best metric tracking."""
        if metric_name not in self.best_metrics:
            self.best_metrics[metric_name] = {
                'value': value,
                'epoch': epoch,
                'improved': True
            }
            return
        
        # Assume lower is better for loss, higher is better for accuracy/precision/etc
        is_loss = 'loss' in metric_name.lower() or 'error' in metric_name.lower()
        
        current_best = self.best_metrics[metric_name]['value']
        improved = value < current_best if is_loss else value > current_best
        
        if improved:
            self.best_metrics[metric_name] = {
                'value': value,
                'epoch': epoch,
                'improved': True
            }
        else:
            self.best_metrics[metric_name]['improved'] = False
    
    def get_latest(self, metric_name: str) -> Optional[float]:
        """Get latest value for a metric."""
        if metric_name in self.metrics and self.metrics[metric_name]:
            return self.metrics[metric_name][-1]
        return None
    
    def get_all(self, metric_name: str) -> List[float]:
        """Get all values for a metric."""
        return self.metrics.get(metric_name, [])
    
    def get_best(self, metric_name: str) -> Optional[Dict[str, Any]]:
        """Get best value for a metric."""
        return self.best_metrics.get(metric_name)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics."""
        elapsed_time = time.time() - self.start_time
        
        summary = {
            'total_metrics': len(self.metrics),
            'total_epochs': len(self.epochs),
            'elapsed_time': elapsed_time,
            'elapsed_time_formatted': self._format_time(elapsed_time),
            'metrics': {}
        }
        
        for metric_name, values in self.metrics.items():
            if not values:
                continue
                
            summary['metrics'][metric_name] = {
                'latest': values[-1],
                'best': self.best_metrics.get(metric_name, {}).get('value'),
                'best_epoch': self.best_metrics.get(metric_name, {}).get('epoch'),
                'count': len(values)
            }
        
        return summary
    
    def check_improvement(self, metric_name: str) -> bool:
        """Check if metric improved on last update."""
        if metric_name in self.best_metrics:
            return self.best_metrics[metric_name].get('improved', False)
        return False
    
    @staticmethod
    def _format_time(seconds: float) -> str:
        """Format seconds into human-readable string."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"