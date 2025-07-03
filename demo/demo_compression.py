#!/usr/bin/env python3
"""
Demonstration script for Data Compression functionality in Bills Tracker application.

This script demonstrates:
- How to use the compression features
- Compression effectiveness on different data types
- Integration with the main application
- Best practices for data compression
"""

import os
import sys
import json
import tempfile
import shutil
from datetime import datetime

# Add the parent directory to the path to import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from data_compression import DataCompressor
    print("✅ DataCompressor imported successfully")
except ImportError as e:
    print(f"❌ Failed to import DataCompressor: {e}")
    sys.exit(1)

def demo_compression_methods():
    """Demonstrate different compression methods."""
    print("🗜️ Data Compression Methods Demonstration")
    print("=" * 50)
    
    compressor = DataCompressor()
    
    # Create sample data with different characteristics
    sample_data = {
        'text_data': 'This is a sample text that will be compressed. ' * 50,
        'numbers': list(range(1000)),
        'repetitive_data': ['repeated_item'] * 100,
        'metadata': {
            'created': datetime.now().isoformat(),
            'demo_type': 'compression_methods',
            'version': '1.0'
        }
    }
    
    # Save sample data
    sample_file = "demo_sample_data.json"
    with open(sample_file, 'w') as f:
        json.dump(sample_data, f, indent=2)
    
    original_size = os.path.getsize(sample_file)
    print(f"Sample data file: {sample_file}")
    print(f"Original size: {original_size:,} bytes ({original_size / 1024:.1f} KB)")
    print()
    
    # Test each compression method
    methods = ['gzip', 'lzma', 'zlib']
    results = {}
    
    for method in methods:
        print(f"Testing {method.upper()} compression...")
        
        success, compressed_path, stats = compressor.compress_file(sample_file, method)
        
        if success:
            results[method] = stats
            print(f"  ✅ Compressed size: {stats['compressed_size']:,} bytes")
            print(f"  ✅ Compression ratio: {stats['compression_ratio']:.1f}%")
            print(f"  ✅ Compression time: {stats['compression_time']:.2f} seconds")
            print(f"  ✅ Space saved: {stats['original_size'] - stats['compressed_size']:,} bytes")
            
            # Clean up compressed file
            os.remove(compressed_path)
        else:
            print(f"  ❌ Compression failed: {stats.get('error', 'Unknown error')}")
        print()
    
    # Show comparison
    print("📊 Compression Method Comparison:")
    print("-" * 40)
    print(f"{'Method':<8} {'Size (KB)':<12} {'Ratio %':<10} {'Time (s)':<10}")
    print("-" * 40)
    
    for method in methods:
        if method in results:
            stats = results[method]
            print(f"{method.upper():<8} {stats['compressed_size']/1024:<12.1f} {stats['compression_ratio']:<10.1f} {stats['compression_time']:<10.2f}")
    
    print()
    
    # Find best method
    best_method = None
    best_ratio = 0
    for method, stats in results.items():
        if stats['compression_ratio'] > best_ratio:
            best_ratio = stats['compression_ratio']
            best_method = method
    
    if best_method:
        print(f"🏆 Best compression method: {best_method.upper()} ({best_ratio:.1f}% ratio)")
    
    # Clean up
    os.remove(sample_file)
    print("\n✅ Compression methods demonstration completed")

def demo_database_compression():
    """Demonstrate database compression."""
    print("\n🗜️ Database Compression Demonstration")
    print("=" * 50)
    
    compressor = DataCompressor()
    
    # Check if database exists
    db_file = "bills_tracker.db"
    if not os.path.exists(db_file):
        print(f"Database file '{db_file}' not found.")
        print("Creating a sample database for demonstration...")
        
        # Create a sample database
        import sqlite3
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Create bills table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                due_date TEXT NOT NULL,
                billing_cycle TEXT,
                reminder_days INTEGER,
                web_page TEXT,
                login_info TEXT,
                password TEXT,
                paid INTEGER DEFAULT 0,
                company_email TEXT,
                support_phone TEXT,
                billing_phone TEXT,
                customer_service_hours TEXT,
                account_number TEXT,
                reference_id TEXT,
                support_chat_url TEXT,
                mobile_app TEXT
            )
        ''')
        
        # Insert sample data
        sample_bills = [
            ('Netflix Subscription', '2024-12-15', 'monthly', 7, 'https://netflix.com', 'user@example.com', 'password123', 0, 'support@netflix.com', '1-800-NETFLIX', '1-800-BILLING', '24/7', 'ACC123456', 'REF789', 'https://help.netflix.com', 'Netflix App'),
            ('Electric Bill', '2024-12-20', 'monthly', 5, 'https://electriccompany.com', 'user@example.com', 'password456', 0, 'support@electric.com', '1-800-ELECTRIC', '1-800-BILLING', '8AM-6PM', 'ACC789012', 'REF456', 'https://help.electric.com', 'Electric App'),
            ('Internet Service', '2024-12-25', 'monthly', 3, 'https://internetprovider.com', 'user@example.com', 'password789', 0, 'support@internet.com', '1-800-INTERNET', '1-800-BILLING', '9AM-5PM', 'ACC345678', 'REF123', 'https://help.internet.com', 'Internet App'),
        ]
        
        for bill in sample_bills:
            cursor.execute('''
                INSERT INTO bills (
                    name, due_date, billing_cycle, reminder_days, web_page,
                    login_info, password, paid, company_email, support_phone,
                    billing_phone, customer_service_hours, account_number,
                    reference_id, support_chat_url, mobile_app
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', bill)
        
        conn.commit()
        conn.close()
        print("Sample database created successfully!")
    
    # Analyze database compression
    print(f"Analyzing compression for database: {db_file}")
    analysis = compressor.analyze_compression_effectiveness(db_file)
    
    if 'error' not in analysis:
        print(f"Database size: {analysis['original_size']:,} bytes ({analysis['original_size'] / 1024:.1f} KB)")
        print(f"Best compression method: {analysis.get('best_method', 'None')}")
        print(f"Best compression ratio: {analysis.get('best_compression_ratio', 0):.1f}%")
        
        # Show detailed analysis
        print("\nDetailed compression analysis:")
        for method, data in analysis['methods'].items():
            if 'error' not in data:
                print(f"  {method.upper()}: {data['compression_ratio']:.1f}% ratio, {data['compression_time']:.2f}s")
        
        # Demonstrate actual compression
        if analysis.get('best_method'):
            print(f"\nDemonstrating {analysis['best_method'].upper()} compression...")
            success, compressed_path, stats = compressor.compress_database(
                db_file, analysis['best_method'], backup_original=False
            )
            
            if success:
                print(f"✅ Database compressed successfully!")
                print(f"  Compressed file: {compressed_path}")
                print(f"  Compression ratio: {stats['compression_ratio']:.1f}%")
                print(f"  Space saved: {stats['original_size'] - stats['compressed_size']:,} bytes")
                
                # Show file sizes
                compressed_size = os.path.getsize(compressed_path)
                print(f"  Original: {stats['original_size']:,} bytes")
                print(f"  Compressed: {compressed_size:,} bytes")
                
                # Clean up
                os.remove(compressed_path)
                print("  Compressed file removed (demo only)")
            else:
                print(f"❌ Compression failed: {stats.get('error', 'Unknown error')}")
    
    print("\n✅ Database compression demonstration completed")

def demo_backup_compression():
    """Demonstrate backup directory compression."""
    print("\n🗜️ Backup Directory Compression Demonstration")
    print("=" * 50)
    
    compressor = DataCompressor()
    
    # Create sample backup files
    backup_dir = "demo_backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Create sample backup files
    sample_backups = [
        {
            'filename': 'bills_backup_20241201_120000.json',
            'data': {
                'bills': [
                    {'name': 'Sample Bill 1', 'due_date': '2024-12-15', 'amount': 100.00},
                    {'name': 'Sample Bill 2', 'due_date': '2024-12-20', 'amount': 250.50},
                    {'name': 'Sample Bill 3', 'due_date': '2024-12-25', 'amount': 75.25}
                ],
                'backup_date': '2024-12-01T12:00:00',
                'total_bills': 3
            }
        },
        {
            'filename': 'bills_backup_20241202_120000.json',
            'data': {
                'bills': [
                    {'name': 'Sample Bill 1', 'due_date': '2024-12-15', 'amount': 100.00},
                    {'name': 'Sample Bill 2', 'due_date': '2024-12-20', 'amount': 250.50},
                    {'name': 'Sample Bill 3', 'due_date': '2024-12-25', 'amount': 75.25},
                    {'name': 'Sample Bill 4', 'due_date': '2024-12-30', 'amount': 150.00}
                ],
                'backup_date': '2024-12-02T12:00:00',
                'total_bills': 4
            }
        },
        {
            'filename': 'bills_backup_20241203_120000.json',
            'data': {
                'bills': [
                    {'name': 'Sample Bill 1', 'due_date': '2024-12-15', 'amount': 100.00},
                    {'name': 'Sample Bill 2', 'due_date': '2024-12-20', 'amount': 250.50},
                    {'name': 'Sample Bill 3', 'due_date': '2024-12-25', 'amount': 75.25},
                    {'name': 'Sample Bill 4', 'due_date': '2024-12-30', 'amount': 150.00},
                    {'name': 'Sample Bill 5', 'due_date': '2025-01-05', 'amount': 200.00}
                ],
                'backup_date': '2024-12-03T12:00:00',
                'total_bills': 5
            }
        }
    ]
    
    for backup in sample_backups:
        file_path = os.path.join(backup_dir, backup['filename'])
        with open(file_path, 'w') as f:
            json.dump(backup['data'], f, indent=2)
    
    # Show backup directory info
    backup_files = [f for f in os.listdir(backup_dir) if os.path.isfile(os.path.join(backup_dir, f))]
    total_size = sum(os.path.getsize(os.path.join(backup_dir, f)) for f in backup_files)
    
    print(f"Created {len(backup_files)} sample backup files")
    print(f"Total size: {total_size:,} bytes ({total_size / 1024:.1f} KB)")
    print(f"Files: {', '.join(backup_files)}")
    
    # Demonstrate compression
    print(f"\nCompressing backup directory with GZIP...")
    results = compressor.compress_backup_directory(backup_dir, 'gzip', delete_originals=False)
    
    if 'error' not in results:
        print(f"✅ Backup compression completed!")
        print(f"  Files processed: {results['files_processed']}")
        print(f"  Files compressed: {results['files_compressed']}")
        print(f"  Original size: {results['total_original_size']:,} bytes")
        print(f"  Compressed size: {results['total_compressed_size']:,} bytes")
        print(f"  Compression ratio: {results['compression_ratio']:.1f}%")
        print(f"  Space saved: {results['total_original_size'] - results['total_compressed_size']:,} bytes")
        
        # Show compressed files
        compressed_files = [f for f in os.listdir(backup_dir) if f.endswith('.gz')]
        print(f"  Compressed files: {', '.join(compressed_files)}")
        
        # Clean up compressed files
        for filename in compressed_files:
            os.remove(os.path.join(backup_dir, filename))
        print("  Compressed files removed (demo only)")
    else:
        print(f"❌ Backup compression failed: {results['error']}")
    
    # Clean up demo directory
    shutil.rmtree(backup_dir)
    print("\n✅ Backup compression demonstration completed")

def demo_compression_analysis():
    """Demonstrate compression analysis features."""
    print("\n🗜️ Compression Analysis Demonstration")
    print("=" * 50)
    
    compressor = DataCompressor()
    
    # Create different types of data files
    test_files = {
        'repetitive_data.json': {
            'data': {'repetitive_string': 'This is a very repetitive string. ' * 1000},
            'description': 'Highly repetitive data (should compress well)'
        },
        'random_data.json': {
            'data': {'random_numbers': [hash(str(i)) % 10000 for i in range(1000)]},
            'description': 'Random data (should compress poorly)'
        },
        'mixed_data.json': {
            'data': {
                'text': 'Some text data that might compress well. ' * 50,
                'numbers': list(range(100)),
                'mixed': ['item'] * 50 + list(range(50))
            },
            'description': 'Mixed data (moderate compression)'
        }
    }
    
    for filename, file_info in test_files.items():
        print(f"\n📄 Analyzing: {filename}")
        print(f"   Description: {file_info['description']}")
        
        # Create file
        with open(filename, 'w') as f:
            json.dump(file_info['data'], f, indent=2)
        
        # Analyze compression
        analysis = compressor.analyze_compression_effectiveness(filename)
        
        if 'error' not in analysis:
            print(f"   Original size: {analysis['original_size']:,} bytes")
            print(f"   Best method: {analysis.get('best_method', 'None')}")
            print(f"   Best ratio: {analysis.get('best_compression_ratio', 0):.1f}%")
            
            # Show method comparison
            for method, data in analysis['methods'].items():
                if 'error' not in data:
                    print(f"     {method.upper()}: {data['compression_ratio']:.1f}% ratio")
        
        # Clean up
        os.remove(filename)
    
    print("\n✅ Compression analysis demonstration completed")

def demo_integration_with_app():
    """Demonstrate how compression integrates with the main app."""
    print("\n🗜️ Integration with Bills Tracker Application")
    print("=" * 50)
    
    print("The data compression feature is fully integrated into the Bills Tracker application.")
    print("Here's how to use it:")
    print()
    
    print("1. 📱 From the main menu, select option 13: 'Data Compression'")
    print("2. 🗜️ Choose from the compression menu options:")
    print("   • Compress database - Reduce database file size")
    print("   • Compress backup directory - Save space on backup files")
    print("   • Compress individual files - Compress specific files")
    print("   • Analyze compression effectiveness - Find best method")
    print("   • View compression information - Get file details")
    print("   • Decompress files - Restore compressed files")
    print()
    
    print("3. 🎯 Best practices:")
    print("   • Use compression for large datasets to save storage space")
    print("   • Analyze compression effectiveness before compressing")
    print("   • Keep original files when possible (for safety)")
    print("   • Use GZIP for fast compression, LZMA for best ratio")
    print("   • Compress backup files to save significant space")
    print()
    
    print("4. 🔧 Technical features:")
    print("   • Multiple compression algorithms (GZIP, LZMA, ZLIB)")
    print("   • Automatic compression level optimization")
    print("   • Progress tracking for large operations")
    print("   • Compression ratio analysis")
    print("   • Automatic decompression for data access")
    print("   • Batch compression for multiple files")
    print()
    
    print("5. 💾 Storage benefits:")
    print("   • Database files: 20-80% size reduction")
    print("   • Backup files: 30-90% size reduction")
    print("   • JSON files: 40-95% size reduction")
    print("   • Text files: 50-98% size reduction")
    print()
    
    print("✅ Integration demonstration completed")

def main():
    """Run all compression demonstrations."""
    print("🗜️ Bills Tracker Data Compression Demonstration")
    print("=" * 60)
    
    demonstrations = [
        demo_compression_methods,
        demo_database_compression,
        demo_backup_compression,
        demo_compression_analysis,
        demo_integration_with_app
    ]
    
    for demo in demonstrations:
        try:
            demo()
            print("\n" + "=" * 60)
        except Exception as e:
            print(f"❌ Demonstration failed: {e}")
            print("\n" + "=" * 60)
    
    print("🎉 All compression demonstrations completed!")
    print("\n💡 To use compression in the main application:")
    print("   1. Run: python bills-tracker.py")
    print("   2. Select option 13: Data Compression")
    print("   3. Choose your desired compression operation")

if __name__ == "__main__":
    main() 