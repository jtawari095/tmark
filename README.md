# Tmark

Markdown Slideshow in Terminal.

Tmark allows you to create presentations in markdown format and render them directly inside your terminal.

You can look at example presentations in the [examples directories](/examples).

## Features ✨

- ✅ Fully complaint to CommonMark and GitHub Flavoured Markdown (GFM) spec.
- 🎨 Customizable themes.
- ✍️ Presentation can contain one or more slides in a single markdown file spearated by thematic breaks.
- 🖼️ Images are supported on some terminals (like `kitty` and `wezterm`).
- 🎨 Code highlighting support for a wide list of programming languages.

## Usage 💻

Run the program and the pass the markdown source file:

```bash
tmark source.md
```

Additional flags:

```
-t, --theme THEME  (str, default=gruvbox) theme to use
-h, --help         show this help message and exit
```
