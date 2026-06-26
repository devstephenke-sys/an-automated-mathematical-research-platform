"""
MathDiscoveryAI Configuration
Central configuration for all modules
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_DIR = PROJECT_ROOT / "database"
REPORTS_DIR = PROJECT_ROOT / "reports"
CACHE_DIR = PROJECT_ROOT / ".cache"

# Create directories if they don't exist
for directory in [DATA_DIR, DATABASE_DIR, REPORTS_DIR, CACHE_DIR]:
    directory.mkdir(exist_ok=True)

# Database
DATABASE_PATH = DATABASE_DIR / "discoveries.db"
CACHE_DATABASE_PATH = DATABASE_DIR / "cache.db"

# Feature extraction settings
FEATURE_COUNT = 350  # Target number of features to extract
MAX_FEATURES = 500   # Hard limit

# Analysis settings
CORRELATION_THRESHOLD = 0.7
MIN_PATTERN_EVIDENCE = 5
PATTERN_CONFIDENCE_MIN = 0.6

# Search settings
MAX_RELATIONSHIPS_TO_TEST = 1000000
BATCH_SIZE = 100

# Visualization settings
CHART_DPI = 150
CHART_FIGSIZE = (12, 8)
REPORT_THEME = "seaborn"

# Data sources
KNOWN_PERFECT_NUMBERS = [
    6, 28, 496, 8128, 33550336, 8589869056, 137438691328, 2305843008139952128
]

KNOWN_MERSENNE_EXPONENTS = [
    2, 3, 5, 7, 13, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 
    4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049, 
    216091, 756839, 859433, 1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 
    20996011, 24036583, 25964951, 30402457, 32582657, 37156667, 42643801, 43112609
]

# AI/ML settings
ML_SEED = 42
TEST_SIZE = 0.2
CROSS_VALIDATION_FOLDS = 5

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = PROJECT_ROOT / "research.log"

# Runtime constraints
MAX_COMPUTATION_TIME = 3600  # 1 hour in seconds
TIMEOUT_FEATURE_EXTRACTION = 600  # 10 minutes
TIMEOUT_PATTERN_SEARCH = 1800  # 30 minutes
