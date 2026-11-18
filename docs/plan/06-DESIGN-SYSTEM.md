# 06 · Design system

Taken from the Keystone design canvas. Task T03 writes these tokens to `app/static/css/tokens.css`
and the components to `app/static/css/app.css` and `app/templates/components/`.

## Hard rules for templates

- **No inline `style=""` attributes and no `<style>` blocks.** The CSP blocks them. Use classes
  from `app.css`.
- **No inline JavaScript** and no `on...=` attributes. This app needs no JavaScript.
- Use the component macros. Do not hand-write buttons, badges or form fields.
- Never use color alone to carry meaning. Badges always include a word ("Pending").

## Color tokens

```css
:root {
  /* surfaces */
  --bg:            #F4F6F9;   /* page background */
  --surface:       #FFFFFF;   /* cards, tables, forms */
  --surface-muted: #FAFBFC;   /* table header, quiet boxes */
  --border:        #DDE2EA;   /* default hairline */
  --border-strong: #C5CCD8;   /* inputs, secondary buttons */
  --divider:       #EBEEF3;   /* rows inside a card */

  /* text */
  --text:          #141A26;   /* body and headings */
  --text-2:        #3A4354;   /* supporting copy */
  --text-muted:    #525C6E;   /* captions, labels */
  --text-faint:    #5F697C;   /* placeholders, meta */

  /* brand */
  --navy:          #0B1F3A;   /* sidebar header, landing hero */
  --navy-2:        #12294A;
  --navy-3:        #1B3A66;
  --on-navy:       #FFFFFF;
  --on-navy-muted: #B9C7DD;

  /* accent (primary actions, links) */
  --accent:        #1D54BF;
  --accent-hover:  #17459F;
  --accent-soft:   #EEF3FD;   /* selected nav item, info badge */
  --on-accent:     #FFFFFF;

  /* roles */
  --agent-bg:      #E4EAF3;   /* "suggested by Keystone" chips */
  --agent-text:    #1B3A66;
  --decide-bg:     #FEF6E7;   /* "you decide" / pending */
  --decide-border: #FCE8C4;
  --decide-text:   #7A4300;
  --success-bg:    #EAF7F0;
  --success-text:  #0B5C39;
  --success-dot:   #178A57;
  --danger:        #B0271F;
  --danger-bg:     #FDF0EF;
  --danger-text:   #8E1D17;
}
```

All text and background pairs above pass WCAG AA (4.5:1). Do not add new colors.

## Type

```css
--font-sans: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
--font-mono: "IBM Plex Mono", ui-monospace, Consolas, monospace;
```

Loaded in `base.html` with one `<link>` to Google Fonts (weights 400, 500, 600). The fallback stack
works offline.

| Use | Size / line height | Weight |
|---|---|---|
| Page title (h1) | 24 / 32 px | 600 |
| Section title (h2) | 15 / 20 px | 600 |
| Body | 14 / 20 px | 400 |
| Small, meta | 13 / 18 px | 400 |
| Caption, badge | 12 / 16 px | 500 |
| IDs, numbers | mono 12 px | 400 |

## Spacing and shape

- Spacing scale: 4, 8, 12, 16, 20, 24, 32, 48 px (`--s-1` to `--s-8`).
- Radius: 6 px for controls, 8 px for cards.
- Card: white, 1 px `--border`, radius 8, padding 16.
- Page: sidebar 232 px wide on desktop; main content max width 1040 px, padding 24 px 32 px.
- Below 800 px wide the sidebar becomes a top bar and cards stack. No horizontal scroll.

## Components (macros in `templates/components/`)

| Macro | File | Looks like |
|---|---|---|
| `button(label, kind="primary", type="submit")` | `ui.html` | primary: accent fill, white text. secondary: white, strong border. danger: danger fill. Height 36 px. |
| `link_button(label, href, kind="secondary")` | `ui.html` | same look, an `<a>` |
| `badge(text, tone)` | `ui.html` | tones: `neutral`, `info` (accent-soft), `pending` (decide), `success`, `danger`, `agent` |
| `field(name, label, value, error, type="text", required=False, help="")` | `forms.html` | label, input, help text, error |
| `textarea_field(...)`, `select_field(name, label, options, value, error)` | `forms.html` | same pattern |
| `csrf_field()` | `forms.html` | hidden input with `session["csrf"]` |
| `card(title)` with `caller()` | `ui.html` | card with optional title row |
| `empty_state(text, action_label=None, action_href=None)` | `ui.html` | centred muted text plus optional button |
| `score_bar(score, max_score)` | `ui.html` | 5 segments filled in proportion, plus the number |
| `confirm_box(title)` with `caller()` | `ui.html` | decide-colored box, used on every confirm screen |
| `flash_messages()` | `ui.html` | success and error banners at the top of main |

## Status badge mapping

| Status | Tone | Text |
|---|---|---|
| pending | pending | Pending |
| other statuses | set in T15 from the brief | brief's wording |
| booked | success | Booked |
| open slot | info | Open |
| job closed | neutral | Closed |
