#!/usr/bin/env python3
"""
Filter color-rendering icons from UTF-8 library
Identifies icons that render as colored emoji on platforms like Discord
"""

import re
from pathlib import Path

# Known color-rendering icons (render as emoji on Discord/Telegram)
COLOR_ICONS = {
    # Check marks & crosses (often colored)
    '✅': 'White Heavy Check Mark',
    '❌': 'Cross Mark',
    '❎': 'Negative Squared Cross Mark',
    '✔': 'Heavy Check Mark',  # Sometimes colored
    '✓': 'Check Mark',  # Sometimes colored
    
    # Warning & alerts
    '⚠': 'Warning Sign',
    '⚡': 'High Voltage Sign',
    '❗': 'Heavy Exclamation Mark Symbol',
    '❕': 'White Exclamation Mark Ornament',
    '❓': 'Black Question Mark Ornament',
    '❔': 'White Question Mark Ornament',
    
    # Hearts
    '❤': 'Heavy Black Heart',
    '❣': 'Heavy Heart Exclamation Mark Ornament',
    
    # Stars (often colored/yellow)
    '⭐': 'White Medium Star',
    '🌟': 'Glowing Star',
    '✨': 'Sparkles',
    '⚝': 'Outlined White Star',  # Sometimes colored
    
    # Weather & nature
    '☀': 'Black Sun With Rays',
    '☁': 'Cloud',
    '☂': 'Umbrella',
    '☃': 'Snowman',
    '☄': 'Comet',
    '☔': 'Umbrella With Rain Drops',
    '☕': 'Hot Beverage',
    '☘': 'Shamrock',
    
    # Hands & gestures (often colored as skin tones)
    '✊': 'Raised Fist',
    '✋': 'Raised Hand',
    '✌': 'Victory Hand',
    '✍': 'Writing Hand',
    
    # Tools & objects
    '✂': 'Black Scissors',
    '✈': 'Airplane',
    '✉': 'Envelope',
    
    # Zodiac signs (sometimes colored)
    '♈': 'Aries',
    '♉': 'Taurus',
    '♊': 'Gemini',
    '♋': 'Cancer',
    '♌': 'Leo',
    '♍': 'Virgo',
    '♎': 'Libra',
    '♏': 'Scorpius',
    '♐': 'Sagittarius',
    '♑': 'Capricorn',
    '♒': 'Aquarius',
    '♓': 'Pisces',
    
    # Chess pieces (sometimes colored)
    '♔': 'White Chess King',
    '♕': 'White Chess Queen',
    '♖': 'White Chess Rook',
    '♗': 'White Chess Bishop',
    '♘': 'White Chess Knight',
    '♙': 'White Chess Pawn',
    '♚': 'Black Chess King',
    '♛': 'Black Chess Queen',
    '♜': 'Black Chess Rook',
    '♝': 'Black Chess Bishop',
    '♞': 'Black Chess Knight',
    '♟': 'Black Chess Pawn',
    
    # Card suits (sometimes colored)
    '♠': 'Black Spade Suit',
    '♡': 'White Heart Suit',
    '♢': 'White Diamond Suit',
    '♣': 'Black Club Suit',
    
    # Circles (sometimes colored)
    '⚪': 'Medium White Circle',
    '⚫': 'Medium Black Circle',
    
    # Other potentially colored
    '☎': 'Black Telephone',
    '☏': 'White Telephone',
    '☑': 'Ballot Box With Check',  # Sometimes green
    '☒': 'Ballot Box With X',  # Sometimes red
    '☢': 'Radioactive Sign',
    '☣': 'Biohazard Sign',
    '☤': 'Caduceus',
    '☥': 'Ankh',
    '☦': 'Orthodox Cross',
    '☧': 'Chi Rho',
    '☨': 'Cross of Lorraine',
    '☩': 'Cross of Jerusalem',
    '☪': 'Star and Crescent',
    '☫': 'Farsi Symbol',
    '☬': 'Adi Shakti',
    '☭': 'Hammer and Sickle',
    '☮': 'Peace Symbol',
    '☯': 'Yin Yang',
}

# Safe monochrome icons (should not render as colored emoji)
SAFE_CATEGORIES = {
    'arrows': True,  # Most arrows are safe
    'box_drawing': True,  # Box drawing characters are safe
    'mathematical': True,  # Math symbols are usually safe
    'dingbats': False,  # Some dingbats render as color
    'symbols': False,  # Some symbols render as color
}

def read_icon_library(filepath):
    """Read the icon library and extract icons with their descriptions"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern: `ICON` **Name** - Description
    pattern = r'`([^`]+)` \*\*([^*]+)\*\* - (.+)'
    icons = []
    
    for match in re.finditer(pattern, content):
        icon = match.group(1)
        name = match.group(2)
        description = match.group(3)
        icons.append({
            'icon': icon,
            'name': name,
            'description': description,
            'line': match.group(0)
        })
    
    return icons, content

def filter_color_icons(icons):
    """Separate icons into monochrome and color groups"""
    monochrome = []
    color = []
    
    for icon_data in icons:
        icon_char = icon_data['icon']
        
        if icon_char in COLOR_ICONS:
            color.append(icon_data)
        else:
            # Additional checks for potentially colored icons
            # Check for emoji variation selector (FE0F)
            if '\ufe0f' in icon_char:
                color.append(icon_data)
            # Check for characters in emoji blocks
            elif any(0x1F300 <= ord(c) <= 0x1F9FF for c in icon_char):
                color.append(icon_data)
            else:
                monochrome.append(icon_data)
    
    return monochrome, color

def create_monochrome_library(original_content, monochrome_icons):
    """Create filtered library with only monochrome icons"""
    # Keep the header and overview
    lines = original_content.split('\n')
    
    # Find where the icon listings start
    icon_start = None
    for i, line in enumerate(lines):
        if line.startswith('### ') and 'Most Useful Icons' in line:
            icon_start = i
            break
    
    if icon_start is None:
        # If we can't find the section, rebuild from scratch
        return rebuild_library(monochrome_icons)
    
    # Keep everything up to the icon listings
    header = '\n'.join(lines[:icon_start])
    
    # Rebuild icon sections
    sections = {}
    current_section = None
    
    for icon in monochrome_icons:
        # Extract category from description or name
        category = 'miscellaneous'
        if 'arrow' in icon['name'].lower() or 'arrow' in icon['description'].lower():
            category = 'navigation'
        elif 'check' in icon['name'].lower() or 'cross' in icon['name'].lower() or 'warning' in icon['name'].lower():
            category = 'status'
        elif 'star' in icon['name'].lower() or 'circle' in icon['name'].lower():
            category = 'stars'
        elif 'heart' in icon['name'].lower():
            category = 'symbols'
        elif 'hand' in icon['name'].lower() or 'point' in icon['name'].lower():
            category = 'hands'
        elif 'scissor' in icon['name'].lower() or 'pencil' in icon['name'].lower() or 'envelope' in icon['name'].lower():
            category = 'tools'
        elif 'weather' in icon['description'].lower() or 'sun' in icon['name'].lower() or 'cloud' in icon['name'].lower():
            category = 'weather'
        elif 'zodiac' in icon['description'].lower():
            category = 'zodiac'
        elif 'chess' in icon['name'].lower() or 'card' in icon['description'].lower():
            category = 'games'
        elif 'box' in icon['name'].lower() or 'block' in icon['name'].lower():
            category = 'box_drawing'
        elif 'math' in icon['description'].lower():
            category = 'mathematical'
        
        if category not in sections:
            sections[category] = []
        sections[category].append(icon)
    
    # Build the monochrome library
    monochrome_content = header + "\n\n"
    monochrome_content += "## Monochrome Icon Library\n\n"
    monochrome_content += "**Filtered version** - Color-rendering icons removed for consistent monochrome display.\n\n"
    
    # Add sections in logical order
    section_order = [
        ('navigation', 'Navigation & Direction'),
        ('status', 'Status & Feedback'),
        ('stars', 'Stars & Ratings'),
        ('symbols', 'Common Symbols'),
        ('hands', 'Hands & Gestures'),
        ('tools', 'Tools & Objects'),
        ('weather', 'Weather & Nature'),
        ('zodiac', 'Zodiac & Astrology'),
        ('games', 'Chess & Cards'),
        ('mathematical', 'Mathematical & Technical'),
        ('box_drawing', 'Box Drawing & Blocks'),
        ('miscellaneous', 'Miscellaneous Symbols'),
    ]
    
    for category_key, category_name in section_order:
        if category_key in sections and sections[category_key]:
            monochrome_content += f"### {category_name}\n\n"
            for icon in sections[category_key]:
                monochrome_content += f"{icon['line']}\n"
            monochrome_content += "\n"
    
    # Add footer
    monochrome_content += "## About This Filtered Version\n\n"
    monochrome_content += "This library contains only monochrome icons that should render consistently as black/white text across platforms.\n\n"
    monochrome_content += "**Color icons removed**: Check marks, hearts, stars, and other symbols that platforms often render as colored emoji.\n\n"
    monochrome_content += "**Use when**: You need consistent monochrome display across Discord, Telegram, Signal, etc.\n\n"
    monochrome_content += "**See also**: `utf8-icons-full.md` for the complete library including color-rendering icons.\n"
    
    return monochrome_content

def rebuild_library(monochrome_icons):
    """Rebuild library from scratch if structure parsing fails"""
    content = "# UTF-8 Monochrome Icon Library\n\n"
    content += "## Overview\n\n"
    content += "Filtered version with color-rendering icons removed. All icons should display as monochrome text.\n\n"
    
    # Group by first character for organization
    groups = {}
    for icon in monochrome_icons:
        first_char = icon['icon'][0]
        if first_char not in groups:
            groups[first_char] = []
        groups[first_char].append(icon)
    
    # Add icons grouped by type
    for char, icons in sorted(groups.items()):
        content += f"### U+{ord(char):04X} Range\n\n"
        for icon in icons:
            content += f"{icon['line']}\n"
        content += "\n"
    
    return content

def main():
    """Main execution function"""
    base_dir = Path(__file__).parent
    input_file = base_dir / "utf8-icons.md"
    output_file = base_dir / "utf8-icons-monochrome.md"
    color_list_file = base_dir / "color-icons-removed.md"
    
    print("Reading icon library...")
    icons, original_content = read_icon_library(input_file)
    print(f"Found {len(icons)} icons in library")
    
    print("\nFiltering color-rendering icons...")
    monochrome_icons, color_icons = filter_color_icons(icons)
    print(f"Monochrome icons: {len(monochrome_icons)}")
    print(f"Color icons removed: {len(color_icons)}")
    
    # Create monochrome library
    print("\nCreating monochrome library...")
    monochrome_content = create_monochrome_library(original_content, monochrome_icons)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(monochrome_content)
    print(f"Created: {output_file}")
    
    # Create list of removed color icons
    print("\nCreating color icons reference...")
    color_content = "# Color Icons Removed from Monochrome Library\n\n"
    color_content += "These icons were removed because they often render as colored emoji on platforms like Discord and Telegram.\n\n"
    
    for icon in color_icons:
        color_content += f"- `{icon['icon']}` **{icon['name']}** - {icon['description']}\n"
    
    color_content += f"\n**Total removed**: {len(color_icons)} icons\n"
    color_content += "**Remaining monochrome**: {len(monochrome_icons)} icons\n"
    
    with open(color_list_file, 'w', encoding='utf-8') as f:
        f.write(color_content)
    print(f"Created: {color_list_file}")
    
    # Create quick reference for monochrome icons
    print("\nCreating monochrome quick reference...")
    quick_ref_file = base_dir / "quick-reference-monochrome.md"
    
    # Select top monochrome icons
    top_monochrome = monochrome_icons[:50]
    quick_content = "# Monochrome Icon Quick Reference\n\n"
    quick_content += "Top 50 monochrome icons (color-rendering icons removed).\n\n"
    
    quick_content += "## Navigation & Direction\n"
    nav_icons = [i for i in top_monochrome if 'arrow' in i['name'].lower() or 'arrow' in i['description'].lower()]
    for icon in nav_icons[:10]:
        quick_content += f"`{icon['icon']}` "
    quick_content += "\n\n"
    
    quick_content += "## Status & Symbols\n"
    status_icons = [i for i in top_monochrome if 'check' in i['name'].lower() or 'cross' in i['name'].lower()]
    for icon in status_icons[:10]:
        quick_content += f"`{icon['icon']}` "
    quick_content += "\n\n"
    
    quick_content += "## Common Monochrome Icons\n"
    for icon in top_monochrome[:30]:
        quick_content += f"`{icon['icon']}` "
    
    with open(quick_ref_file, 'w', encoding='utf-8') as f:
        f.write(quick_content)
    print(f"Created: {quick_ref_file}")
    
    print(f"\nDone! Monochrome library created with {len(monochrome_icons)} icons.")
    print(f"Color icons removed: {len(color_icons)}")

if __name__ == "__main__":
    main()