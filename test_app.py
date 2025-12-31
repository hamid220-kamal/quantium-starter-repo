"""
Test suite for Soul Foods Pink Morsel Sales Visualizer Dash App.
Uses pytest to verify app layout and components.
"""

import pytest
from app import app


class TestDashApp:
    """Test class for the Dash application."""
    
    def test_header_present(self):
        """Test 1: Verify the header is present in the app layout."""
        # Get the app layout
        layout = app.layout
        
        # Convert layout to string representation to check for content
        layout_str = str(layout)
        
        # Verify the header text is present
        assert 'Soul Foods' in layout_str, "Header 'Soul Foods' should be present in the layout"
        assert 'Pink Morsel Sales Visualizer' in layout_str, "Header subtitle should be present"
    
    def test_visualization_present(self):
        """Test 2: Verify the visualization (chart) is present in the app layout."""
        # Get the app layout
        layout = app.layout
        
        # Convert layout to string representation
        layout_str = str(layout)
        
        # Verify the graph component with correct ID is present
        assert 'sales-line-chart' in layout_str, "Sales line chart component should be present"
        assert 'Graph' in layout_str, "Graph component should be in the layout"
    
    def test_region_picker_present(self):
        """Test 3: Verify the region picker (radio buttons) is present in the app layout."""
        # Get the app layout
        layout = app.layout
        
        # Convert layout to string representation
        layout_str = str(layout)
        
        # Verify the region filter radio items are present
        assert 'region-filter' in layout_str, "Region filter component should be present"
        assert 'RadioItems' in layout_str, "RadioItems component should be in the layout"
        
        # Verify all region options are present
        assert 'north' in layout_str.lower(), "North region option should be present"
        assert 'south' in layout_str.lower(), "South region option should be present"
        assert 'east' in layout_str.lower(), "East region option should be present"
        assert 'west' in layout_str.lower(), "West region option should be present"
        assert 'all' in layout_str.lower(), "All regions option should be present"
