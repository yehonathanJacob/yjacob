#!/usr/bin/env python3
"""
Script to extract specific events from Google Calendar ICS export.

Filters events based on:
- Start date between 01-Jan-2025 and 01-Sep-2025
- Event name contains "שיעור פרטי"

Exports to CSV with Event Name, Start Date, and Description.
"""

import csv
import re
from datetime import datetime
from pathlib import Path

try:
    from icalendar import Calendar
except ImportError:
    print("Error: icalendar library is not installed.")
    print("Please install it using: pip install icalendar")
    exit(1)


def extract_payment_method(description):
    """
    Extract payment method from description text within parentheses (...).
    
    Args:
        description: Event description text
        
    Returns:
        Payment method string or empty string if not found
    """
    pattern = r'\(([^)]+)\)'
    matches = re.findall(pattern, description)
    
    # Return the first match if found
    return matches[0] if matches else ""


def extract_amount(description):
    """
    Extract amount(s) from description text within square brackets [...].
    If multiple amounts are found, sum them.
    
    Args:
        description: Event description text
        
    Returns:
        Sum of all amounts as integer, or 0 if no valid amounts found
    """
    pattern = r'\[([^\]]+)\]'
    matches = re.findall(pattern, description)
    
    total_amount = 0
    
    for match in matches:
        # Try to convert to number
        try:
            # Remove any whitespace and try to convert
            amount = int(match.strip())
            total_amount += amount
        except ValueError:
            # Not a valid number, skip it
            continue
    
    return total_amount


def parse_ics_file(ics_file_path):
    """
    Parse ICS file and extract events matching the criteria.
    
    Args:
        ics_file_path: Path to the ICS file
        
    Returns:
        List of dictionaries containing event information
    """
    # Define date range
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 9, 1)
    
    # Search term
    search_term = "שיעור פרטי"
    
    # Read and parse ICS file
    with open(ics_file_path, 'r', encoding='utf-8') as f:
        calendar = Calendar.from_ical(f.read())
    
    matching_events = []
    
    # Iterate through all events
    for component in calendar.walk():
        if component.name == "VEVENT":
            # Get event properties
            summary = str(component.get('summary', ''))
            dtstart = component.get('dtstart')
            description = str(component.get('description', ''))
            
            # Skip if no start date
            if not dtstart:
                continue
            
            # Get datetime object from dtstart
            event_start = dtstart.dt
            
            # Convert date to datetime if needed (for all-day events)
            if hasattr(event_start, 'date'):
                # It's already a datetime object
                # Remove timezone info for comparison if present
                if hasattr(event_start, 'tzinfo') and event_start.tzinfo is not None:
                    event_start = event_start.replace(tzinfo=None)
            else:
                # It's a date object, convert to datetime
                event_start = datetime.combine(event_start, datetime.min.time())
            
            # Check if event matches criteria
            if (start_date <= event_start < end_date and 
                search_term in summary):
                
                # Clean up description
                clean_description = description.replace('\\n', '\n').replace('\\,', ',')
                
                # Extract payment method and amount
                payment_method = extract_payment_method(clean_description)
                amount = extract_amount(clean_description)
                
                matching_events.append({
                    'Event Name': summary,
                    'Start Date': event_start.strftime('%Y-%m-%d %H:%M:%S'),
                    'Description': clean_description,
                    'Payment Method': payment_method,
                    'Amount': amount
                })
    
    return matching_events


def export_to_csv(events, output_file):
    """
    Export events to CSV file.
    
    Args:
        events: List of event dictionaries
        output_file: Path to output CSV file
    """
    if not events:
        print("No events found matching the criteria.")
        return
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Event Name', 'Start Date', 'Description', 'Payment Method', 'Amount']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(events)
    
    print(f"Successfully exported {len(events)} events to {output_file}")


def main():
    """Main function to run the script."""
    # Input and output file paths
    ics_file = Path('/Users/yehonathanjacob/Documents/eliraz234@gmail.com.ics')
    output_file = Path('/Users/yehonathanjacob/Documents/calendar_events_export.csv')
    
    # Check if input file exists
    if not ics_file.exists():
        print(f"Error: Input file not found: {ics_file}")
        exit(1)
    
    print(f"Reading calendar file: {ics_file}")
    
    # Parse ICS file and filter events
    events = parse_ics_file(ics_file)
    
    # Export to CSV
    export_to_csv(events, output_file)
    
    # Print summary
    if events:
        print(f"\nExtracted events:")
        print(f"- Total events: {len(events)}")
        print(f"- Date range: 01-Jan-2025 to 01-Sep-2025")
        print(f"- Filter: Events containing 'שיעור פרטי'")


if __name__ == "__main__":
    main()
