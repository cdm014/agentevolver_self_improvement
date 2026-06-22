#!/usr/bin/env python3
"""Self-Improvement Engine implementing AgentEvolver's three mechanisms."""

import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class Experience:
    """Represents a learning experience for the agent."""
    task_type: str
    task_description: str
    actions: List[str]
    outcome: str
    lessons_learned: List[str]
    timestamp: str
    metadata: Dict[str, Any]


@dataclass
class Task:
    """Represents a self-generated task for improvement."""
    task_id: str
    description: str
    difficulty: str
    category: str
    created_at: str
    completed: bool = False
    completion_time: Optional[str] = None
    score: Optional[float] = None


class SelfImprovementEngine:
    """Engine implementing AgentEvolver's self-evolving mechanisms."""

    def __init__(self, plugin_dir: Path, config: Optional[Dict[str, Any]] = None):
        self.plugin_dir = plugin_dir
        self.config = config or {}
        self.data_dir = plugin_dir / "data"
        self.experiences_file = self.data_dir / "experiences.json"
        self.tasks_file = self.data_dir / "tasks.json"
        self.stats_file = self.data_dir / "stats.json"

        self.data_dir.mkdir(exist_ok=True)

        self.experiences: List[Experience] = []
        self.tasks: List[Task] = []
        self.stats: Dict[str, Any] = {
            "total_experiences": 0,
            "total_tasks": 0,
            "tasks_completed": 0,
            "success_rate": 0.0,
            "last_updated": datetime.now().isoformat()
        }

        self._load_data()

    def _config_int(self, key: str, default: int, minimum: Optional[int] = None) -> int:
        value = self.config.get(key, default)
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            parsed = default
        if minimum is not None and parsed < minimum:
            return minimum
        return parsed

    def _load_data(self):
        """Load existing data from files."""
        if self.experiences_file.exists():
            try:
                with open(self.experiences_file, "r") as f:
                    data = json.load(f)
                    self.experiences = [Experience(**exp) for exp in data]
            except Exception as e:
                logger.error(f"Error loading experiences: {e}")
                self.experiences = []

        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, "r") as f:
                    data = json.load(f)
                    self.tasks = [Task(**task) for task in data]
            except Exception as e:
                logger.error(f"Error loading tasks: {e}")
                self.tasks = []

        if self.stats_file.exists():
            try:
                with open(self.stats_file, "r") as f:
                    self.stats = json.load(f)
            except Exception as e:
                logger.error(f"Error loading stats: {e}")

        self._update_stats()

    def _save_data(self):
        """Save data to files."""
        with open(self.experiences_file, "w") as f:
            json.dump([asdict(exp) for exp in self.experiences], f, indent=2)

        with open(self.tasks_file, "w") as f:
            json.dump([asdict(task) for task in self.tasks], f, indent=2)

        self.stats["last_updated"] = datetime.now().isoformat()
        with open(self.stats_file, "w") as f:
            json.dump(self.stats, f, indent=2)

    def _update_stats(self):
        """Update statistics based on current data."""
        self.stats["total_experiences"] = len(self.experiences)
        self.stats["total_tasks"] = len(self.tasks)
        self.stats["tasks_completed"] = len([t for t in self.tasks if t.completed])

        if self.experiences:
            successes = len([e for e in self.experiences if e.outcome == "success"])
            self.stats["success_rate"] = successes / len(self.experiences)

    def generate_task(self, category: str = "general", difficulty: str = "medium") -> Task:
        """Generate a self-improvement task (Self-Questioning)."""
        task_id = f"task_{int(time.time())}_{len(self.tasks)}"

        tasks_by_category = {
            "coding": [
                "Write a function that implements a binary search algorithm",
                "Create a simple web scraper using requests and BeautifulSoup",
                "Implement a REST API endpoint with error handling",
                "Write unit tests for an existing function",
                "Refactor code to follow PEP 8 guidelines"
            ],
            "research": [
                "Research and summarize the latest developments in AI agents",
                "Compare different vector database technologies",
                "Analyze the performance characteristics of various LLM models",
                "Research best practices for prompt engineering",
                "Study agentic workflow patterns and their applications"
            ],
            "general": [
                "Improve error handling in tool usage",
                "Optimize memory usage during long conversations",
                "Enhance the quality of response formatting",
                "Practice writing clear and concise documentation",
                "Learn a new tool or library relevant to current tasks"
            ]
        }

        descriptions = tasks_by_category.get(category, tasks_by_category["general"])
        import random
        description = random.choice(descriptions)

        if difficulty == "hard":
            description = f"Advanced: {description} with additional constraints and optimizations"
        elif difficulty == "easy":
            description = f"Beginner: {description}"

        task = Task(
            task_id=task_id,
            description=description,
            difficulty=difficulty,
            category=category,
            created_at=datetime.now().isoformat()
        )

        self.tasks.append(task)
        self._update_stats()
        self._save_data()

        logger.info(f"Generated new task: {task_id} - {description}")
        return task

    def add_experience(
        self,
        task_type: str,
        task_description: str,
        actions: List[str],
        outcome: str,
        lessons_learned: List[str],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Experience:
        """Add a learning experience (Self-Navigating)."""
        experience = Experience(
            task_type=task_type,
            task_description=task_description,
            actions=actions,
            outcome=outcome,
            lessons_learned=lessons_learned,
            timestamp=datetime.now().isoformat(),
            metadata=metadata or {}
        )

        self.experiences.append(experience)

        max_experiences = self._config_int("experience_pool_size", 1000, minimum=1)
        if len(self.experiences) > max_experiences:
            self.experiences = self.experiences[-max_experiences:]

        self._update_stats()
        self._save_data()

        logger.info(f"Added new experience: {task_type} - {outcome}")
        return experience

    def get_relevant_experiences(self, task_type: str, max_results: int = 5) -> List[Experience]:
        """Get relevant past experiences for a task type (Self-Navigating)."""
        relevant = [exp for exp in self.experiences if exp.task_type == task_type]
        relevant.sort(key=lambda x: x.timestamp, reverse=True)
        return relevant[:max_results]

    def analyze_actions(self, actions: List[str], outcomes: List[str]) -> Dict[str, float]:
        """Analyze which actions contributed to outcomes (Self-Attributing)."""
        depth = self._config_int("credit_assignment_depth", 5, minimum=1)
        action_outcome_pairs = list(zip(actions, outcomes))[-depth:]
        action_scores = {}

        for i, (action, outcome) in enumerate(action_outcome_pairs):
            if outcome == "success":
                score = 1.0
            elif outcome == "partial_success":
                score = 0.5
            else:
                score = 0.0

            discount = 0.9 ** i
            action_scores[action] = score * discount

        return action_scores

    def get_improvement_suggestions(self) -> List[str]:
        """Get suggestions for improvement based on past experiences."""
        suggestions = []

        failures = [exp for exp in self.experiences if exp.outcome == "failure"]
        if failures:
            common_lessons = set()
            for failure in failures[:3]:
                common_lessons.update(failure.lessons_learned)

            if common_lessons:
                suggestions.append(f"Focus on improving: {', '.join(list(common_lessons)[:3])}")

        task_categories = [t.category for t in self.tasks]
        from collections import Counter
        category_counts = Counter(task_categories)

        all_categories = {"coding", "research", "general"}
        for category in all_categories:
            if category_counts.get(category, 0) < 2:
                suggestions.append(f"Generate more {category} tasks for balanced learning")

        if self.stats["success_rate"] < 0.7 and self.experiences:
            suggestions.append("Consider practicing easier tasks to build confidence")

        return suggestions

    def get_stats(self) -> Dict[str, Any]:
        """Get current self-improvement statistics."""
        self._update_stats()
        return self.stats.copy()

    def complete_task(self, task_id: str, score: Optional[float] = None) -> bool:
        """Mark a task as completed."""
        for task in self.tasks:
            if task.task_id == task_id:
                task.completed = True
                task.completion_time = datetime.now().isoformat()
                if score is not None:
                    task.score = score
                self._update_stats()
                self._save_data()
                logger.info(f"Completed task: {task_id}")
                return True
        return False

    def list_tasks(self, completed_only: bool = False, pending_only: bool = False) -> List[Task]:
        """List tasks with optional filtering."""
        tasks = self.tasks
        if completed_only:
            tasks = [task for task in tasks if task.completed]
        elif pending_only:
            tasks = [task for task in tasks if not task.completed]
        return sorted(tasks, key=lambda task: task.created_at, reverse=True)
