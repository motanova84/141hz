# Documentation Site Setup Guide

This guide explains the complete documentation setup for the 141Hz project using MkDocs Material.

## 🎯 Features Implemented

### 1. **README Badges**

The README now includes centered badges at the top showing:
- **Docs Status**: Build status of the documentation workflow
- **Last Commit**: Latest commit timestamp
- **Website Status**: Whether the documentation site is online

These badges are automatically updated by GitHub.

### 2. **MkDocs Material Theme**

The project uses [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) with:
- **Dark/Light Mode**: Toggle between themes
- **Spanish Language**: Configured for Spanish content
- **Responsive Design**: Mobile-friendly
- **Search**: Full-text search across all documentation
- **Navigation**: Tab-based navigation with sections

### 3. **Social Cards (OpenGraph/Twitter)**

The site automatically generates social media preview images for sharing:
- **Auto-generation**: Creates unique cards for each page
- **Custom Colors**: Matches project theme (#0f172a background, #e2e8f0 text)
- **Twitter Integration**: Includes @Investigad1154 attribution
- **Summary Large Image**: Optimized for Twitter/X and Facebook

**Note**: Social cards require internet access to download fonts. They work in GitHub Actions but may fail in restricted environments.

### 4. **GitHub Pages Deployment**

Automatic deployment workflow (`.github/workflows/docs.yml`):
- **Trigger**: Runs on push to `main` branch or manual dispatch
- **Build**: Compiles MkDocs site
- **Deploy**: Publishes to `gh-pages` branch
- **URL**: https://motanova84.github.io/141hz

### 5. **Custom Domain Support (Optional)**

Two options for custom domains:

#### Option A: Via Workflow (Recommended)
Edit `.github/workflows/docs.yml` and uncomment:
```yaml
cname: your-domain.com  # e.g., qcal.tech or docs.qcal.tech
```

#### Option B: CNAME File
Create `docs/CNAME` with your domain:
```
your-domain.com
```

Then configure DNS:
- **CNAME Record**: Point to `motanova84.github.io.`
- **Or A Records**: For apex domains, use GitHub Pages IPs

## 📁 Project Structure

```
.
├── docs/                        # Documentation source files
│   ├── index.md                # Homepage (from root README.md)
│   ├── README.md               # Docs directory index
│   ├── CNAME.md                # CNAME setup instructions
│   ├── assets/
│   │   └── brand/
│   │       ├── logo.svg        # Site logo
│   │       ├── favicon.png     # (To be added)
│   │       └── README.md       # Branding instructions
│   └── *.md                    # All documentation pages
├── mkdocs.yml                  # MkDocs configuration
└── .github/workflows/
    └── docs.yml                # Documentation build/deploy workflow
```

## 🚀 Local Development

### Prerequisites
```bash
pip install -r requirements.txt
```

### Build Documentation
```bash
mkdocs build
```

Output goes to `site/` directory (ignored by git).

### Live Preview
```bash
mkdocs serve
```

Visit http://127.0.0.1:8000 to preview.

### Deploy (Manual)
```bash
mkdocs gh-deploy
```

**Note**: Normally deployment is automatic via GitHub Actions.

## 🎨 Customization

### Logo and Favicon

1. **Replace Logo**: Add your SVG logo to `docs/assets/brand/logo.svg`
   - Recommended: 200x200px
   - Should work on light and dark backgrounds

2. **Add Favicon**: Add PNG favicon to `docs/assets/brand/favicon.png`
   - Recommended: 32x32px or 64x64px
   - Then uncomment in `mkdocs.yml`:
   ```yaml
   theme:
     favicon: assets/brand/favicon.png
   ```

3. **Social Card Background**: Customize in `mkdocs.yml`:
   ```yaml
   plugins:
     - social:
         cards_layout_options:
           background_color: "#your-color"
           color: "#text-color"
   ```

### Navigation

Edit `mkdocs.yml` to customize the nav structure:
```yaml
nav:
  - Inicio: index.md
  - Your Section:
    - Page 1: page1.md
    - Page 2: page2.md
```

### Theme Colors

In `mkdocs.yml`:
```yaml
theme:
  palette:
    - scheme: default
      primary: indigo      # Change primary color
      accent: indigo       # Change accent color
```

Available colors: red, pink, purple, deep purple, indigo, blue, light blue, cyan, teal, green, light green, lime, yellow, amber, orange, deep orange

## 📊 Analytics (Optional)

To add Google Analytics, add to `mkdocs.yml`:
```yaml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

## 🔍 SEO Optimization

Already configured:
- ✅ Sitemap (auto-generated)
- ✅ Meta descriptions
- ✅ OpenGraph tags
- ✅ Twitter cards
- ✅ Canonical URLs
- ✅ Last update dates

## 🐛 Troubleshooting

### Social Cards Fail Locally
**Issue**: `Failed to resolve 'fonts.google.com'`

**Solution**: This is expected in restricted networks. Social cards will work in GitHub Actions where internet access is available. You can:
1. Use a VPN/proxy
2. Temporarily disable the social plugin for local builds
3. Accept that social cards only work in CI/CD

### Build Fails on GitHub Actions
**Issue**: Workflow fails with plugin errors

**Solutions**:
1. Check Python version (should be 3.11+)
2. Verify all plugins are in `requirements.txt`
3. Check workflow logs for specific errors

### Pages Not Appearing
**Issue**: Some documentation pages don't show up

**Solution**: 
1. Add them to `nav:` in `mkdocs.yml`
2. Or rely on auto-discovery (all `.md` files in `docs/` are included)

### Custom Domain Not Working
**Issue**: Custom domain shows 404

**Solutions**:
1. Wait 24 hours for DNS propagation
2. Verify CNAME is deployed to `gh-pages` branch
3. Check DNS configuration with `dig your-domain.com`
4. Ensure GitHub Pages is enabled in repo settings

## 📚 Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Social Cards Plugin Guide](https://squidfunk.github.io/mkdocs-material/setup/setting-up-social-cards/)

## ✅ Verification Checklist

After setup, verify:
- [ ] README badges display correctly
- [ ] Documentation workflow runs successfully
- [ ] Site builds without errors
- [ ] Navigation works on deployed site
- [ ] Social cards generate (check `site/assets/images/social/`)
- [ ] Custom domain resolves (if configured)
- [ ] Search works
- [ ] Dark/light mode toggle works
- [ ] Mobile responsive design works

## 🔄 Maintenance

### Adding New Pages
1. Create `.md` file in `docs/`
2. Add to `nav:` in `mkdocs.yml` (optional)
3. Commit and push - auto-deploys!

### Updating Documentation
1. Edit `.md` files in `docs/`
2. Preview with `mkdocs serve`
3. Commit and push - auto-deploys!

### Updating Theme
```bash
pip install --upgrade mkdocs-material
```

Then update version in `requirements.txt`.

## 🎉 Success!

Your documentation site is now:
- ✅ Beautifully styled with Material Design
- ✅ Auto-deployed on every push
- ✅ SEO optimized with social cards
- ✅ Mobile responsive
- ✅ Searchable
- ✅ Monitored with status badges

Visit https://motanova84.github.io/141hz to see it live!
