# Visuals for adult-beginner explainers

Read this when the explainer can use diagrams, illustrations, charts, screenshots, or generated images.

## Choose the visual by its teaching job

| The reader needs to see | Best starting form |
|---|---|
| Order, flow, cause and effect | Labeled HTML or inline SVG diagram |
| Parts, hierarchy, or ownership | Labeled SVG map or nested HTML |
| A comparison | Side-by-side cards, table, or aligned SVG |
| Quantity or change | Simple chart with the values also present as text or a table |
| A real interface | Cropped screenshot with callouts, if the current interface matters |
| Appearance, setting, scale, or a hard-to-draw scene | Generated raster illustration or photo |

Start with the simplest form that makes the relationship visible. Give every visual a teaching job.

## Draw diagrams directly

Use HTML, CSS, or inline SVG when labels must be exact. Keep the reading direction obvious. Use arrowheads, borders, position, and words so the diagram does not rely on color alone.

Put an SVG in a `<figure>` with a visible `<figcaption>`. Give it `role="img"`, a short `<title>`, and a useful `<desc>`. For a complex diagram, repeat its full meaning as normal visible text after the figure.

This example gives one visual job to a sign-in diagram: show that Google confirms identity without sending the password to the app.

```html
<figure class="flow">
  <svg viewBox="0 0 760 210" role="img" aria-labelledby="flow-title flow-desc">
    <title id="flow-title">How Google sign-in connects three parties</title>
    <desc id="flow-desc">You ask Google to confirm your identity. Google sends the recipe app a limited confirmation, not your password.</desc>
    <defs>
      <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor" />
      </marker>
    </defs>
    <g fill="none" stroke="currentColor" stroke-width="3">
      <rect x="20" y="55" width="180" height="90" rx="18" />
      <rect x="290" y="55" width="180" height="90" rx="18" />
      <rect x="560" y="55" width="180" height="90" rx="18" />
      <path d="M 200 85 H 286" marker-end="url(#arrow)" />
      <path d="M 470 120 H 556" marker-end="url(#arrow)" />
    </g>
    <g fill="currentColor" text-anchor="middle" font-family="system-ui, sans-serif">
      <text x="110" y="95" font-size="24" font-weight="700">You</text>
      <text x="110" y="122" font-size="16">Choose Google sign-in</text>
      <text x="380" y="95" font-size="24" font-weight="700">Google</text>
      <text x="380" y="122" font-size="16">Checks and asks permission</text>
      <text x="650" y="95" font-size="24" font-weight="700">Recipe app</text>
      <text x="650" y="122" font-size="16">Gets limited confirmation</text>
      <text x="243" y="68" font-size="14">Request</text>
      <text x="513" y="104" font-size="14">No password</text>
    </g>
  </svg>
  <figcaption>Google confirms who you are. The app receives only the identity details and access shown on the permission screen.</figcaption>
</figure>
```

Make the SVG responsive with `width: 100%; height: auto`. Stack or redraw dense horizontal flows for narrow screens rather than shrinking labels until they are unreadable.

## Generate a complex image only when it teaches

Use the current runtime's image-generation tool when available. If the runtime exposes the `imagegen` skill, invoke `$imagegen`. Ask for an educational visual with a clear subject and composition. Keep essential labels as HTML or SVG because generated lettering is less reliable and less accessible.

If direct image generation is unavailable but the `codex` CLI is available, delegate the asset from the shell. Single quotes preserve the `$imagegen` skill name:

```bash
codex '$imagegen Create a calm editorial illustration of an adult reviewing a calendar app permission screen, with the person in control and no logos, labels, text, or watermark. Wide composition for an educational HTML explainer.'
```

Inspect the result. Check that it teaches the intended idea, contains no misleading details, and fits the page. Copy the selected file beside the artifact, reference it with a relative path, and report the saved path.

## Make every visual understandable without sight

- Write nearby visible text that states the visual's conclusion and full explanation.
- Use concise `alt` text for a simple informative image. Use `alt=""` only when an image adds no information.
- Give a complex image a short identification plus a visible long description with the relationships, values, or sequence it conveys.
- Keep prose as real HTML. Avoid baking essential wording into a raster image.
- Use `<figure>` and `<figcaption>` to keep each visual tied to its explanation.

These choices follow the [W3C guidance for complex images](https://www.w3.org/WAI/tutorials/images/complex/) and the [GOV.UK guidance on images in services](https://design-system.service.gov.uk/styles/images/).
