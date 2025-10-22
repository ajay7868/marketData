"""
Test script for Stock Chart Pattern Drawing Tool
Tests the complete workflow: load data → draw pattern → export → clear → import → verify pattern matches
"""
import os
import sys
from datetime import datetime
from data_handler import DataHandler


def test_complete_workflow():
    """Test the complete workflow of the pattern drawing tool."""
    print("=" * 60)
    print("TESTING STOCK CHART PATTERN DRAWING TOOL WORKFLOW")
    print("=" * 60)
    
    # Initialize data handler
    data_handler = DataHandler()
    
    # Test 1: Load market data
    print("\n[TEST 1] Loading market data from 1Day.csv...")
    try:
        market_data = data_handler.load_market_data('1Day.csv')
        print(f"✅ SUCCESS: Loaded {len(market_data)} data points")
        print(f"   Date range: {market_data.index.min()} to {market_data.index.max()}")
        print(f"   Price range: ${market_data['close'].min():.2f} to ${market_data['close'].max():.2f}")
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False
    
    # Test 2: Create sample pattern strokes
    print("\n[TEST 2] Creating sample pattern strokes...")
    try:
        # Create sample strokes (simulating drawn patterns)
        sample_strokes = [
            # Stroke 1: Trend line
            [
                ('03/12/2025 10:00', 560.0),
                ('03/12/2025 10:30', 558.0),
                ('03/12/2025 11:00', 556.0),
                ('03/12/2025 11:30', 554.0)
            ],
            # Stroke 2: Support line
            [
                ('03/12/2025 12:00', 555.0),
                ('03/12/2025 13:00', 555.0),
                ('03/12/2025 14:00', 555.0),
                ('03/12/2025 15:00', 555.0)
            ],
            # Stroke 3: Resistance line
            [
                ('03/12/2025 10:15', 562.0),
                ('03/12/2025 11:15', 562.0),
                ('03/12/2025 12:15', 562.0),
                ('03/12/2025 13:15', 562.0)
            ]
        ]
        
        # Add strokes to data handler
        for stroke in sample_strokes:
            data_handler.add_stroke(stroke)
        
        print(f"✅ SUCCESS: Created {len(sample_strokes)} pattern strokes")
        for i, stroke in enumerate(sample_strokes):
            print(f"   Stroke {i+1}: {len(stroke)} points")
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False
    
    # Test 3: Export patterns to CSV
    print("\n[TEST 3] Exporting patterns to CSV...")
    try:
        export_filename = 'test_pattern_export.csv'
        data_handler.export_pattern_to_csv(sample_strokes, export_filename)
        
        # Verify file was created
        if os.path.exists(export_filename):
            file_size = os.path.getsize(export_filename)
            print(f"✅ SUCCESS: Exported to {export_filename} ({file_size} bytes)")
            
            # Show sample of exported data
            with open(export_filename, 'r') as f:
                lines = f.readlines()[:10]  # First 10 lines
                print("   Sample exported data:")
                for line in lines:
                    print(f"     {line.strip()}")
        else:
            print(f"❌ FAILED: Export file not created")
            return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False
    
    # Test 4: Clear patterns
    print("\n[TEST 4] Clearing patterns...")
    try:
        data_handler.clear_patterns()
        strokes_after_clear = data_handler.get_pattern_strokes()
        
        if len(strokes_after_clear) == 0:
            print("✅ SUCCESS: Patterns cleared successfully")
        else:
            print(f"❌ FAILED: Expected 0 strokes, got {len(strokes_after_clear)}")
            return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False
    
    # Test 5: Import patterns from CSV
    print("\n[TEST 5] Importing patterns from CSV...")
    try:
        imported_strokes = data_handler.import_pattern_from_csv(export_filename)
        
        if len(imported_strokes) == len(sample_strokes):
            print(f"✅ SUCCESS: Imported {len(imported_strokes)} strokes")
        else:
            print(f"❌ FAILED: Expected {len(sample_strokes)} strokes, got {len(imported_strokes)}")
            return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False
    
    # Test 6: Verify pattern matches
    print("\n[TEST 6] Verifying pattern matches...")
    try:
        matches = True
        
        for i, (original, imported) in enumerate(zip(sample_strokes, imported_strokes)):
            if len(original) != len(imported):
                print(f"❌ FAILED: Stroke {i+1} length mismatch")
                matches = False
                break
            
            for j, (orig_point, imp_point) in enumerate(zip(original, imported)):
                if orig_point[0] != imp_point[0] or abs(orig_point[1] - imp_point[1]) > 0.01:
                    print(f"❌ FAILED: Stroke {i+1}, point {j+1} mismatch")
                    print(f"   Original: {orig_point}")
                    print(f"   Imported: {imp_point}")
                    matches = False
                    break
            
            if not matches:
                break
        
        if matches:
            print("✅ SUCCESS: All patterns match perfectly!")
        else:
            print("❌ FAILED: Pattern verification failed")
            return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False
    
    # Test 7: Data structure verification
    print("\n[TEST 7] Verifying CSV structure is compatible with 1Day.csv...")
    try:
        # Read the exported file and check structure
        with open(export_filename, 'r') as f:
            lines = f.readlines()
            
        # Check header
        header = lines[0].strip().split(',')
        expected_header = ['stroke_id', 'datetime', 'open', 'high', 'low', 'close', 'volume']
        
        if header == expected_header:
            print("✅ SUCCESS: CSV structure is compatible with 1Day.csv format")
            print("   Note: Added stroke_id column for pattern stroke identification")
        else:
            print(f"❌ FAILED: Header mismatch")
            print(f"   Expected: {expected_header}")
            print(f"   Got: {header}")
            return False
        
        # Check data format
        sample_data_line = lines[1].strip().split(',')
        if len(sample_data_line) == 7:
            print("✅ SUCCESS: Data format is correct (7 columns including stroke_id)")
        else:
            print(f"❌ FAILED: Data format incorrect ({len(sample_data_line)} columns)")
            return False
        
        # Verify that datetime format matches 1Day.csv
        sample_datetime = sample_data_line[1]  # datetime column
        try:
            datetime.strptime(sample_datetime, '%m/%d/%Y %H:%M')
            print("✅ SUCCESS: Datetime format matches 1Day.csv format")
        except ValueError:
            print(f"❌ FAILED: Datetime format mismatch")
            return False
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        return False
    
    # Cleanup
    print("\n[CLEANUP] Removing test files...")
    try:
        if os.path.exists(export_filename):
            os.remove(export_filename)
            print("✅ SUCCESS: Test files cleaned up")
    except Exception as e:
        print(f"⚠️  WARNING: Could not clean up test files: {str(e)}")
    
    # Final summary
    print("\n" + "=" * 60)
    print("WORKFLOW TEST COMPLETE")
    print("=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("\nThe Stock Chart Pattern Drawing Tool is working correctly:")
    print("• Market data loading: ✅")
    print("• Pattern creation: ✅")
    print("• Pattern export: ✅")
    print("• Pattern clearing: ✅")
    print("• Pattern import: ✅")
    print("• Pattern verification: ✅")
    print("• CSV structure compatibility: ✅")
    print("\nThe tool is ready for use!")
    
    return True


def test_data_handler_functions():
    """Test individual data handler functions."""
    print("\n" + "=" * 60)
    print("TESTING DATA HANDLER FUNCTIONS")
    print("=" * 60)
    
    data_handler = DataHandler()
    
    # Test data summary
    print("\n[TEST] Data summary with no data...")
    summary = data_handler.get_data_summary()
    print(f"Summary: {summary}")
    
    # Test with loaded data
    print("\n[TEST] Data summary with loaded data...")
    try:
        data_handler.load_market_data('1Day.csv')
        summary = data_handler.get_data_summary()
        print(f"Summary: {summary}")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    # Run the complete workflow test
    success = test_complete_workflow()
    
    if success:
        # Run additional function tests
        test_data_handler_functions()
        
        print("\n🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
        print("The Stock Chart Pattern Drawing Tool is ready to use.")
    else:
        print("\n❌ TESTS FAILED!")
        print("Please check the implementation and try again.")
        sys.exit(1)
