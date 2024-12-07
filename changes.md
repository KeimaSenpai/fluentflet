Added new features to enhance component functionality and user interaction.

Components changed:
- `Calendar`: Added blackout dates feature to disable specific dates
- `TextBox`: Added support for action buttons with tooltips
- `FluentWindow`: Added state management system and template-based routing
- `FluentState`: New class for centralized state management

Implementation details:
- Calendar supports array of blocked dates with visual indicators
- TextBox supports multiple action buttons with icons and tooltips
- Added path-based routing with parameter support
- Added session-based state persistence

---

Refactored components to use FluentDesignSystem for consistent styling and theming.

Components changed:
- `Button`: Integrated design system colors and animations
- `Calendar`: Updated to use theme colors and properties
- `Checkbox`: Migrated to design system color scheme
- `Expander`: Updated animations and layout handling
- `ListItem`: Improved selection handling with theme colors
- `Radio`: Updated state management with theme properties
- `Slider`: Fixed positioning and improved theme integration
- `TextBox`: Improved styling and state management
- `Toggle`: Updated transitions and theme colors
- `fluent_design_system.py`: Improved color management system

Implementation details:
- Changed color format from HSL to hex/rgba
- Added theme switching support
- Added font management system
- Improved component documentation
- Added type hints
- Standardized animation durations

Breaking changes:
- Components require FluentDesignSystem instance
- Updated theme color format
- Modified component constructors