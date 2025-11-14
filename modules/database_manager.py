#!/usr/bin/env python3
"""
Database Manager Module
Handles all database operations for the enhanced Aply system with LLM integration.
"""

import sqlite3
import json
import os
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import logging

class DatabaseManager:
    """
    Manages all database operations for the Aply job application system.
    
    Features:
    - Application tracking with LLM analysis
    - Content versioning with quality metrics
    - Event-driven tracking
    - LLM usage and cost monitoring
    - Performance analytics
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file. If None, uses default location.
        """
        if db_path is None:
            # Default to database folder in project root
            project_root = Path(__file__).parent.parent
            db_dir = project_root / "database"
            db_dir.mkdir(exist_ok=True)
            self.db_path = str(db_dir / "aply_applications.db")
        else:
            self.db_path = db_path
            
        self.schema_path = Path(__file__).parent.parent / "database" / "schema.sql"
        
        # Set up logging first
        self.logger = logging.getLogger(__name__)
        
        # Initialize database
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database with schema if it doesn't exist."""
        # Check if database exists and has tables
        needs_initialization = not os.path.exists(self.db_path)
        
        if not needs_initialization:
            # Check if tables exist
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                needs_initialization = len(tables) == 0
        
        if needs_initialization:
            self._create_tables()
    
    def _create_tables(self):
        """Create database tables from schema file."""
        try:
            with open(self.schema_path, 'r') as f:
                schema_sql = f.read()
            
            with sqlite3.connect(self.db_path) as conn:
                conn.executescript(schema_sql)
                conn.commit()
                
            self.logger.info(f"Database initialized at {self.db_path}")
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
            raise
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with JSON support."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    # ===============================
    # APPLICATION MANAGEMENT
    # ===============================
    
    def create_application(self, 
                         company: str, 
                         role_title: str, 
                         country: str,
                         jd_text: str,
                         jd_analysis: Dict,
                         credibility_score: int,
                         profile_match_analysis: Dict,
                         positioning_strategy: Dict) -> int:
        """
        Create new job application record.
        
        Returns:
            Application ID
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO applications (
                    company, role_title, country, jd_text, jd_analysis,
                    credibility_score, profile_match_analysis, positioning_strategy
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                company, role_title, country, jd_text,
                json.dumps(jd_analysis),
                credibility_score,
                json.dumps(profile_match_analysis),
                json.dumps(positioning_strategy)
            ))
            
            application_id = cursor.lastrowid
            
            # Track creation event within same transaction
            self._track_event(application_id, 'generated', {
                'company': company,
                'role': role_title,
                'credibility_score': credibility_score
            }, cursor=cursor)
            
            conn.commit()
            return application_id
    
    def get_application(self, application_id: int) -> Optional[Dict]:
        """Get application by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM applications WHERE id = ?
            """, (application_id,))
            
            row = cursor.fetchone()
            if row:
                return self._row_to_dict(row, parse_json=['jd_analysis', 'profile_match_analysis', 'positioning_strategy'])
            return None
    
    def get_applications(self, 
                        company: Optional[str] = None,
                        country: Optional[str] = None,
                        min_credibility: Optional[int] = None,
                        limit: Optional[int] = None) -> List[Dict]:
        """Get applications with optional filtering."""
        query = "SELECT * FROM applications WHERE 1=1"
        params = []
        
        if company:
            query += " AND company LIKE ?"
            params.append(f"%{company}%")
        
        if country:
            query += " AND country = ?"
            params.append(country)
            
        if min_credibility:
            query += " AND credibility_score >= ?"
            params.append(min_credibility)
        
        query += " ORDER BY created_at DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            rows = cursor.fetchall()
            return [self._row_to_dict(row, parse_json=['jd_analysis', 'profile_match_analysis', 'positioning_strategy']) 
                    for row in rows]
    
    def update_application_status(self, application_id: int, status: str, event_data: Dict = None):
        """Update application status and track event."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE applications 
                SET application_status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (status, application_id))
            
            # Track status change event within same transaction
            self._track_event(application_id, status, event_data or {}, cursor=cursor)
            
            conn.commit()
    
    # ===============================
    # CONTENT VERSION MANAGEMENT
    # ===============================
    
    def save_content_version(self,
                           application_id: int,
                           content_type: str,
                           content: Dict,
                           template_structure: Optional[Dict] = None,
                           llm_customization_applied: bool = False,
                           quality_score: Optional[float] = None,
                           human_voice_score: Optional[float] = None,
                           rule_compliance_score: Optional[float] = None,
                           generation_method: str = 'template_only',
                           generation_time_ms: Optional[int] = None,
                           llm_cost_usd: float = 0.0) -> int:
        """
        Save content version with quality metrics.
        
        Returns:
            Content version ID
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get next version number
            cursor.execute("""
                SELECT COALESCE(MAX(version), 0) + 1
                FROM content_versions 
                WHERE application_id = ? AND content_type = ?
            """, (application_id, content_type))
            
            version = cursor.fetchone()[0]
            
            # Insert content version
            cursor.execute("""
                INSERT INTO content_versions (
                    application_id, content_type, version, content, template_structure,
                    llm_customization_applied, quality_score, human_voice_score,
                    rule_compliance_score, generation_method, generation_time_ms, llm_cost_usd
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                application_id, content_type, version, json.dumps(content), 
                json.dumps(template_structure) if template_structure else None,
                llm_customization_applied, quality_score, human_voice_score,
                rule_compliance_score, generation_method, generation_time_ms, llm_cost_usd
            ))
            
            content_version_id = cursor.lastrowid
            conn.commit()
            return content_version_id
    
    def get_latest_content(self, application_id: int, content_type: str) -> Optional[Dict]:
        """Get latest version of specific content type."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM content_versions 
                WHERE application_id = ? AND content_type = ?
                ORDER BY version DESC LIMIT 1
            """, (application_id, content_type))
            
            row = cursor.fetchone()
            if row:
                return self._row_to_dict(row, parse_json=['content'])
            return None
    
    def get_all_content(self, application_id: int) -> Dict[str, Dict]:
        """Get all latest content for an application."""
        content_types = ['resume', 'cover_letter', 'linkedin_message', 'email_template']
        result = {}
        
        for content_type in content_types:
            content = self.get_latest_content(application_id, content_type)
            if content:
                result[content_type] = content
        
        return result
    
    # ===============================
    # EVENT TRACKING
    # ===============================
    
    def _track_event(self, 
                    application_id: int, 
                    event_type: str, 
                    event_data: Dict,
                    user_action: Optional[str] = None,
                    system_response: Optional[str] = None,
                    session_id: Optional[str] = None,
                    cursor=None):
        """Track application event."""
        if cursor is not None:
            # Use existing cursor and connection (within transaction)
            cursor.execute("""
                INSERT INTO application_tracking (
                    application_id, event_type, event_data, 
                    user_action, system_response, session_id
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                application_id, event_type, json.dumps(event_data),
                user_action, system_response, session_id
            ))
        else:
            # Create new connection
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO application_tracking (
                        application_id, event_type, event_data, 
                        user_action, system_response, session_id
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    application_id, event_type, json.dumps(event_data),
                    user_action, system_response, session_id
                ))
                
                conn.commit()
    
    def get_application_timeline(self, application_id: int) -> List[Dict]:
        """Get chronological timeline of events for an application."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM application_tracking 
                WHERE application_id = ?
                ORDER BY timestamp ASC
            """, (application_id,))
            
            rows = cursor.fetchall()
            return [self._row_to_dict(row, parse_json=['event_data']) for row in rows]
    
    # ===============================
    # LLM USAGE TRACKING
    # ===============================
    
    def track_llm_usage(self,
                       task_type: str,
                       model_used: str,
                       tokens_input: int,
                       tokens_output: int,
                       cost_usd: float,
                       response_time_ms: int,
                       application_id: Optional[int] = None,
                       success: bool = True,
                       error_message: Optional[str] = None,
                       output_quality_score: Optional[float] = None) -> int:
        """Track LLM API usage for cost and performance monitoring."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO llm_usage (
                    application_id, task_type, model_used, tokens_input, tokens_output,
                    cost_usd, response_time_ms, success, error_message, output_quality_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                application_id, task_type, model_used, tokens_input, tokens_output,
                cost_usd, response_time_ms, success, error_message, output_quality_score
            ))
            
            usage_id = cursor.lastrowid
            conn.commit()
            return usage_id
    
    # ===============================
    # QUALITY METRICS
    # ===============================
    
    def save_quality_metrics(self,
                           content_version_id: int,
                           factual_accuracy_score: float,
                           cultural_appropriateness_score: float,
                           professional_tone_score: float,
                           achievement_clarity_score: float,
                           length_compliance_score: float,
                           country_tone_compliance: float,
                           country_format_compliance: float,
                           llm_language_detected: bool = False,
                           placeholder_text_found: bool = False,
                           formatting_issues_count: int = 0,
                           needs_revision: bool = False) -> int:
        """Save detailed quality metrics for content."""
        # Calculate overall quality as weighted average
        overall_quality = (
            factual_accuracy_score * 0.2 +
            cultural_appropriateness_score * 0.15 +
            professional_tone_score * 0.15 +
            achievement_clarity_score * 0.2 +
            length_compliance_score * 0.1 +
            country_tone_compliance * 0.1 +
            country_format_compliance * 0.1
        )
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO content_quality_metrics (
                    content_version_id, factual_accuracy_score, cultural_appropriateness_score,
                    professional_tone_score, achievement_clarity_score, length_compliance_score,
                    llm_language_detected, placeholder_text_found, formatting_issues_count,
                    country_tone_compliance, country_format_compliance, overall_quality, needs_revision
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                content_version_id, factual_accuracy_score, cultural_appropriateness_score,
                professional_tone_score, achievement_clarity_score, length_compliance_score,
                llm_language_detected, placeholder_text_found, formatting_issues_count,
                country_tone_compliance, country_format_compliance, overall_quality, needs_revision
            ))
            
            metrics_id = cursor.lastrowid
            conn.commit()
            return metrics_id
    
    # ===============================
    # ANALYTICS AND REPORTING
    # ===============================
    
    def get_application_stats(self, days: int = 30) -> Dict:
        """Get application statistics for the last N days."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_applications,
                    AVG(credibility_score) as avg_credibility,
                    COUNT(CASE WHEN application_status = 'sent' THEN 1 END) as sent_count,
                    COUNT(CASE WHEN application_status = 'responded' THEN 1 END) as response_count,
                    COUNT(DISTINCT company) as unique_companies,
                    COUNT(DISTINCT country) as unique_countries
                FROM applications 
                WHERE created_at >= date('now', '-{} days')
            """.format(days))
            
            row = cursor.fetchone()
            return dict(row) if row else {}
    
    def get_llm_cost_summary(self, days: int = 30) -> Dict:
        """Get LLM usage cost summary."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    task_type,
                    COUNT(*) as call_count,
                    SUM(cost_usd) as total_cost,
                    AVG(cost_usd) as avg_cost_per_call,
                    AVG(response_time_ms) as avg_response_time,
                    SUM(tokens_input) as total_input_tokens,
                    SUM(tokens_output) as total_output_tokens
                FROM llm_usage 
                WHERE timestamp >= date('now', '-{} days')
                GROUP BY task_type
            """.format(days))
            
            rows = cursor.fetchall()
            return {row['task_type']: dict(row) for row in rows}
    
    def get_quality_trends(self, days: int = 30) -> Dict:
        """Get content quality trends."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    AVG(cqm.overall_quality) as avg_overall_quality,
                    AVG(cqm.factual_accuracy_score) as avg_factual_accuracy,
                    AVG(cqm.cultural_appropriateness_score) as avg_cultural_fit,
                    AVG(cqm.professional_tone_score) as avg_professional_tone,
                    COUNT(CASE WHEN cqm.needs_revision = 1 THEN 1 END) as revision_needed_count,
                    COUNT(*) as total_content_pieces
                FROM content_quality_metrics cqm
                JOIN content_versions cv ON cqm.content_version_id = cv.id
                WHERE cv.created_at >= date('now', '-{} days')
            """.format(days))
            
            row = cursor.fetchone()
            return dict(row) if row else {}
    
    # ===============================
    # UTILITY METHODS
    # ===============================
    
    def _row_to_dict(self, row: sqlite3.Row, parse_json: List[str] = None) -> Dict:
        """Convert SQLite row to dictionary with JSON parsing."""
        result = dict(row)
        
        if parse_json:
            for field in parse_json:
                if field in result and result[field]:
                    try:
                        result[field] = json.loads(result[field])
                    except json.JSONDecodeError:
                        # Keep as string if JSON parsing fails
                        pass
        
        return result
    
    def execute_custom_query(self, query: str, params: Tuple = ()) -> List[Dict]:
        """Execute custom query and return results."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def backup_database(self, backup_path: str):
        """Create backup of database."""
        import shutil
        shutil.copy2(self.db_path, backup_path)
        self.logger.info(f"Database backed up to {backup_path}")
    
    def get_database_size(self) -> Dict[str, Any]:
        """Get database size and table counts."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get file size
            db_size_bytes = os.path.getsize(self.db_path)
            
            # Get table counts
            tables = ['applications', 'content_versions', 'application_tracking', 
                     'llm_usage', 'content_quality_metrics']
            
            table_counts = {}
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                table_counts[table] = cursor.fetchone()[0]
            
            return {
                'size_bytes': db_size_bytes,
                'size_mb': round(db_size_bytes / (1024 * 1024), 2),
                'table_counts': table_counts
            }