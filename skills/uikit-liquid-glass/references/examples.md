# Liquid Glass Extended Examples

## Reusable GlassCardView

A complete, reusable glass card component:

```swift
class GlassCardView: UIView {
    private let visualEffectView: UIVisualEffectView
    private let contentView = UIView()
    
    init(frame: CGRect, tintColor: UIColor? = nil, isInteractive: Bool = false) {
        let glassEffect = UIGlassEffect()
        glassEffect.tintColor = tintColor
        glassEffect.isInteractive = isInteractive
        
        visualEffectView = UIVisualEffectView(effect: glassEffect)
        
        super.init(frame: frame)
        setupViews()
    }
    
    required init?(coder: NSCoder) {
        let glassEffect = UIGlassEffect()
        visualEffectView = UIVisualEffectView(effect: glassEffect)
        super.init(coder: coder)
        setupViews()
    }
    
    private func setupViews() {
        visualEffectView.frame = bounds
        visualEffectView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        visualEffectView.layer.cornerRadius = 20
        visualEffectView.clipsToBounds = true
        addSubview(visualEffectView)
        
        contentView.frame = bounds
        contentView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        contentView.backgroundColor = .clear
        addSubview(contentView)
    }
    
    func addContent(_ view: UIView) {
        view.frame = contentView.bounds
        view.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        contentView.addSubview(view)
    }
}

// Usage:
let cardView = GlassCardView(
    frame: CGRect(x: 50, y: 100, width: 300, height: 200),
    tintColor: UIColor.systemBlue.withAlphaComponent(0.2),
    isInteractive: true
)

let label = UILabel()
label.text = "Glass Card"
label.textAlignment = .center
label.textColor = .white
cardView.addContent(label)

view.addSubview(cardView)
```

## Interactive Glass Button

Creating a button with glass background that responds to touch:

```swift
let interactiveGlassEffect = UIGlassEffect()
interactiveGlassEffect.isInteractive = true

let glassButton = UIButton(frame: CGRect(x: 50, y: 300, width: 200, height: 50))
glassButton.setTitle("Glass Button", for: .normal)
glassButton.setTitleColor(.white, for: .normal)

let buttonEffectView = UIVisualEffectView(effect: interactiveGlassEffect)
buttonEffectView.frame = glassButton.bounds
buttonEffectView.layer.cornerRadius = 15
buttonEffectView.clipsToBounds = true
buttonEffectView.isUserInteractionEnabled = false  // Let touches pass through

glassButton.insertSubview(buttonEffectView, at: 0)
view.addSubview(glassButton)
```

## Morphing Glass Container

Multiple glass elements that blend when close together:

```swift
// Create the container effect
let containerEffect = UIGlassContainerEffect()
containerEffect.spacing = 40.0  // Merge threshold in points

let containerView = UIVisualEffectView(effect: containerEffect)
containerView.frame = CGRect(x: 50, y: 400, width: 300, height: 200)

// First glass element
let firstGlassEffect = UIGlassEffect()
let firstGlassView = UIVisualEffectView(effect: firstGlassEffect)
firstGlassView.frame = CGRect(x: 20, y: 20, width: 100, height: 100)
firstGlassView.layer.cornerRadius = 20
firstGlassView.clipsToBounds = true

// Second glass element with tint
let secondGlassEffect = UIGlassEffect()
secondGlassEffect.tintColor = UIColor.systemPink.withAlphaComponent(0.3)
let secondGlassView = UIVisualEffectView(effect: secondGlassEffect)
secondGlassView.frame = CGRect(x: 80, y: 60, width: 100, height: 100)
secondGlassView.layer.cornerRadius = 20
secondGlassView.clipsToBounds = true

// Add to container's contentView (not the container directly)
containerView.contentView.addSubview(firstGlassView)
containerView.contentView.addSubview(secondGlassView)

view.addSubview(containerView)
```

## Scroll View with Edge Effects and Overlay

Complete scroll view setup with custom edge effects and interactive overlay:

```swift
// Configure the scroll view
let scrollView = UIScrollView(frame: view.bounds)
scrollView.topEdgeEffect.style = .automatic
scrollView.bottomEdgeEffect.style = .hard
scrollView.leftEdgeEffect.isHidden = true
scrollView.rightEdgeEffect.isHidden = true

view.addSubview(scrollView)

// Create overlay container that affects the bottom edge
let buttonContainer = UIView(frame: CGRect(
    x: 0,
    y: scrollView.frame.height - 80,
    width: scrollView.frame.width,
    height: 80
))

let button1 = UIButton(frame: CGRect(x: 20, y: 20, width: 100, height: 40))
button1.setTitle("Button 1", for: .normal)
button1.backgroundColor = .systemBlue
button1.layer.cornerRadius = 8
buttonContainer.addSubview(button1)

let button2 = UIButton(frame: CGRect(x: 140, y: 20, width: 100, height: 40))
button2.setTitle("Button 2", for: .normal)
button2.backgroundColor = .systemGreen
button2.layer.cornerRadius = 8
buttonContainer.addSubview(button2)

// Add interaction to make buttons affect scroll edge shape
let interaction = UIScrollEdgeElementContainerInteraction()
interaction.scrollView = scrollView
interaction.edge = .bottom
buttonContainer.addInteraction(interaction)

view.addSubview(buttonContainer)
```

## Toolbar with Mixed Glass Backgrounds

Controlling which toolbar items use shared glass:

```swift
let shareButton = UIBarButtonItem(
    barButtonSystemItem: .action,
    target: self,
    action: #selector(shareAction)
)

let favoriteButton = UIBarButtonItem(
    image: UIImage(systemName: "heart"),
    style: .plain,
    target: self,
    action: #selector(favoriteAction)
)
// Opt this item out of shared glass background
favoriteButton.hidesSharedBackground = true

let spacer = UIBarButtonItem(
    barButtonSystemItem: .flexibleSpace,
    target: nil,
    action: nil
)

toolbarItems = [spacer, shareButton, spacer, favoriteButton, spacer]
navigationController?.setToolbarHidden(false, animated: false)
```

## API Reference Links

- [UIGlassEffect](https://developer.apple.com/documentation/UIKit/UIGlassEffect)
- [UIGlassContainerEffect](https://developer.apple.com/documentation/UIKit/UIGlassContainerEffect)
- [UIScrollEdgeEffect](https://developer.apple.com/documentation/UIKit/UIScrollEdgeEffect)
- [UIScrollEdgeElementContainerInteraction](https://developer.apple.com/documentation/UIKit/UIScrollEdgeElementContainerInteraction)
