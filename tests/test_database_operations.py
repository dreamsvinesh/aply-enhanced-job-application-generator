#!/usr/bin/env python3
"""
Database Operations Test Suite
Comprehensive tests for the database manager functionality.
"""

import os
import sys
import sqlite3
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

# Add the modules directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "modules"))

from database_manager import DatabaseManager

class TestDatabaseOperations(unittest.TestCase):
    """Test suite for database operations."""
    
    def setUp(self):
        """Set up test database for each test."""
        # Create temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db_path = self.temp_db.name
        self.temp_db.close()
        
        # Initialize database manager with temp database
        self.db_manager = DatabaseManager(self.temp_db_path)
        
        # Sample test data
        self.sample_jd_analysis = {
            "role_focus": "communication_platforms",
            "key_requirements": ["UI/UX design", "frontend development", "React"],
            "company_culture": "creative, user-focused",
            "skills_match": ["React", "JavaScript", "Design Systems"]
        }
        
        self.sample_profile_match = {
            "matching_skills": ["React", "JavaScript"],
            "missing_skills": ["Figma"],
            "relevant_experience": ["Frontend development at TechCorp"],
            "credibility_factors": ["Strong React portfolio", "2+ years frontend experience"]
        }
        
        self.sample_positioning = {
            "key_strengths": ["React expertise", "User-centered design"],
            "positioning_angle": "Experienced frontend developer with design sensibility",
            "emphasis_areas": ["Technical skills", "Portfolio projects"]
        }
        
        self.sample_content = {
            "summary": "Experienced React developer with strong design background",
            "experience": [
                {
                    "company": "TechCorp",
                    "role": "Frontend Developer",
                    "highlights": ["Built responsive React applications", "Improved user engagement by 25%"]
                }
            ]
        }
    
    def tearDown(self):
        """Clean up after each test."""
        # Remove temporary database file
        if os.path.exists(self.temp_db_path):
            os.unlink(self.temp_db_path)
    
    def test_database_initialization(self):
        """Test that database initializes correctly with all tables."""
        # Verify database file exists
        self.assertTrue(os.path.exists(self.temp_db_path))
        
        # Check that all expected tables exist
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = [
                'applications', 'content_versions', 'application_tracking',
                'llm_usage', 'content_quality_metrics', 'system_metrics'
            ]
            
            for table in expected_tables:
                self.assertIn(table, tables, f"Table {table} not found in database")
    
    def test_create_application(self):
        """Test creating a new application record."""
        # Create application
        app_id = self.db_manager.create_application(
            company="Squarespace",
            role_title="Frontend Developer",
            country="Portugal",
            jd_text="Looking for experienced React developer...",
            jd_analysis=self.sample_jd_analysis,
            credibility_score=8,
            profile_match_analysis=self.sample_profile_match,
            positioning_strategy=self.sample_positioning
        )
        
        # Verify application was created
        self.assertIsInstance(app_id, int)
        self.assertGreater(app_id, 0)
        
        # Verify application can be retrieved
        app = self.db_manager.get_application(app_id)
        self.assertIsNotNone(app)
        self.assertEqual(app['company'], "Squarespace")
        self.assertEqual(app['role_title'], "Frontend Developer")
        self.assertEqual(app['credibility_score'], 8)
        
        # Verify JSON fields are properly parsed
        self.assertIsInstance(app['jd_analysis'], dict)
        self.assertEqual(app['jd_analysis']['role_focus'], "communication_platforms")
    
    def test_content_versioning(self):
        """Test content versioning functionality."""
        # First create an application
        app_id = self.db_manager.create_application(
            company="TestCorp",
            role_title="Developer",
            country="Netherlands",
            jd_text="Test JD",
            jd_analysis=self.sample_jd_analysis,
            credibility_score=7,
            profile_match_analysis=self.sample_profile_match,
            positioning_strategy=self.sample_positioning
        )
        
        # Save first version of resume content
        content_v1_id = self.db_manager.save_content_version(
            application_id=app_id,
            content_type="resume",
            content=self.sample_content,
            template_variant="b2b",
            quality_score=8.5,
            generation_method="template_only",
            generation_time_ms=150
        )
        
        # Save second version (LLM customized)
        modified_content = self.sample_content.copy()
        modified_content['summary'] = "Expert React developer with proven design expertise"
        
        content_v2_id = self.db_manager.save_content_version(
            application_id=app_id,
            content_type="resume",
            content=modified_content,
            template_variant="b2b",
            llm_customization_applied=True,
            quality_score=9.2,
            generation_method="llm_customized",
            generation_time_ms=2500,
            llm_cost_usd=0.003
        )
        
        # Verify both versions exist and have correct version numbers
        self.assertNotEqual(content_v1_id, content_v2_id)
        
        # Get latest content (should be version 2)
        latest_content = self.db_manager.get_latest_content(app_id, "resume")
        self.assertIsNotNone(latest_content)
        self.assertEqual(latest_content['version'], 2)
        self.assertTrue(latest_content['llm_customization_applied'])
        self.assertEqual(latest_content['content']['summary'], "Expert React developer with proven design expertise")
    
    def test_event_tracking(self):
        """Test application event tracking."""
        # Create application
        app_id = self.db_manager.create_application(
            company="EventTest",
            role_title="Test Role",
            country="Denmark",
            jd_text="Test JD",
            jd_analysis=self.sample_jd_analysis,
            credibility_score=6,
            profile_match_analysis=self.sample_profile_match,
            positioning_strategy=self.sample_positioning
        )
        
        # Update status (this should create tracking events)
        self.db_manager.update_application_status(app_id, "sent", {"sent_via": "email"})
        self.db_manager.update_application_status(app_id, "viewed", {"viewed_at": "2025-11-14"})
        
        # Get application timeline
        timeline = self.db_manager.get_application_timeline(app_id)
        
        # Should have at least 3 events: generated (from creation), sent, viewed
        self.assertGreaterEqual(len(timeline), 3)
        
        # Check event types
        event_types = [event['event_type'] for event in timeline]
        self.assertIn('generated', event_types)
        self.assertIn('sent', event_types)
        self.assertIn('viewed', event_types)
        
        # Verify chronological order
        timestamps = [event['timestamp'] for event in timeline]
        self.assertEqual(timestamps, sorted(timestamps))
    
    def test_llm_usage_tracking(self):
        """Test LLM usage and cost tracking."""
        # Create application for context
        app_id = self.db_manager.create_application(
            company="LLMTest",
            role_title="Test Role",
            country="Finland",
            jd_text="Test JD",
            jd_analysis=self.sample_jd_analysis,
            credibility_score=9,
            profile_match_analysis=self.sample_profile_match,
            positioning_strategy=self.sample_positioning
        )
        
        # Track JD analysis LLM usage
        usage_id_1 = self.db_manager.track_llm_usage(
            application_id=app_id,
            task_type="jd_analysis",
            model_used="gpt-4o-mini",
            tokens_input=850,
            tokens_output=420,
            cost_usd=0.004,
            response_time_ms=1200,
            success=True,
            output_quality_score=8.8
        )
        
        # Track content customization LLM usage
        usage_id_2 = self.db_manager.track_llm_usage(
            application_id=app_id,
            task_type="content_customization",
            model_used="gpt-4o-mini",
            tokens_input=920,
            tokens_output=380,
            cost_usd=0.003,
            response_time_ms=950,
            success=True,
            output_quality_score=9.1
        )
        
        # Verify tracking records were created
        self.assertIsInstance(usage_id_1, int)
        self.assertIsInstance(usage_id_2, int)
        
        # Get cost summary
        cost_summary = self.db_manager.get_llm_cost_summary(days=1)
        
        # Should have both task types
        self.assertIn('jd_analysis', cost_summary)
        self.assertIn('content_customization', cost_summary)
        
        # Verify cost calculations
        jd_stats = cost_summary['jd_analysis']
        self.assertEqual(jd_stats['call_count'], 1)
        self.assertEqual(jd_stats['total_cost'], 0.004)
        
        customization_stats = cost_summary['content_customization']
        self.assertEqual(customization_stats['call_count'], 1)
        self.assertEqual(customization_stats['total_cost'], 0.003)
    
    def test_quality_metrics(self):
        """Test content quality metrics tracking."""
        # Create application and content version
        app_id = self.db_manager.create_application(
            company="QualityTest",
            role_title="Test Role",
            country="Sweden",
            jd_text="Test JD",
            jd_analysis=self.sample_jd_analysis,
            credibility_score=7,
            profile_match_analysis=self.sample_profile_match,
            positioning_strategy=self.sample_positioning
        )
        
        content_id = self.db_manager.save_content_version(
            application_id=app_id,
            content_type="cover_letter",
            content={"text": "Sample cover letter content"},
            template_variant="b2c",
            quality_score=8.7
        )
        
        # Save quality metrics
        metrics_id = self.db_manager.save_quality_metrics(
            content_version_id=content_id,
            factual_accuracy_score=9.2,
            cultural_appropriateness_score=8.8,
            professional_tone_score=8.5,
            achievement_clarity_score=9.0,
            length_compliance_score=8.9,
            country_tone_compliance=8.7,
            country_format_compliance=9.1,
            llm_language_detected=False,
            placeholder_text_found=False,
            formatting_issues_count=0
        )
        
        # Verify metrics were saved
        self.assertIsInstance(metrics_id, int)
        
        # Get quality trends
        quality_trends = self.db_manager.get_quality_trends(days=1)
        
        # Should have quality data
        self.assertIn('avg_overall_quality', quality_trends)
        self.assertGreater(quality_trends['avg_overall_quality'], 8.0)
        self.assertEqual(quality_trends['total_content_pieces'], 1)
    
    def test_application_queries(self):
        """Test application querying and filtering."""
        # Create multiple applications with different properties
        apps = [
            ("Company A", "Role 1", "Netherlands", 8),
            ("Company B", "Role 2", "Netherlands", 6),
            ("Company A", "Role 3", "Portugal", 9),
            ("Company C", "Role 4", "Denmark", 5),
        ]
        
        app_ids = []
        for company, role, country, credibility in apps:
            app_id = self.db_manager.create_application(
                company=company,
                role_title=role,
                country=country,
                jd_text=f"JD for {role}",
                jd_analysis=self.sample_jd_analysis,
                credibility_score=credibility,
                profile_match_analysis=self.sample_profile_match,
                positioning_strategy=self.sample_positioning
            )
            app_ids.append(app_id)
        
        # Test filtering by company
        company_a_apps = self.db_manager.get_applications(company="Company A")
        self.assertEqual(len(company_a_apps), 2)
        
        # Test filtering by country
        netherlands_apps = self.db_manager.get_applications(country="Netherlands")
        self.assertEqual(len(netherlands_apps), 2)
        
        # Test filtering by minimum credibility
        high_credibility_apps = self.db_manager.get_applications(min_credibility=8)
        self.assertEqual(len(high_credibility_apps), 2)
        
        # Test limit
        limited_apps = self.db_manager.get_applications(limit=2)
        self.assertEqual(len(limited_apps), 2)
        
        # Test combined filters
        filtered_apps = self.db_manager.get_applications(
            country="Netherlands",
            min_credibility=7
        )
        self.assertEqual(len(filtered_apps), 1)
        self.assertEqual(filtered_apps[0]['credibility_score'], 8)
    
    def test_analytics_and_reporting(self):
        """Test analytics and reporting functionality."""
        # Create several applications with content
        for i in range(5):
            app_id = self.db_manager.create_application(
                company=f"Company {i}",
                role_title=f"Role {i}",
                country="Ireland",
                jd_text=f"JD text {i}",
                jd_analysis=self.sample_jd_analysis,
                credibility_score=7 + i % 3,
                profile_match_analysis=self.sample_profile_match,
                positioning_strategy=self.sample_positioning
            )
            
            # Add some content and LLM usage
            self.db_manager.save_content_version(
                application_id=app_id,
                content_type="resume",
                content=self.sample_content,
                template_variant="aiml",
                quality_score=8.0 + i * 0.2
            )
            
            self.db_manager.track_llm_usage(
                application_id=app_id,
                task_type="jd_analysis",
                model_used="gpt-4o-mini",
                tokens_input=800 + i * 10,
                tokens_output=400 + i * 5,
                cost_usd=0.003 + i * 0.0001,
                response_time_ms=1000 + i * 50
            )
        
        # Test application stats
        stats = self.db_manager.get_application_stats(days=1)
        self.assertEqual(stats['total_applications'], 5)
        self.assertEqual(stats['unique_companies'], 5)
        self.assertEqual(stats['unique_countries'], 1)
        self.assertGreater(stats['avg_credibility'], 7.0)
        
        # Test LLM cost summary
        cost_summary = self.db_manager.get_llm_cost_summary(days=1)
        self.assertIn('jd_analysis', cost_summary)
        jd_stats = cost_summary['jd_analysis']
        self.assertEqual(jd_stats['call_count'], 5)
        self.assertGreater(jd_stats['total_cost'], 0.015)
        
        # Test database size info
        size_info = self.db_manager.get_database_size()
        self.assertIn('size_bytes', size_info)
        self.assertIn('table_counts', size_info)
        self.assertGreater(size_info['table_counts']['applications'], 0)
    
    def test_custom_query(self):
        """Test custom query functionality."""
        # Create test data
        app_id = self.db_manager.create_application(
            company="CustomQueryTest",
            role_title="Test Role",
            country="Portugal",
            jd_text="Test JD",
            jd_analysis=self.sample_jd_analysis,
            credibility_score=8,
            profile_match_analysis=self.sample_profile_match,
            positioning_strategy=self.sample_positioning
        )
        
        # Execute custom query
        results = self.db_manager.execute_custom_query(
            "SELECT company, credibility_score FROM applications WHERE credibility_score > ?",
            (7,)
        )
        
        # Verify results
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['company'], "CustomQueryTest")
        self.assertEqual(results[0]['credibility_score'], 8)


def run_database_tests():
    """Run all database tests and return results."""
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabaseOperations)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return test results
    return result.wasSuccessful(), result.testsRun, len(result.failures), len(result.errors)


if __name__ == "__main__":
    # Run tests when script is executed directly
    print("🧪 Running Database Operations Tests...\n")
    
    success, total_tests, failures, errors = run_database_tests()
    
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"Total Tests: {total_tests}")
    print(f"Failures: {failures}")
    print(f"Errors: {errors}")
    print(f"Success Rate: {((total_tests - failures - errors) / total_tests * 100):.1f}%")
    
    if success:
        print("\n✅ ALL TESTS PASSED - Database operations working correctly!")
        exit(0)
    else:
        print("\n❌ SOME TESTS FAILED - Please check the output above for details.")
        exit(1)