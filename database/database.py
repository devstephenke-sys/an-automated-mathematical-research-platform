"""
Database Module - Manages discoveries and caching
"""

import sqlite3
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import json

class DiscoveryDatabase:
    """SQLite database for storing mathematical discoveries"""
    
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Discoveries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS discoveries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    discovery_type TEXT NOT NULL,
                    number_set TEXT NOT NULL,
                    pattern TEXT NOT NULL,
                    confidence REAL,
                    complexity TEXT,
                    novelty TEXT,
                    evidence_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            ''')
            
            # Conjectures table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conjectures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    statement TEXT NOT NULL,
                    type TEXT,
                    confidence REAL,
                    evidence_count INTEGER,
                    status TEXT DEFAULT 'open',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    verified BOOLEAN DEFAULT 0,
                    counterexample TEXT
                )
            ''')
            
            # Analysis cache
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analysis_cache (
                    hash TEXT PRIMARY KEY,
                    number_set TEXT,
                    features TEXT,
                    patterns TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def add_discovery(self, discovery_type: str, number_set: str, 
                     pattern: str, confidence: float, 
                     complexity: str = 'medium', novelty: str = 'medium',
                     evidence_count: int = 0, metadata: Dict = None):
        """Add a discovery to the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO discoveries 
                (discovery_type, number_set, pattern, confidence, complexity, novelty, evidence_count, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                discovery_type,
                number_set,
                pattern,
                confidence,
                complexity,
                novelty,
                evidence_count,
                json.dumps(metadata) if metadata else None
            ))
            conn.commit()
    
    def add_conjecture(self, statement: str, conj_type: str,
                      confidence: float, evidence_count: int, status: str = 'open'):
        """Add a conjecture to the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO conjectures
                (statement, type, confidence, evidence_count, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (statement, conj_type, confidence, evidence_count, status))
            conn.commit()
    
    def get_all_discoveries(self, limit: int = None) -> List[Dict]:
        """Retrieve all discoveries"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = 'SELECT * FROM discoveries ORDER BY created_at DESC'
            if limit:
                query += f' LIMIT {limit}'
            
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_all_conjectures(self, status: str = None) -> List[Dict]:
        """Retrieve all conjectures"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if status:
                cursor.execute('SELECT * FROM conjectures WHERE status = ? ORDER BY created_at DESC', (status,))
            else:
                cursor.execute('SELECT * FROM conjectures ORDER BY created_at DESC')
            
            return [dict(row) for row in cursor.fetchall()]
    
    def verify_conjecture(self, conjecture_id: int, verified: bool = True):
        """Mark a conjecture as verified or refuted"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            status = 'verified' if verified else 'refuted'
            cursor.execute('UPDATE conjectures SET status = ?, verified = ? WHERE id = ?',
                          (status, verified, conjecture_id))
            conn.commit()
    
    def cache_analysis(self, hash_key: str, number_set: str, 
                      features: Dict, patterns: Dict, hours: int = 24):
        """Cache analysis results"""
        from datetime import timedelta
        expires_at = datetime.now() + timedelta(hours=hours)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO analysis_cache
                (hash, number_set, features, patterns, expires_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                hash_key,
                number_set,
                json.dumps(features),
                json.dumps(patterns),
                expires_at
            ))
            conn.commit()
    
    def get_cached_analysis(self, hash_key: str) -> Dict:
        """Retrieve cached analysis if not expired"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM analysis_cache
                WHERE hash = ? AND expires_at > datetime('now')
            ''', (hash_key,))
            result = cursor.fetchone()
            
            if result:
                return {
                    'number_set': result[1],
                    'features': json.loads(result[2]),
                    'patterns': json.loads(result[3])
                }
        return None
    
    def clear_expired_cache(self):
        """Remove expired cache entries"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM analysis_cache WHERE expires_at < datetime('now')")
            conn.commit()
