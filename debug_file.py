#!/usr/bin/env python3
"""
Debug script for WhatsApp chat files
Run this script to analyze your chat file and identify issues
"""

import sys
import re
import pandas as pd

def analyze_file(file_path):
    """Analyze a WhatsApp chat file and show detailed information"""
    
    print("🔍 WhatsApp Chat File Analyzer")
    print("=" * 50)
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()
        
        print(f"📁 File: {file_path}")
        print(f"📊 File size: {len(data)} characters")
        print(f"📄 Total lines: {len(data.split(chr(10)))}")
        
        # Show first few lines
        lines = data.split('\n')[:5]
        print("\n📝 First 5 lines:")
        for i, line in enumerate(lines, 1):
            print(f"  {i}: {line}")
        
        # Check for common patterns
        patterns = {
            'date_12h': r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M\s-\s',
            'date_24h': r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s',
            'date_full': r'\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\s-\s',
            'date_iso': r'\d{4}-\d{1,2}-\d{1,2},\s\d{1,2}:\d{2}\s-\s',
            'user_pattern': r'[^:]+:\s',
        }
        
        print("\n🔍 Pattern Analysis:")
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, data)
            print(f"  {pattern_name}: {len(matches)} matches")
            if matches:
                print(f"    Examples: {matches[:2]}")
        
        # Try to extract messages
        print("\n📨 Message Extraction Test:")
        
        # Test different patterns
        test_patterns = [
            (r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M\s-\s', '12-hour format'),
            (r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s', '24-hour format'),
            (r'\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\s-\s', 'full year format'),
        ]
        
        for pattern, desc in test_patterns:
            messages = re.split(pattern, data)[1:]
            dates = re.findall(pattern, data)
            print(f"  {desc}: {len(messages)} messages, {len(dates)} dates")
            
            if messages and len(messages) > 0:
                # Show first message structure
                first_msg = messages[0].strip()
                print(f"    First message: {first_msg[:100]}...")
                
                # Check user extraction
                user_match = re.match(r'^([^:]+):\s*(.*)', first_msg)
                if user_match:
                    print(f"    User: '{user_match.group(1)}'")
                    print(f"    Message: '{user_match.group(2)[:50]}...'")
                else:
                    print(f"    No user pattern found in first message")
        
        # Check for potential issues
        print("\n⚠️  Potential Issues:")
        
        if len(data.strip()) == 0:
            print("  ❌ File is empty")
        
        if not any(re.search(pattern, data) for pattern in patterns.values()):
            print("  ❌ No date patterns found")
        
        # Check encoding issues
        try:
            data.encode('utf-8')
        except UnicodeEncodeError:
            print("  ❌ Encoding issues detected")
        
        # Check for very long lines (might indicate formatting issues)
        long_lines = [line for line in data.split('\n') if len(line) > 1000]
        if long_lines:
            print(f"  ⚠️  {len(long_lines)} very long lines found (might cause issues)")
        
        print("\n✅ Analysis complete!")
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
    except Exception as e:
        print(f"❌ Error analyzing file: {str(e)}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python debug_file.py <path_to_whatsapp_chat.txt>")
        print("Example: python debug_file.py chat_export.txt")
        sys.exit(1)
    
    file_path = sys.argv[1]
    analyze_file(file_path)

if __name__ == "__main__":
    main() 