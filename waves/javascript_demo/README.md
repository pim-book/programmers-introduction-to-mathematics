# Springs demo

To view the live demo visit [pimbook.org](https://pimbook.org)

# Run locally

If you want to run this demo locally, you can simply clone the repo and open index.html.

If you want to edit the code (you plucky little ruffian), you'll have to install the Javascript dependencies.

```
yarn install  # or npm install
# edit files...
gulp build    # or gulp watch for auto builds
open index.html
```

 - `geometry.js`: contains basic, model-agnostic vector arithmetic
 - `springs.js`: containts spring physics specific to this system
 - `main.js`: contains d3 visualization setup and interaction with DOM
