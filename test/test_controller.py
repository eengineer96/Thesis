import sys
import pytest
from unittest.mock import MagicMock, patch
from PIL import Image
from pathlib import Path
import numpy as np

"""Picamera2 is not available for Windows so it needs a workaround to get it working!"""
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.modules['picamera2'] = MagicMock()

from app.controller import Controller 

@pytest.fixture
def controller():
    """Create a Controller instance for testing"""
    telegram_notifier = MagicMock()
    gui = MagicMock()
    printer = MagicMock()
    model_evaluator = MagicMock()
    with patch('app.controller.Picamera2') as mock_camera:
        controller = Controller(
            telegram_notifier,
            gui,
            printer,
            model_evaluator
        )

    return controller

def test_evaluate_model_with_NOK_test_image(controller):
    """Test model evaluation with OK image file"""
    test_image_path = Path(__file__).parent / "test_images" / "nok.jpg"
    test_image = Image.open(test_image_path).convert("RGB")
    test_array = np.array(test_image)
    
    controller.model_evaluator.evaluate.return_value = ("NOK", 95.5)
    
    controller.get_camera_frame = MagicMock(return_value=test_array)

    controller.evaluate_model()
    
    assert controller.result == "NOK"
    assert controller.confidence == 95.5

def test_evaluate_model_with_OK_test_image(controller):
    """Test model evaluation with NOK image file"""
    test_image_path = Path(__file__).parent / "test_images" / "ok.jpg"
    test_image = Image.open(test_image_path).convert("RGB")
    test_array = np.array(test_image)
    
    controller.model_evaluator.evaluate.return_value = ("OK", 95.5)
    
    controller.get_camera_frame = MagicMock(return_value=test_array)
    
    controller.evaluate_model()
    
    assert controller.result == "OK"
    assert controller.confidence == 95.5

def test_calculate_nok_counter_increments(controller):
    """Test that NOK counter increments when anomaly is detected with high confidence"""
    controller.result = "NOK"
    controller.confidence = 95
    controller.tolerance = 90
    controller.nok_counter = 0
    
    controller.calculate_nok_counter()
    
    assert controller.nok_counter == 1

def test_calculate_nok_counter_resets_when_OK(controller):
    """Test that NOK counter resets when result is OK"""
    controller.result = "OK"
    controller.confidence = 95
    controller.nok_counter = 5
    
    controller.calculate_nok_counter()
    
    assert controller.nok_counter == 0

def test_calculate_nok_counter_resets_when_confidence_is_low(controller):
    """Test that NOK counter resets when confidence falls below tolerance"""
    controller.result = "NOK"
    controller.confidence = 85
    controller.tolerance = 90
    controller.nok_counter = 5
    
    controller.calculate_nok_counter()
    
    assert controller.nok_counter == 0

def test_reset_notification_flag(controller):
    """Test notification flag is reset"""
    controller._notification_sent_flag = True
    
    controller.reset_notification_flag()
    
    assert controller._notification_sent_flag is False

