from typing import Any, Dict, List
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tech_monitor import get_trending_technologies


class Monitor:
    """Wraps tech_monitor functions for orchestrator use."""

    def check_trends(self, profession: str = None, min_relevance: int = 80) -> Dict[str, Any]:
        # Use existing tech_monitor.get_trending_technologies
        trending = get_trending_technologies(profession, min_relevance)
        return {'trending': trending}
