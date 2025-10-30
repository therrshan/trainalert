"""Plot generation for training metrics."""
import io
from typing import Dict, List, Optional
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np


class PlotGenerator:
    """Generates plots for training metrics."""
    
    @staticmethod
    def create_metric_plot(
        metric_name: str,
        values: List[float],
        epochs: Optional[List[int]] = None,
        figsize: tuple = (10, 6)
    ) -> io.BytesIO:
        """
        Create a plot for a single metric.
        
        Args:
            metric_name: Name of the metric
            values: List of metric values
            epochs: Optional list of epoch numbers
            figsize: Figure size tuple
        
        Returns:
            BytesIO object containing the plot image
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        x_axis = epochs if epochs else list(range(len(values)))
        
        ax.plot(x_axis, values, marker='o', linewidth=2, markersize=4)
        ax.set_xlabel('Epoch' if epochs else 'Step', fontsize=12)
        ax.set_ylabel(metric_name.replace('_', ' ').title(), fontsize=12)
        ax.set_title(f'{metric_name.replace("_", " ").title()} Over Time', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add value annotations for first, last, and best points
        if values:
            # First point
            ax.annotate(f'{values[0]:.4f}',
                       xy=(x_axis[0], values[0]),
                       xytext=(10, 10),
                       textcoords='offset points',
                       fontsize=8,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.5))
            
            # Last point
            ax.annotate(f'{values[-1]:.4f}',
                       xy=(x_axis[-1], values[-1]),
                       xytext=(10, -15),
                       textcoords='offset points',
                       fontsize=8,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.5))
            
            # Best point
            is_loss = 'loss' in metric_name.lower()
            best_idx = np.argmin(values) if is_loss else np.argmax(values)
            ax.annotate(f'Best: {values[best_idx]:.4f}',
                       xy=(x_axis[best_idx], values[best_idx]),
                       xytext=(10, 10),
                       textcoords='offset points',
                       fontsize=8,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7),
                       arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        plt.tight_layout()
        
        # Save to BytesIO
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        
        return buf
    
    @staticmethod
    def create_multi_metric_plot(
        metrics_dict: Dict[str, List[float]],
        epochs: Optional[List[int]] = None,
        figsize: tuple = (12, 8)
    ) -> io.BytesIO:
        """
        Create subplots for multiple metrics.
        
        Args:
            metrics_dict: Dictionary of metric names to value lists
            epochs: Optional list of epoch numbers
            figsize: Figure size tuple
        
        Returns:
            BytesIO object containing the plot image
        """
        n_metrics = len(metrics_dict)
        if n_metrics == 0:
            return None
        
        # Determine subplot layout
        cols = min(2, n_metrics)
        rows = (n_metrics + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=figsize)
        if n_metrics == 1:
            axes = [axes]
        else:
            axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]
        
        for idx, (metric_name, values) in enumerate(metrics_dict.items()):
            if idx >= len(axes):
                break
                
            ax = axes[idx]
            x_axis = epochs if epochs else list(range(len(values)))
            
            ax.plot(x_axis, values, marker='o', linewidth=2, markersize=3)
            ax.set_xlabel('Epoch' if epochs else 'Step', fontsize=10)
            ax.set_ylabel(metric_name.replace('_', ' ').title(), fontsize=10)
            ax.set_title(metric_name.replace('_', ' ').title(), fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            # Add latest value annotation
            if values:
                ax.annotate(f'{values[-1]:.4f}',
                           xy=(x_axis[-1], values[-1]),
                           xytext=(5, 5),
                           textcoords='offset points',
                           fontsize=8,
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.5))
        
        # Hide extra subplots
        for idx in range(n_metrics, len(axes)):
            axes[idx].set_visible(False)
        
        plt.suptitle('Training Metrics Overview', fontsize=14, fontweight='bold', y=1.00)
        plt.tight_layout()
        
        # Save to BytesIO
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        
        return buf
    
    @staticmethod
    def create_comparison_plot(
        train_values: List[float],
        val_values: List[float],
        metric_name: str,
        epochs: Optional[List[int]] = None,
        figsize: tuple = (10, 6)
    ) -> io.BytesIO:
        """
        Create a comparison plot for training vs validation metrics.
        
        Args:
            train_values: Training metric values
            val_values: Validation metric values
            metric_name: Name of the metric
            epochs: Optional list of epoch numbers
            figsize: Figure size tuple
        
        Returns:
            BytesIO object containing the plot image
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        x_axis = epochs if epochs else list(range(len(train_values)))
        
        ax.plot(x_axis, train_values, marker='o', linewidth=2, markersize=4, label='Train', color='blue')
        ax.plot(x_axis, val_values, marker='s', linewidth=2, markersize=4, label='Validation', color='orange')
        
        ax.set_xlabel('Epoch' if epochs else 'Step', fontsize=12)
        ax.set_ylabel(metric_name.replace('_', ' ').title(), fontsize=12)
        ax.set_title(f'{metric_name.replace("_", " ").title()} - Train vs Validation', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=11)
        
        plt.tight_layout()
        
        # Save to BytesIO
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)
        
        return buf