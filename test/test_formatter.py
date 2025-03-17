import sys
import pytest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from app.formatter import format_data

@pytest.fixture
def sample_status():
    """Sample status response"""
    return {
        'params': {
            'fanPercent': [75]
        },
        'temps': {
            'extra': [
                {'temp': 60},   # bed 
                {'temp': 210},  # hotend 
                {'temp': 35},   # chamber temp
                {'temp': 40},   # chamber humidity
                {'temp': 28},   # electronics temp
                {'temp': 30},   # electronics humidity
            ]
        }
    }

def test_format_data_basic_functionality(sample_status):
    """Test that format_data correctly formats all values."""
    mode = True
    result = "OK"
    confidence = 95.75
    nok_counter = 0
    
    formatted_text = format_data(sample_status, mode, result, confidence, nok_counter)
    
    assert "Fan percentage: 75%" in formatted_text
    assert "Bed temperature: 60C" in formatted_text
    assert "Hotend temperature: 210C" in formatted_text
    assert "Chamber temperature: 35C" in formatted_text
    assert "Chamber humidity: 40%" in formatted_text
    assert "Electronics temperature: 28C" in formatted_text
    assert "Electronics humidity: 30%" in formatted_text
    assert "Evaluation mode is set to automatic" in formatted_text
    assert "Status is 'OK'" in formatted_text
    assert "with a confidence of 95.75%" in formatted_text
    assert "Anomaly is present since 0 evaluation" in formatted_text
