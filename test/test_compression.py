#!/usr/bin/env python3
"""
Test script for Data Compression functionality in Bills Tracker application.

This script tests:
- File compression with different algorithms
- Database compression
- Backup directory compression
- Compression analysis
- Decompression functionality
"""

import os
import sys
import tempfile
import shutil
import json
from datetime import datetime

# Add the parent directory to the path to import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from data_compression import DataCompressor
    print("✅ DataCompressor imported successfully")
except ImportError as e:
    print(f"❌ Failed to import DataCompressor: {e}")
    sys.exit(1)

def create_test_data():
    """Create test data for compression testing."""
    test_data = {
        'bills': [
            {
                'name': 'Test Bill 1',
                'due_date': '2024-12-31',
                'amount': 100.00,
                'description': 'This is a test bill for compression testing'
            },
            {
                'name': 'Test Bill 2',
                'due_date': '2024-12-15',
                'amount': 250.50,
                'description': 'Another test bill with different data'
            }
        ],
        'metadata': {
            'created': datetime.now().isoformat(),
            'test_type': 'compression_test',
            'version': '1.0'
        }
    }
    return test_data

def test_basic_compression():
    """Test basic file compression functionality."""
    print("\n🧪 Testing Basic Compression")
    print("=" * 40)
    
    compressor = DataCompressor()
    
    # Create test file
    test_data = create_test_data()
    test_file = "test_compression_data.json"
    
    with open(test_file, 'w') as f:
        json.dump(test_data, f, indent=2)
    
    original_size = os.path.getsize(test_file)
    print(f"Created test file: {test_file} ({original_size:,} bytes)")
    
    # Test each compression method
    methods = ['gzip', 'lzma', 'zlib']
    
    for method in methods:
        print(f"\nTesting {method.upper()} compression...")
        
        success, compressed_path, stats = compressor.compress_file(test_file, method)
        
        if success:
            print(f"  ✅ {method.upper()} compression successful")
            print(f"  Compressed size: {stats['compressed_size']:,} bytes")
            print(f"  Compression ratio: {stats['compression_ratio']:.1f}%")
            print(f"  Compression time: {stats['compression_time']:.2f} seconds")
            
            # Test decompression
            success_decompress, decompressed_path = compressor.decompress_file(compressed_path)
            if success_decompress:
                print(f"  ✅ Decompression successful: {decompressed_path}")
                
                # Verify file integrity
                with open(test_file, 'r') as f1, open(decompressed_path, 'r') as f2:
                    if f1.read() == f2.read():
                        print(f"  ✅ File integrity verified")
                    else:
                        print(f"  ❌ File integrity check failed")
                
                # Clean up decompressed file
                os.remove(decompressed_path)
            else:
                print(f"  ❌ Decompression failed: {decompressed_path}")
            
            # Clean up compressed file
            os.remove(compressed_path)
        else:
            print(f"  ❌ {method.upper()} compression failed: {stats.get('error', 'Unknown error')}")
    
    # Clean up test file
    os.remove(test_file)
    print(f"\n✅ Basic compression tests completed")

def test_compression_analysis():
    """Test compression analysis functionality."""
    print("\n🧪 Testing Compression Analysis")
    print("=" * 40)
    
    compressor = DataCompressor()
    
    # Create test file with repetitive data (good for compression)
    repetitive_data = {
        'repetitive_string': 'This is a very repetitive string that should compress well. ' * 100,
        'numbers': list(range(1000)),
        'metadata': {
            'test': 'compression_analysis',
            'timestamp': datetime.now().isoformat()
        }
    }
    
    test_file = "test_analysis_data.json"
    with open(test_file, 'w') as f:
        json.dump(repetitive_data, f, indent=2)
    
    print(f"Created test file for analysis: {test_file}")
    
    # Analyze compression effectiveness
    analysis = compressor.analyze_compression_effectiveness(test_file)
    
    if 'error' not in analysis:
        print(f"Original size: {analysis['original_size']:,} bytes")
        print(f"Best method: {analysis.get('best_method', 'None')}")
        print(f"Best ratio: {analysis.get('best_compression_ratio', 0):.1f}%")
        
        print("\nDetailed analysis:")
        for method, data in analysis['methods'].items():
            if 'error' not in data:
                print(f"  {method.upper()}: {data['compression_ratio']:.1f}% ratio, {data['compression_time']:.2f}s")
            else:
                print(f"  {method.upper()}: {data['error']}")
        
        print("✅ Compression analysis test completed")
    else:
        print(f"❌ Analysis failed: {analysis['error']}")
    
    # Clean up
    os.remove(test_file)

def test_batch_compression():
    """Test batch compression functionality."""
    print("\n🧪 Testing Batch Compression")
    print("=" * 40)
    
    compressor = DataCompressor()
    
    # Create multiple test files
    test_files = []
    for i in range(3):
        test_data = {
            'file_number': i,
            'content': f'This is test file number {i} with some data for compression testing',
            'timestamp': datetime.now().isoformat()
        }
        
        filename = f"test_batch_{i}.json"
        with open(filename, 'w') as f:
            json.dump(test_data, f, indent=2)
        test_files.append(filename)
    
    print(f"Created {len(test_files)} test files for batch compression")
    
    # Test batch compression
    results = compressor.batch_compress(test_files, 'gzip', delete_originals=False)
    
    print(f"Batch compression results:")
    print(f"  Total files: {results['total_files']}")
    print(f"  Successful: {results['successful']}")
    print(f"  Failed: {results['failed']}")
    print(f"  Overall ratio: {results.get('overall_compression_ratio', 0):.1f}%")
    
    if results['errors']:
        print(f"  Errors: {len(results['errors'])}")
        for error in results['errors']:
            print(f"    • {error}")
    
    # Clean up
    for filename in test_files:
        if os.path.exists(filename):
            os.remove(filename)
        compressed_filename = filename + '.gz'
        if os.path.exists(compressed_filename):
            os.remove(compressed_filename)
    
    print("✅ Batch compression test completed")

def test_compression_info():
    """Test compression information functionality."""
    print("\n🧪 Testing Compression Information")
    print("=" * 40)
    
    compressor = DataCompressor()
    
    # Create a test file and compress it
    test_data = {'test': 'compression_info_test', 'data': 'some test data'}
    test_file = "test_info.json"
    
    with open(test_file, 'w') as f:
        json.dump(test_data, f, indent=2)
    
    # Compress the file
    success, compressed_path, _ = compressor.compress_file(test_file, 'gzip')
    
    if success:
        # Test getting compression info
        info = compressor.get_compression_info(compressed_path)
        
        print(f"Compression info for {compressed_path}:")
        print(f"  File size: {info['file_size']:,} bytes")
        print(f"  Is compressed: {info['is_compressed']}")
        print(f"  Method: {info.get('compression_method', 'None')}")
        
        if info['original_size']:
            print(f"  Original size: {info['original_size']:,} bytes")
            print(f"  Compression ratio: {info['compression_ratio']:.1f}%")
        
        # Test getting info for uncompressed file
        uncompressed_info = compressor.get_compression_info(test_file)
        print(f"\nInfo for uncompressed file {test_file}:")
        print(f"  Is compressed: {uncompressed_info['is_compressed']}")
        
        print("✅ Compression info test completed")
        
        # Clean up
        os.remove(compressed_path)
    else:
        print("❌ Failed to create compressed file for testing")
    
    os.remove(test_file)

def test_database_compression():
    """Test database compression functionality."""
    print("\n🧪 Testing Database Compression")
    print("=" * 40)
    
    compressor = DataCompressor()
    
    # Check if database exists
    db_file = "bills_tracker.db"
    if not os.path.exists(db_file):
        print(f"Database file '{db_file}' not found. Skipping database compression test.")
        return
    
    print(f"Testing compression on existing database: {db_file}")
    
    # Analyze compression effectiveness
    analysis = compressor.analyze_compression_effectiveness(db_file)
    
    if 'error' not in analysis:
        print(f"Database size: {analysis['original_size']:,} bytes")
        print(f"Best compression method: {analysis.get('best_method', 'None')}")
        print(f"Best compression ratio: {analysis.get('best_compression_ratio', 0):.1f}%")
        
        # Test actual compression (without deleting original)
        if analysis.get('best_method'):
            success, compressed_path, stats = compressor.compress_database(
                db_file, analysis['best_method'], backup_original=False
            )
            
            if success:
                print(f"✅ Database compression successful")
                print(f"  Compressed file: {compressed_path}")
                print(f"  Compression ratio: {stats['compression_ratio']:.1f}%")
                
                # Clean up compressed file
                os.remove(compressed_path)
            else:
                print(f"❌ Database compression failed: {stats.get('error', 'Unknown error')}")
        
        print("✅ Database compression test completed")
    else:
        print(f"❌ Database analysis failed: {analysis['error']}")

def test_backup_directory_compression():
    """Test backup directory compression functionality."""
    print("\n🧪 Testing Backup Directory Compression")
    print("=" * 40)
    
    compressor = DataCompressor()
    
    # Check if backup directory exists
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        print(f"Backup directory '{backup_dir}' not found. Skipping backup compression test.")
        return
    
    print(f"Testing compression on backup directory: {backup_dir}")
    
    # Count files and calculate total size
    backup_files = [f for f in os.listdir(backup_dir) if os.path.isfile(os.path.join(backup_dir, f))]
    total_size = sum(os.path.getsize(os.path.join(backup_dir, f)) for f in backup_files)
    
    print(f"Backup directory contains {len(backup_files)} files")
    print(f"Total size: {total_size:,} bytes")
    
    if backup_files:
        # Test compression (without deleting originals)
        results = compressor.compress_backup_directory(backup_dir, 'gzip', delete_originals=False)
        
        if 'error' not in results:
            print(f"✅ Backup directory compression completed")
            print(f"  Files processed: {results['files_processed']}")
            print(f"  Files compressed: {results['files_compressed']}")
            print(f"  Compression ratio: {results['compression_ratio']:.1f}%")
            
            # Clean up compressed files
            for filename in backup_files:
                compressed_filename = os.path.join(backup_dir, filename + '.gz')
                if os.path.exists(compressed_filename):
                    os.remove(compressed_filename)
            
            print("✅ Backup directory compression test completed")
        else:
            print(f"❌ Backup compression failed: {results['error']}")
    else:
        print("No files found in backup directory")

def main():
    """Run all compression tests."""
    print("🧪 Bills Tracker Data Compression Tests")
    print("=" * 50)
    
    tests = [
        test_basic_compression,
        test_compression_analysis,
        test_batch_compression,
        test_compression_info,
        test_database_compression,
        test_backup_directory_compression
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL COMPRESSION TESTS PASSED!")
    else:
        print(f"⚠️  {total - passed} tests failed.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 