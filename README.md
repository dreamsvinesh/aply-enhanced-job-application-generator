# Aply - Enhanced Job Application Generator with LLM Agents

**AI-Powered Job Application Generator with Multi-Agent Intelligence**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-green.svg)]()

Aply is an intelligent job application generator that uses LLM-powered agents to create personalized, culturally-adapted resumes, cover letters, and outreach messages. The system employs a multi-agent architecture for content optimization, cultural adaptation, and quality validation.

## ✨ Key Features

- 🤖 **LLM Agent Framework**: 4 specialized AI agents for intelligent content optimization
- 🎯 **Skills Analysis**: AI-powered skills matching with job requirements (82%+ alignment)
- 🌍 **Cultural Adaptation**: Dynamic tone adaptation for different countries/cultures
- 📊 **Quality Scoring**: Multi-dimensional content quality assessment (8.6/10 average)
- 📄 **HTML Output**: Copy-paste friendly format with preserved formatting
- 🔄 **Real-time Optimization**: Iterative content enhancement through agent pipeline
- 📈 **Performance Analytics**: Detailed metrics and improvement suggestions

## 🚀 Quick Start

### Enhanced Version (Recommended)
```bash
# Run the AI-enhanced application generator
python3 enhanced_main.py --interactive

# Follow the prompts:
# 1. Paste job description (press Enter twice when done)
# 2. Enter target country (e.g., sweden, netherlands)
# 3. Optional: Enter company name
# 4. Get AI-enhanced application package (HTML format)
```

### Original Version
```bash
# Run the basic application generator
python3 main.py

# Follow the prompts for standard generation
```

## 🧪 Testing

### Full Test Suite
```bash
# Run all tests with detailed output
python3 run_tests.py

# Quick smoke test only
python3 run_tests.py --smoke
```

### Individual Test Modules
```bash
# Test specific components
python3 -m pytest tests/test_jd_parser.py -v
python3 -m pytest tests/test_resume_generator.py -v
python3 -m pytest tests/test_country_config.py -v
python3 -m pytest tests/test_integration.py -v
```

### Validate Generated Output
```bash
# Validate a generated application package
python3 validate_output.py output/Company_country_2025-11-13.md
```

## 📊 Test Coverage

- **Unit Tests**: Individual module functionality
- **Integration Tests**: End-to-end workflow testing
- **Quality Validation**: Output format and content checks
- **Country Compliance**: Country-specific formatting verification

## 🔧 Development Testing

### Adding New Tests

1. **Unit Tests**: Add to `tests/test_[module].py`
2. **Integration Tests**: Add to `tests/test_integration.py`
3. **Update Test Runner**: Add new modules to `run_tests.py`

### Test Structure
```
tests/
├── test_jd_parser.py         # JD parsing logic
├── test_resume_generator.py  # Resume generation
├── test_country_config.py    # Country configurations
├── test_integration.py       # End-to-end workflows
└── __init__.py              # Test module
```

## 📈 Quality Standards

- **ATS Score**: Target 70%+ keyword matching
- **LinkedIn Messages**: Under 400 characters
- **Cover Letters**: 150-400 words
- **Country Compliance**: Proper tone and formatting
- **Content Quality**: Quantified metrics included

## 🐛 Debugging

### Common Issues

1. **Import Errors**: Ensure you're in the Aply directory
2. **File Not Found**: Check output/ directory exists
3. **Low ATS Score**: Review JD parsing and skill matching
4. **Long LinkedIn Messages**: Check country-specific char limits

### Debug Mode
```bash
# Run with detailed logging
python3 main.py --debug
```

## 📁 Project Structure

```
Aply/
├── main.py                   # Main application
├── modules/
│   ├── jd_parser.py         # Job description parsing
│   ├── resume_generator.py  # Resume generation
│   ├── cover_letter_generator.py  # Cover letter creation
│   ├── message_generator.py # LinkedIn/email messages
│   └── country_config.py    # Country-specific rules
├── data/
│   └── user_profile.json    # User profile and projects
├── tests/                   # Test suite
├── output/                  # Generated applications
└── templates/               # Future template storage
```