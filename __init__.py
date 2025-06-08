"""
LeetCode AI Assistant - A CrewAI-powered screenshot analysis tool for LeetCode problems

This package provides an AI-powered assistant that can analyze screenshots of LeetCode problems
and provide comprehensive solutions, explanations, and coding guidance.
"""

from .main import main
from .crew_manager import LeetCodeCrewManager
from .config import Config

__version__ = "1.0.0"
__author__ = "LeetCode AI Assistant"
__description__ = "AI-powered LeetCode problem analysis tool"

# Make main function available at package level
__all__ = ["main", "LeetCodeCrewManager", "Config"] 