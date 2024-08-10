"""

"""
# %%
# import tidyxbrl
import sys
import os
import pytest
import pandas as pd 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.tidyxbrl import edgar_frames

# %%
def test_edgar_frames():
    # Test with a valid URL descriptor
    result = edgar_frames(urldescriptor='us-gaap/NonoperatingIncomeExpense/USD/CY2019Q1I')
    assert result is not None, "Result should not be None"
    assert isinstance(result, pd.DataFrame), "Result should be a pandas DataFrame"

    # Test with another valid URL descriptor
    result = edgar_frames(urldescriptor='us-gaap/OperatingIncomeLoss/USD/CY2020Q1I')
    assert result is not None, "Result should not be None"
    assert isinstance(result, pd.DataFrame), "Result should be a pandas DataFrame"


# %%
