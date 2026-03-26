# UTF-8 Icon Library for Chat Applications

## Overview
A comprehensive library of UTF-8 icons organized for easy use by agents in chat applications (Discord, Telegram, Signal, WhatsApp, etc.). Now available in two versions:

### **Version 1: Full Library** (includes all icons)
- `utf8-icons-full.md` - Complete library with 168 icons (includes color-rendering icons)
- `quick-reference-full.md` - Top icons from full library

### **Version 2: Monochrome Library** (color icons removed)
- `utf8-icons-monochrome.md` - Filtered library with 99 monochrome-only icons
- `quick-reference-monochrome.md` - Top monochrome icons
- `color-icons-removed.md` - List of 69 icons removed for color rendering

## Why Two Versions?

### Color Rendering Issue
Some UTF-8 icons render as **colored emoji** on platforms like Discord and Telegram, while others render as **monochrome text**. This causes inconsistent appearance across platforms.

### Solution
1. **Full Library**: Use when you want all available icons, don't mind color variations
2. **Monochrome Library**: Use when you need consistent black/white display across all platforms

## Files

### Primary Files
- **`utf8-icons-full.md`** - Complete library (168 icons, includes color)
- **`utf8-icons-monochrome.md`** - Filtered library (99 icons, monochrome only)
- **`quick-reference-full.md`** - Top icons from full library
- **`quick-reference-monochrome.md`** - Top monochrome icons

### Reference Files
- **`color-icons-removed.md`** - List of 69 icons removed from monochrome version
- **`color-filter.py`** - Python script used for filtering

### Raw Data
- **`raw/arrows.md`** - Raw arrow icons from utf8icons.com
- **`raw/dingbats.md`** - Raw dingbat icons from utf8icons.com
- **`raw/miscellaneous-symbols.md`** - Raw miscellaneous symbols

## Usage

### For Agents
1. **Choose version** based on your needs:
   - **Monochrome**: `utf8-icons-monochrome.md` for consistent display
   - **Full**: `utf8-icons-full.md` for maximum icon selection

2. **Copy-paste**: Simply copy any icon and paste into your chat application
3. **Search**: Use Ctrl+F to find icons by name, category, or function
4. **Templates**: Use the ready-made templates in quick reference files

### Categories Included (Monochrome Version)
- **Navigation & Direction**: Arrows, pointers (monochrome variants)
- **Status & Feedback**: Check marks, crosses (text versions)
- **Mathematical & Technical**: Math symbols, technical icons
- **Box Drawing & Blocks**: Box drawing characters, blocks
- **Letterlike Symbols**: Symbols that resemble letters
- **Miscellaneous**: Other monochrome symbols

### Categories Removed (Color Version Only)
- Colored check marks (✅, ✔)
- Colored crosses (❌, ❎)
- Colored stars (⭐, 🌟, ✨)
- Colored hearts (❤)
- Colored weather symbols (☀, ☁, ☂)
- Colored hands and gestures (✊, ✋, ✌)
- Colored zodiac signs
- Colored chess pieces and card suits

## Quick Start

### Monochrome Icons (Recommended for Consistency)
```
Navigation: ← ↑ → ↓ ↔ ↕
Status: ✓ ✗ ✘
Box Drawing: ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼
Mathematical: × ÷ ± ≠ ≈
```

### Full Icons (Includes Color)
```
Navigation: ← ↑ → ↓ ↔ ↕
Status: ✓ ✔ ✗ ✘ ⚠ ✅ ❌
Stars: ★ ☆ ⭐ 🌟 ✨
Common: ❤ ♡ ☀ ☁ ☂ ☃
```

## Platform Compatibility

| Platform | Monochrome Icons | Color Icons |
|----------|------------------|-------------|
| Discord | Consistent black/white | Render as colored emoji |
| Telegram | Consistent black/white | Render as colored emoji |
| WhatsApp | Consistent | May render as colored |
| Signal | Consistent | May render as colored |
| Slack | Consistent | May render as colored |

## Best Practices

1. **For professional/business use**: Use **monochrome** version for consistency
2. **For casual/fun use**: Use **full** version for colorful expressions
3. **Testing**: Always test icon rendering in your target platform
4. **Documentation**: Note which version you're using in your projects

## Source & Updates

- **Source**: utf8icons.com
- **Filtering**: Custom Python script (`color-filter.py`)
- **Last updated**: 2026-03-26
- **Total icons (full)**: 168 organized icons
- **Total icons (monochrome)**: 99 filtered icons
- **Color icons removed**: 69 icons

## License
This icon library is compiled from publicly available UTF-8 characters. Icons can be freely used in chat applications, documentation, and user interfaces.

## Contributing
To update or expand the library:
1. Fetch new subsets from utf8icons.com
2. Add to `utf8-icons-full.md`
3. Run `python3 color-filter.py` to update monochrome version
4. Update documentation

## Notes
- Monochrome version ensures consistent cross-platform display
- Full version provides maximum icon selection
- Always test in your target environment before production use
- Bookmark or save locally for quick access during chat operations