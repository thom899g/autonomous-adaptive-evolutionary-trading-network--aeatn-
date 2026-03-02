"""
AEATN Configuration Management
Centralized configuration with environment variable fallbacks
"""
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import logging

class Config:
    """Configuration manager for AEATN"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    MODELS_DIR = BASE_DIR / "models"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Create directories if they don't exist
    for dir_path in [DATA_DIR, MODELS_DIR, LOGS_DIR]:
        dir_path.mkdir(exist_ok=True)
    
    # Firebase configuration
    FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json")
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "aeatn-system")
    
    # Trading configuration
    TRADING_SYMBOLS = ["BTC/USDT", "ETH/USDT", "BNB/USDT"]
    EXCHANGE_NAME = "binance"  # Using binance for reliability
    TIMEFRAME = "1h"  # Default timeframe
    
    # Model configuration
    RL_MODEL_CHECKPOINT_INTERVAL = 1000  # Save model every 1000 steps
    NEURO_SYMBOLIC_THRESHOLD = 0.7  # Confidence threshold for action execution
    EVOLUTIONARY_EPOCHS = 1000
    
    # Risk management
    MAX_POSITION_SIZE = 0.1  # 10% of portfolio per trade
    STOP_LOSS_PERCENT = 0.02  # 2% stop loss
    TAKE_PROFIT_PERCENT = 0.05  # 5% take profit
    
    # Logging configuration
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Telegram alerts
    TELEGRAM_ENABLED = os.getenv("TELEGRAM_ENABLED", "false").lower() == "true"
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate critical configuration parameters"""
        errors = []
        
        # Check Firebase credentials
        if not Path(cls.FIREBASE_CREDENTIALS_PATH).exists():
            errors.append(f"Firebase credentials not found at {cls.FIREBASE_CREDENTIALS_PATH}")
        
        # Check trading symbols
        if not cls.TRADING_SYMBOLS:
            errors.append("No trading symbols configured")
        
        # Validate Telegram if enabled
        if cls.TELEGRAM_ENABLED:
            if not cls.TELEGRAM_BOT_TOKEN or not cls.TELEGRAM_CHAT_ID:
                errors.append("Telegram enabled but token or chat ID missing")
        
        if errors:
            logging.error("Configuration validation failed:")
            for error in errors:
                logging.error(f"  - {error}")
            return False
        return True

config = Config()