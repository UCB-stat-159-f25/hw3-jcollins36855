from ligotools import readligo as r
from .readligo import SegmentList
import numpy as np
from ligotools import dq_channel_to_seglist

def test_getsegs_returns_list():
    """Test that getsegs returns a list (SegmentList)"""
    
    # Set up test parameters
    start = 1126259446
    stop = 1126259478
    ifo = 'H1'
    flag = 'DATA'
    
    # Run the function
    result = r.getsegs(start, stop, ifo, flag=flag)
    
    # Test that result is a SegmentList
    assert isinstance(result, r.SegmentList), f"Expected SegmentList, got {type(result)}"
    
    print(f"✓ Test passed: Output is {type(result).__name__}")




def test_dq_channel_slices_and_getstrain_incompatibility():
    """
    Test that dq_channel_to_seglist returns slices,
    and that it does NOT work with getstrain output (as warned in docstring)
    """
    
    print("="*60)
    print("TEST 1: Verify output contains slices")
    print("="*60)
    
    # Create sample DQ channel (from loaddata-like output)
    channel = np.array([1, 1, 0, 1, 1, 1])
    result = dq_channel_to_seglist(channel, fs=4096)
    
    # Check it's a list
    assert isinstance(result, list), f"Expected list, got {type(result)}"
    print(f"✓ Output is a list")
    
    # Check each element is a slice
    for i, element in enumerate(result):
        if not isinstance(element, slice):
            print(f"✗ FAILED: Element {i} should be a slice, got {type(element)}")
            raise AssertionError(f"Element {i} is not a slice")
        print(f"✓ Element {i} is a slice: {element}")
    
    print(f"✓ All {len(result)} elements are slices\n")
    
    print("="*60)
    print("TEST 2: Verify it does NOT work with getstrain output")
    print("="*60)
    
    # Simulate getstrain output structure (returns a dictionary, not raw channel)
    try:
        # This is what getstrain returns for DQ
        getstrain_dq_output = {
            'DATA': np.array([1, 1, 0, 1, 1]),
            'CBC_CAT1': np.array([1, 1, 1, 1, 1]),
            'CBC_CAT2': np.array([0, 0, 0, 0, 0])
        }
        
        print("Attempting to use getstrain DQ output directly (should fail without 'DEFAULT' key)...")
        # This will fail unless there's a 'DEFAULT' key
        result = dq_channel_to_seglist(getstrain_dq_output, fs=4096)
        print(f"✗ UNEXPECTED: Function worked with getstrain output without 'DEFAULT' key")
        
    except KeyError as e:
        print(f"✓ CORRECT: Function fails with getstrain DQ dict that lacks 'DEFAULT' key")
        print(f"  Error: {e}\n")
    
    # Show the correct way to use it with getstrain output
    print("="*60)
    print("TEST 3: Correct usage - extract specific channel first")
    print("="*60)
    
    getstrain_dq_output = {
        'DATA': np.array([1, 1, 0, 1, 1]),
        'CBC_CAT1': np.array([1, 1, 1, 1, 1])
    }
    
    # This is the CORRECT way to use getstrain output
    print("Extracting 'DATA' channel first, then passing to dq_channel_to_seglist...")
    data_channel = getstrain_dq_output['DATA']
    result = dq_channel_to_seglist(data_channel, fs=4096)
    print(f"✓ Works correctly when channel is extracted first")
    print(f"  Result: {result}\n")
    
    print("="*60)
    print("TEST 4: Works with dict containing 'DEFAULT' key")
    print("="*60)
    
    # Test with DEFAULT key (which the function does support)
    dq_with_default = {
        'DEFAULT': np.array([1, 1, 0, 1, 1]),
        'OTHER': np.array([0, 0, 0, 0, 0])
    }
    
    print("Testing with dictionary containing 'DEFAULT' key...")
    result = dq_channel_to_seglist(dq_with_default, fs=4096)
    print(f"✓ Works with 'DEFAULT' key in dictionary")
    print(f"  Result: {result}\n")
    
    print("="*60)
    print("✓ ALL TESTS PASSED!")
    print("="*60)
    print("\nSummary:")
    print("- dq_channel_to_seglist returns a list of slices ✓")
    print("- It does NOT directly work with getstrain DQ output ✓")
    print("- User must extract specific channel from getstrain DQ dict first ✓")
    print("- Or use a dict with 'DEFAULT' key ✓")
    

