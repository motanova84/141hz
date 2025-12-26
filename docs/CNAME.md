# CNAME Configuration for Custom Domain

This file is optional. If you want to use a custom domain:

1. **Option A: Via Workflow (Recommended)**
   
   Edit `.github/workflows/docs.yml` and uncomment the `cname:` line:
   
   ```yaml
   - name: Deploy to GitHub Pages
     uses: peaceiris/actions-gh-pages@v3
     with:
       github_token: ${{ secrets.GITHUB_TOKEN }}
       publish_dir: ./site
       publish_branch: gh-pages
       force_orphan: true
       cname: your-domain.com  # Uncomment and set your domain
   ```

2. **Option B: Create docs/CNAME file**
   
   Create a file at `docs/CNAME` containing just your domain:
   ```
   your-domain.com
   ```

3. **DNS Configuration**
   
   In your DNS provider, create a CNAME record pointing to:
   ```
   motanova84.github.io.
   ```
   
   Or for apex domains, create A records pointing to GitHub Pages IPs.

## Default

By default, the site will be available at:
https://motanova84.github.io/141hz
