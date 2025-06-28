from __future__ import annotations
import os
import yaml
import importlib
import pkgutil
from typing import Type, Dict

from pydantic.v1.typing import get_class

from extract.extract_result import ExtractResult
from text_extract_api.files.file_formats.file_format import FileFormat

class Strategy:
    _strategies: Dict[str, Strategy] = {}
    _strategy_config: Dict[str, Dict] = {}

    def __init__(self):
        self.update_state_callback = None
        self._strategy_config = None

    def set_strategy_config(self, config: Dict):
        self._strategy_config = config

    def set_update_state_callback(self, callback):
        self.update_state_callback = callback

    def update_state(self, state, meta):
        if self.update_state_callback:
            self.update_state_callback(state, meta)

    @classmethod
    def name(cls) -> str:
        raise NotImplementedError("Strategy subclasses must implement name")

    @classmethod
    def extract_text(cls, file_format: Type["FileFormat"], language: str = 'en') -> ExtractResult:
        raise NotImplementedError("Strategy subclasses must implement extract_text method")

    @classmethod
    def get_strategy(cls, name: str) -> Type["Strategy"]:
        """
        Fetches and returns a registered strategy class based on the given name.

        Args:
            name: The name of the strategy to fetch.

        Returns:
            The strategy class corresponding to the provided name.

        Raises:
            ValueError: If the specified strategy name does not exist among the registered strategies.
        """
        # Normalize strategy name to lowercase
        name = name.lower().strip()

        if name not in cls._strategies:
            cls.load_strategies_from_config()

        if name not in cls._strategies:
            cls.autodiscover_strategies()

        if name not in cls._strategies:
            available = ', '.join(cls._strategies.keys())
            raise ValueError(f"Unknown strategy '{name}'. Available: {available}")

        return cls._strategies[name]

    @classmethod
    def register_strategy(cls, strategy, name: str = None, override: bool = False):
        # Handle both strategy instances and strategy classes
        if isinstance(strategy, type):
            # It's a class
            strategy_name = name or strategy.name()
            strategy_instance = strategy()
        else:
            # It's already an instance
            strategy_instance = strategy
            strategy_name = name or strategy_instance.name()
        
        # Normalize strategy name to lowercase to avoid duplicates
        strategy_name = strategy_name.lower()
            
        if override or strategy_name not in cls._strategies:
            cls._strategies[strategy_name] = strategy_instance
        else:
            print(f"Strategy '{strategy_name}' already registered, skipping duplicate")

    @classmethod
    def load_strategies_from_config(cls, path: str = os.getenv('OCR_CONFIG_PATH', 'config/strategies.yaml')):
        strategies = cls._strategies
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(path)))
        config_file_path = os.path.join(project_root, path)

        if not os.path.isfile(config_file_path):
            raise FileNotFoundError(f"Config file not found at path: {config_file_path}")

        with open(config_file_path, 'r') as f:
            config = yaml.safe_load(f)

        if 'strategies' not in config or not isinstance(config['strategies'], dict):
            raise ValueError(f"Missing or invalid 'strategies' section in the {config_file_path} file")

        for strategy_name, strategy_config in config['strategies'].items():
            if 'class' not in strategy_config:
                raise ValueError(f"Missing 'class' attribute for OCR strategy: {strategy_name}")

            strategy_class_path = strategy_config['class']
            module_path, class_name = strategy_class_path.rsplit('.', 1)
            module = importlib.import_module(module_path)

            strategy = getattr(module, class_name)
            strategy_instance = strategy()
            strategy_instance.set_strategy_config(strategy_config)
            
            # Normalize strategy name to lowercase
            normalized_name = strategy_name.lower()
            cls.register_strategy(strategy_instance, normalized_name)
            print(f"Loaded strategy from {config_file_path} {normalized_name} [{strategy_class_path}]")

        return strategies

    @classmethod
    def autodiscover_strategies(cls) -> Dict[str, Type]:
        strategies = cls._strategies
        for module_info in pkgutil.iter_modules():
            if not module_info.name.startswith("text_extract_api"):
                continue

            try:
                module = importlib.import_module(module_info.name)
            except ImportError:
                continue

            if not hasattr(module, "__path__"):
                continue

            for submodule_info in pkgutil.walk_packages(module.__path__, module_info.name + "."):
                if ".strategies." not in submodule_info.name:
                    continue

                try:
                    ocr_module = importlib.import_module(submodule_info.name)
                except ImportError as e:
                    print('Error loading strategy ' + submodule_info.name + ': ' + str(e))
                    continue
                for attr_name in dir(ocr_module):
                    attr = getattr(ocr_module, attr_name)
                    if (isinstance(attr, type)
                            and issubclass(attr, Strategy)
                            and attr is not Strategy
                    ):
                        # Get the strategy name using the classmethod
                        try:
                            strategy_name = attr.name().lower()  # Normalize to lowercase
                            if strategy_name not in strategies:
                                strategies[strategy_name] = attr()
                                print(f"Discovered strategy {strategy_name} from {submodule_info.name} [{module_info.name}]")
                            else:
                                print(f"Strategy {strategy_name} already discovered, skipping duplicate")
                        except Exception as e:
                            print(f"Error getting name for strategy {attr_name}: {e}")
                            continue


        cls._strategies = strategies



