import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from ..telemetry.monitor import HardwareMonitor
from ..telemetry.models import HardwareState
from .models import PriorityLevel, ComputeQuota, ThrottlingDecision

class ResourceGovernor:
    """
    Manages compute quotas and enforces resource limits based on hardware telemetry.
    """
    def __init__(self, monitor: HardwareMonitor):
        self.monitor = monitor
        # Thresholds
        self.max_cpu_percent = 90.0
        self.max_memory_percent = 85.0
        self.max_gpu_memory_percent = 90.0
        self.max_gpu_temp_c = 80.0
        
        # State
        self.active_tasks: Dict[str, ComputeQuota] = {}

    def check_resources(self, priority: PriorityLevel) -> ThrottlingDecision:
        """
        Determines if a new task should be allowed to start based on current system load.
        """
        state = self.monitor.get_latest_state()
        if not state:
            # If no state is available yet, assume safe but caution
            return ThrottlingDecision(should_throttle=False)

        # Thermal Throttling (Highest Priority Check)
        for gpu in state.gpus:
            if gpu.temperature >= self.max_gpu_temp_c:
                return ThrottlingDecision(
                    should_throttle=True,
                    reason=f"Thermal Throttling: GPU {gpu.id} at {gpu.temperature}C",
                    suggested_wait_time=5.0
                )

        # Memory Pressure
        if state.memory.percent >= self.max_memory_percent:
            if priority in [PriorityLevel.LOW, PriorityLevel.IDLE]:
                 return ThrottlingDecision(
                    should_throttle=True,
                    reason=f"Memory Pressure: {state.memory.percent}% used",
                    suggested_wait_time=2.0
                )

        # VRAM Pressure
        for gpu in state.gpus:
             # Calculate percentage since we only have raw values
            if gpu.memory_total > 0:
                vram_percent = (gpu.memory_used / gpu.memory_total) * 100
                if vram_percent >= self.max_gpu_memory_percent:
                     if priority != PriorityLevel.CRITICAL:
                        return ThrottlingDecision(
                            should_throttle=True,
                            reason=f"VRAM Pressure: GPU {gpu.id} at {vram_percent:.1f}%",
                            suggested_wait_time=1.0
                        )

        return ThrottlingDecision(should_throttle=False)

    def allocate_resources(self, task_id: str, quota: ComputeQuota) -> bool:
        """
        Allocates resources for a task. Returns True if successful.
        """
        # In a real implementation, this would reserve resources.
        # For now, we just track the allocation.
        self.active_tasks[task_id] = quota
        return True

    def release_resources(self, task_id: str):
        """
        Releases resources for a task.
        """
        if task_id in self.active_tasks:
            del self.active_tasks[task_id]
