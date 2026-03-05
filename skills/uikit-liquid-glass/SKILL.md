---
name: uikit-liquid-glass
description: Implement Apple's Liquid Glass design system in UIKit applications. Use when asked to adopt new Apple design language, create glass effects, implement iOS 26/macOS 26 visual effects, or work with UIGlassEffect, UIGlassContainerEffect, UIScrollEdgeEffect, or UIScrollEdgeElementContainerInteraction. Covers interactive glass buttons, morphing glass containers, scroll view edge effects, and toolbar glass integration.
---

# Liquid Glass UIKit Implementation

Liquid Glass is Apple's dynamic material that blurs content, reflects surrounding color/light, and reacts to touch. This skill covers UIKit implementation patterns.

## Core Components

| Class | Purpose |
|-------|---------|
| `UIGlassEffect` | Basic glass material with blur, tint, interactivity |
| `UIGlassContainerEffect` | Container enabling glass elements to morph/blend |
| `UIScrollEdgeEffect` | Glass effects at scroll view edges |
| `UIScrollEdgeElementContainerInteraction` | Makes overlay views affect scroll edge shape |

## Quick Start

**Basic glass view:**
```swift
let glass = UIGlassEffect()
glass.tintColor = UIColor.systemBlue.withAlphaComponent(0.3)
glass.isInteractive = true

let effectView = UIVisualEffectView(effect: glass)
effectView.layer.cornerRadius = 20
effectView.clipsToBounds = true
```

**Morphing glass container:**
```swift
let container = UIGlassContainerEffect()
container.spacing = 40.0  // Distance where elements begin merging

let containerView = UIVisualEffectView(effect: container)
// Add UIVisualEffectView children with UIGlassEffect to contentView
// Elements within spacing distance will blend shapes
```

**Scroll edge effects:**
```swift
scrollView.topEdgeEffect.style = .automatic
scrollView.bottomEdgeEffect.style = .hard
scrollView.leftEdgeEffect.isHidden = true
```

**Overlay affecting scroll edge:**
```swift
let interaction = UIScrollEdgeElementContainerInteraction()
interaction.scrollView = scrollView
interaction.edge = .bottom
overlayContainer.addInteraction(interaction)
```

**Toolbar glass control:**
```swift
barButtonItem.hidesSharedBackground = true  // Opt out of shared glass
```

## Implementation Workflow

1. **Determine glass type needed:**
   - Single glass element → `UIGlassEffect` + `UIVisualEffectView`
   - Multiple blending elements → `UIGlassContainerEffect` wrapper
   - Scroll view edges → Configure `scrollView.*EdgeEffect`
   - Overlays on scroll views → `UIScrollEdgeElementContainerInteraction`

2. **Configure the effect:**
   - Set `tintColor` for visual differentiation
   - Set `isInteractive = true` for touch-responsive elements
   - Set container `spacing` for morph threshold

3. **Build view hierarchy:**
   - Add content to `visualEffectView.contentView`
   - Apply `cornerRadius` + `clipsToBounds` for rounded glass
   - For containers: child glass views go in container's `contentView`

## Best Practices

- **Performance:** Limit simultaneous glass elements; test on older devices
- **Contrast:** Ensure text meets accessibility requirements on glass backgrounds
- **Spacing:** Keep glass elements within container's `spacing` value for blending
- **Accessibility:** Test with VoiceOver; all glass elements must be accessible

## Extended Examples

See [references/examples.md](references/examples.md) for complete implementations:
- Reusable `GlassCardView` class
- Interactive glass buttons
- Complex multi-element containers
- Scroll view with edge effects and overlays
