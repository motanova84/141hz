# QCAL Demo Deployment Guide

This document provides detailed instructions for deploying the QCAL-LLM ∞³ Quantum Coherence Evaluator to Vercel.

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Vercel account (free tier works)
- Vercel CLI installed: `npm install -g vercel`

## Local Development

### First-time Setup

```bash
# Navigate to the app directory
cd apps/qcal-demo

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at `http://localhost:3000`.

### Build Locally

```bash
# Test production build
npm run build

# Start production server locally
npm start
```

### Linting and Type Checking

```bash
# Run ESLint
npm run lint

# TypeScript type checking is done automatically during build
```

## Deployment to Vercel

### Option 1: Vercel CLI (Recommended for First Deployment)

1. **Login to Vercel**
   ```bash
   vercel login
   ```

2. **Deploy from the app directory**
   ```bash
   cd apps/qcal-demo
   vercel
   ```

3. **Follow the prompts:**
   - Set up and deploy? **Y**
   - Which scope? Select your account
   - Link to existing project? **N** (first time)
   - Project name? **qcal-demo** (or your preferred name)
   - In which directory is your code located? **./**
   - Want to modify settings? **N**

4. **Deploy to production**
   ```bash
   vercel --prod
   ```

### Option 2: Vercel Dashboard (Git Integration)

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Add QCAL demo application"
   git push origin main
   ```

2. **Import project in Vercel Dashboard**
   - Go to https://vercel.com/new
   - Import your repository
   - Set the **Root Directory** to: `apps/qcal-demo`
   - Framework Preset: **Next.js**
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`
   - Click **Deploy**

3. **Configure Production Domain**
   - After deployment, go to project Settings → Domains
   - Add custom domain (e.g., `qcal-consciousness.vercel.app`)

### Option 3: Monorepo Deployment

If deploying from the root of the repository:

**vercel.json** (root level):
```json
{
  "version": 2,
  "builds": [
    {
      "src": "apps/qcal-demo/package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/qcal/(.*)",
      "dest": "apps/qcal-demo/$1"
    }
  ]
}
```

## Environment Configuration

### Environment Variables

The application doesn't require environment variables for basic operation. However, you can optionally configure:

- `NODE_ENV`: Set to `production` (automatic in Vercel)
- `NEXT_PUBLIC_API_URL`: If using external API endpoint

To add environment variables in Vercel:
1. Go to Project Settings → Environment Variables
2. Add variables for Production, Preview, and Development
3. Redeploy for changes to take effect

## Build Configuration

The application uses:
- **Framework**: Next.js 14 with App Router
- **Build Output**: Standalone mode for optimized deployment
- **Node Version**: 18.x (Vercel default)
- **Package Manager**: npm

## Performance Optimization

### Automatic Optimizations by Vercel

- ✅ Automatic HTTPS
- ✅ Global CDN distribution
- ✅ Image optimization
- ✅ Edge caching
- ✅ Gzip/Brotli compression

### Application-specific Optimizations

- Three.js particle system limited to 5000 particles
- WebGL rendering with hardware acceleration
- Code splitting for optimal loading
- CSS purging via Tailwind

## Post-Deployment Verification

1. **Check Deployment Status**
   ```bash
   vercel ls
   ```

2. **View Deployment Logs**
   ```bash
   vercel logs
   ```

3. **Test Core Features:**
   - [ ] Page loads with 3D visualization
   - [ ] Text input accepts content
   - [ ] Evaluation API returns results
   - [ ] Animation renders Ψ value smoothly
   - [ ] Audio button plays 141.7 Hz frequency
   - [ ] Share button copies to clipboard
   - [ ] Links to GitHub, ORCID, Zenodo work

4. **Performance Testing:**
   - Run Lighthouse audit (target: 90+ performance score)
   - Test on mobile devices
   - Verify WebGL compatibility

## Custom Domain Setup

1. **Purchase domain** (e.g., via Namecheap, GoDaddy)

2. **Add to Vercel:**
   - Project Settings → Domains
   - Enter your domain name
   - Add DNS records as instructed:
     ```
     Type: A
     Name: @
     Value: 76.76.21.21
     
     Type: CNAME  
     Name: www
     Value: cname.vercel-dns.com
     ```

3. **Wait for DNS propagation** (up to 48 hours)

4. **Enable HTTPS** (automatic via Let's Encrypt)

## Monitoring and Analytics

### Vercel Analytics (Optional)

Add Vercel Analytics for performance monitoring:

```bash
npm install @vercel/analytics
```

Update `app/layout.tsx`:
```typescript
import { Analytics } from '@vercel/analytics/react'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
```

### Error Monitoring

Consider integrating:
- Sentry for error tracking
- LogRocket for session replay
- Google Analytics for user metrics

## Troubleshooting

### Build Fails

**Issue**: `Module not found: Can't resolve 'three'`
**Solution**: Ensure all dependencies are in `package.json`:
```bash
npm install three @types/three framer-motion
```

**Issue**: `Font loading error`
**Solution**: Already fixed in layout.tsx by removing Google Fonts

### Deployment Issues

**Issue**: "No Build Cache Found"
**Solution**: Normal for first build, subsequent builds will be faster

**Issue**: API routes return 404
**Solution**: Verify file structure: `app/api/evaluate/route.ts`

### Runtime Errors

**Issue**: WebGL context lost
**Solution**: Implement context restoration in Three.js cleanup

**Issue**: Audio doesn't play
**Solution**: User must interact with page first (browser autoplay policy)

## Scaling Considerations

### Current Limits (Vercel Free Tier)
- 100 GB bandwidth/month
- 100 hours of build time/month
- Serverless function execution: 100 GB-hours

### Upgrading
If traffic exceeds free tier:
- Pro Plan: $20/month (1 TB bandwidth)
- Enterprise: Custom pricing for high traffic

## Continuous Deployment

Once connected to Git:
1. Push to `main` branch → auto-deploy to production
2. Push to feature branches → auto-deploy preview
3. Pull requests get unique preview URLs

## Rollback Procedure

If deployment has issues:

```bash
# List deployments
vercel ls

# Promote specific deployment to production
vercel promote <deployment-url>
```

Or via Dashboard:
1. Go to Deployments
2. Find working deployment
3. Click "..." → Promote to Production

## Security Considerations

- ✅ HTTPS enforced automatically
- ✅ No secrets in client-side code
- ✅ API routes use Next.js server-side
- ✅ Input validation in evaluation API
- ⚠️ Add rate limiting for production (optional)

## Maintenance

### Regular Updates

```bash
# Update dependencies
npm update

# Check for security vulnerabilities
npm audit

# Fix auto-fixable issues
npm audit fix
```

### Monitoring

- Check Vercel dashboard weekly
- Review error logs
- Monitor bandwidth usage
- Update Next.js quarterly

## Support Resources

- Vercel Documentation: https://vercel.com/docs
- Next.js Documentation: https://nextjs.org/docs
- QCAL Framework: See main repository README
- Issues: GitHub repository issues

## Cost Estimate

**Free Tier (Hobby)**:
- Suitable for: Development, demos, low-traffic projects
- Cost: $0/month
- Bandwidth: 100 GB
- Build time: 100 hours

**Pro Tier**:
- Suitable for: Production apps, moderate traffic
- Cost: $20/month per user
- Bandwidth: 1 TB
- Build time: 400 hours

**Enterprise**:
- Suitable for: High-traffic applications
- Cost: Custom pricing
- Unlimited bandwidth
- Priority support

## Recommended URL

Once deployed, your application will be available at:
- **Development**: `https://qcal-demo-xxx.vercel.app`
- **Production** (suggested): `https://qcal-consciousness.vercel.app`

---

## Quick Reference

**Deploy Command**: `vercel --prod`  
**Logs**: `vercel logs`  
**Redeploy**: `vercel --prod --force`  
**Domain**: Project Settings → Domains  
**Environment**: Project Settings → Environment Variables

---

**Last Updated**: 2025-11-04  
**Version**: 1.0.0
