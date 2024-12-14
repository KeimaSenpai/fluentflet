feat: version 0.2.0alpha1

### `TextBox` Component
- Added new features:
  - `prefix` text support
  - `suffix` text support
- Added dynamic padding calculations based on prefix/suffix content
- Enhanced focus/blur handling:
  - Added opacity control for hint text
  - Improved hint text color management
  - Added explicit handling for hint text style changes during focus/blur states

### `Button` Component
- Reorganized state handling:
  - Reordered control states for better consistency. Flet version must be > `0.25.2` ([see why](https://github.com/flet-dev/flet/pull/4556))
- State configurations now properly implement:
  - Hover states
  - Pressed states
  - Default states
  - Disabled states

### Navigation System
- Added new `NavigationType` enum with two modes:
  - `STANDARD`: Original layout that pushes content
  - `OVERLAY`: Navigation overlays the content
- Enhanced navigation panel styling:
  - Added blur effects for expanded state
  - Implemented border radius adjustments
  - Added shadow effects
  - Improved animation handling

### Window System
- Added `NavigationType` to exported symbols
- Modified default window behavior to support new navigation types
- Enhanced window layout management for both standard and overlay navigation modes

## Infrastructure Changes

### Dependencies
- Updated Flet dependency to match the new pypi library structure:
  - Old: `flet>=0.25.1`
  - New: `flet[all]>=0.25.2`

## API Changes and Deprecations
- Removed **deprecated** `right_icon` and `right_action` properties from `TextBox`
- Changed method of handling icon actions in TextBox to new action system
- Modified window navigation behavior to support new navigation types

## Performance Improvements
- Implemented icon availability caching in icon browser
- Added pre-calculated styles for common UI elements
- Optimized update patterns in components to reduce unnecessary rerenders