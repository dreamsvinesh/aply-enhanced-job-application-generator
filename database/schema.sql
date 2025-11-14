-- Aply Job Application Database Schema
-- Enhanced system with LLM integration and systematic tracking

-- Applications table - Core job application records
CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT NOT NULL,
    role_title TEXT NOT NULL,
    country TEXT NOT NULL,
    
    -- Job Description Analysis (LLM-generated)
    jd_text TEXT, -- Original job description text
    jd_analysis TEXT, -- JSON: {requirements, skills, company_culture, role_focus}
    
    -- Profile Matching and Credibility
    credibility_score INTEGER CHECK(credibility_score >= 1 AND credibility_score <= 10),
    profile_match_analysis TEXT, -- JSON: detailed matching analysis
    positioning_strategy TEXT, -- JSON: how to position user for this role
    
    -- Application Status
    application_status TEXT DEFAULT 'generated', -- 'generated', 'sent', 'viewed', 'responded', 'rejected'
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    UNIQUE(company, role_title, country, created_at)
);

-- Content versions table - All generated content with versioning
CREATE TABLE content_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER NOT NULL,
    
    -- Content Details
    content_type TEXT NOT NULL, -- 'resume', 'cover_letter', 'linkedin_message', 'email_template'
    version INTEGER DEFAULT 1,
    content TEXT NOT NULL, -- JSON: actual content structure
    
    -- Content Metadata
    template_structure TEXT, -- JSON: dynamic LLM-generated template structure
    llm_customization_applied BOOLEAN DEFAULT FALSE,
    
    -- Quality Metrics
    quality_score REAL, -- Overall content quality (0-10)
    human_voice_score REAL, -- How human-like the content sounds (0-10)
    rule_compliance_score REAL, -- Compliance with country/content rules (0-10)
    
    -- Validation Results
    validation_issues TEXT, -- JSON: array of validation issues found
    validation_passed BOOLEAN DEFAULT FALSE,
    
    -- Generation Details
    generation_method TEXT, -- 'template_only', 'llm_customized', 'hybrid'
    generation_time_ms INTEGER, -- Time taken to generate
    llm_cost_usd REAL DEFAULT 0.0, -- Cost of LLM calls
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key
    FOREIGN KEY (application_id) REFERENCES applications (id) ON DELETE CASCADE
);

-- Application tracking table - Event-driven tracking
CREATE TABLE application_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER NOT NULL,
    
    -- Event Details
    event_type TEXT NOT NULL, -- 'generated', 'validated', 'sent', 'viewed', 'responded', 'rejected'
    event_data TEXT, -- JSON: additional event-specific data
    
    -- Event Context
    user_action TEXT, -- Action that triggered this event
    system_response TEXT, -- System response or result
    
    -- Tracking Metadata
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id TEXT, -- To group related events
    
    -- Foreign Key
    FOREIGN KEY (application_id) REFERENCES applications (id) ON DELETE CASCADE
);

-- LLM Usage tracking table - Monitor LLM costs and performance
CREATE TABLE llm_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER,
    
    -- LLM Call Details
    task_type TEXT NOT NULL, -- 'jd_analysis', 'content_customization', 'validation'
    model_used TEXT, -- 'gpt-4o-mini', etc.
    
    -- Usage Metrics
    tokens_input INTEGER,
    tokens_output INTEGER,
    cost_usd REAL,
    response_time_ms INTEGER,
    
    -- Quality Metrics
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    
    -- Content Quality (for analysis tasks)
    output_quality_score REAL, -- How good was the LLM output
    
    -- Timestamps
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key (nullable for system-wide operations)
    FOREIGN KEY (application_id) REFERENCES applications (id) ON DELETE SET NULL
);

-- Content quality metrics table - Detailed quality tracking
CREATE TABLE content_quality_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_version_id INTEGER NOT NULL,
    
    -- Quality Dimensions
    factual_accuracy_score REAL, -- Are all facts correct?
    cultural_appropriateness_score REAL, -- Fits country culture?
    professional_tone_score REAL, -- Professional but not corporate?
    achievement_clarity_score REAL, -- Clear, quantified achievements?
    length_compliance_score REAL, -- Meets country length requirements?
    
    -- Specific Checks
    llm_language_detected BOOLEAN DEFAULT FALSE, -- Corporate/AI language found?
    placeholder_text_found BOOLEAN DEFAULT FALSE, -- [Your Name] etc found?
    formatting_issues_count INTEGER DEFAULT 0,
    
    -- Country-Specific Compliance
    country_tone_compliance REAL, -- Matches country directness/formality
    country_format_compliance REAL, -- Follows country resume format
    
    -- Overall Assessment
    overall_quality REAL, -- Weighted average of all scores
    needs_revision BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key
    FOREIGN KEY (content_version_id) REFERENCES content_versions (id) ON DELETE CASCADE
);

-- System performance metrics table - Monitor system health
CREATE TABLE system_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Performance Metrics
    metric_name TEXT NOT NULL, -- 'avg_generation_time', 'success_rate', etc.
    metric_value REAL,
    metric_unit TEXT, -- 'ms', 'percentage', 'count', 'usd'
    
    -- Context
    time_period TEXT, -- 'daily', 'hourly', 'weekly'
    date_recorded DATE,
    additional_context TEXT, -- JSON with extra details
    
    -- Timestamps
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_applications_company ON applications(company);
CREATE INDEX idx_applications_created_at ON applications(created_at);
CREATE INDEX idx_applications_status ON applications(application_status);
CREATE INDEX idx_applications_credibility ON applications(credibility_score);

CREATE INDEX idx_content_versions_app_id ON content_versions(application_id);
CREATE INDEX idx_content_versions_type ON content_versions(content_type);
CREATE INDEX idx_content_versions_quality ON content_versions(quality_score);

CREATE INDEX idx_tracking_app_id ON application_tracking(application_id);
CREATE INDEX idx_tracking_event_type ON application_tracking(event_type);
CREATE INDEX idx_tracking_timestamp ON application_tracking(timestamp);

CREATE INDEX idx_llm_usage_task_type ON llm_usage(task_type);
CREATE INDEX idx_llm_usage_timestamp ON llm_usage(timestamp);
CREATE INDEX idx_llm_usage_cost ON llm_usage(cost_usd);

CREATE INDEX idx_quality_metrics_content_id ON content_quality_metrics(content_version_id);
CREATE INDEX idx_quality_metrics_overall ON content_quality_metrics(overall_quality);

CREATE INDEX idx_system_metrics_name ON system_metrics(metric_name);
CREATE INDEX idx_system_metrics_date ON system_metrics(date_recorded);

-- Create views for common queries
CREATE VIEW application_summary AS
SELECT 
    a.id,
    a.company,
    a.role_title,
    a.country,
    a.credibility_score,
    a.application_status,
    COUNT(cv.id) as content_pieces_generated,
    AVG(cv.quality_score) as avg_content_quality,
    SUM(lu.cost_usd) as total_llm_cost,
    a.created_at
FROM applications a
LEFT JOIN content_versions cv ON a.id = cv.application_id
LEFT JOIN llm_usage lu ON a.id = lu.application_id
GROUP BY a.id;

CREATE VIEW daily_system_stats AS
SELECT 
    DATE(created_at) as date,
    COUNT(*) as applications_generated,
    AVG(credibility_score) as avg_credibility,
    COUNT(CASE WHEN application_status = 'sent' THEN 1 END) as applications_sent,
    COUNT(CASE WHEN application_status = 'responded' THEN 1 END) as responses_received
FROM applications
GROUP BY DATE(created_at)
ORDER BY date DESC;

CREATE VIEW llm_cost_summary AS
SELECT 
    task_type,
    COUNT(*) as calls_made,
    SUM(cost_usd) as total_cost,
    AVG(cost_usd) as avg_cost_per_call,
    AVG(response_time_ms) as avg_response_time,
    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as success_rate
FROM llm_usage
GROUP BY task_type;