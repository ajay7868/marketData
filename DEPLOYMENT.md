# Deployment Guide for Vercel

This guide explains how to deploy the Stock Chart Pattern Drawing Tool to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI** (optional): Install with `npm i -g vercel`
3. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, or Bitbucket)

## Deployment Steps

### Method 1: Deploy via Vercel Dashboard (Recommended)

1. **Push to Git Repository**:
   ```bash
   git add .
   git commit -m "Add Vercel deployment configuration"
   git push origin main
   ```

2. **Connect to Vercel**:
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your Git repository
   - Vercel will automatically detect the Python configuration

3. **Configure Project**:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (default)
   - **Build Command**: Leave empty (no build step required)
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

4. **Deploy**:
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be available at `https://your-project-name.vercel.app`

### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Follow the prompts**:
   - Link to existing project or create new
   - Confirm settings
   - Deploy

## File Structure for Vercel

```
├── api/
│   └── index.py          # Vercel API handler
├── index.html            # Frontend interface
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── package.json          # Node.js metadata (optional)
├── .vercelignore         # Files to ignore during deployment
└── DEPLOYMENT.md         # This file
```

## Configuration Files

### vercel.json
- Defines build configuration and routing
- Routes API calls to `/api/index.py`
- Serves static files from root

### requirements.txt
- Lists Python dependencies (Flask, Vercel)
- Automatically installed during deployment

### .vercelignore
- Excludes unnecessary files from deployment
- Reduces deployment size and time

## Environment Variables

No environment variables are required for basic functionality.

## API Endpoints

After deployment, your API will be available at:
- `https://your-project.vercel.app/api/load_data` - Load market data
- `https://your-project.vercel.app/api/save_pattern` - Save patterns
- `https://your-project.vercel.app/api/load_pattern` - Load patterns

## Troubleshooting

### Common Issues

1. **Import Errors**:
   - Ensure all dependencies are in `requirements.txt`
   - Check that file paths use `/tmp/` for temporary files

2. **File Upload Issues**:
   - Vercel has a 4.5MB file size limit
   - Use `/tmp/` directory for temporary file storage

3. **CORS Issues**:
   - Vercel handles CORS automatically for same-origin requests
   - No additional CORS configuration needed

### Debugging

1. **Check Vercel Logs**:
   - Go to your project dashboard
   - Click on "Functions" tab
   - View logs for any errors

2. **Local Testing**:
   ```bash
   # Test the API locally
   python3 api/index.py
   ```

## Custom Domain (Optional)

1. **Add Domain**:
   - Go to project settings
   - Add your custom domain
   - Configure DNS records as instructed

2. **SSL Certificate**:
   - Automatically provided by Vercel
   - HTTPS enabled by default

## Performance Considerations

- **Cold Starts**: First request may be slower (1-2 seconds)
- **File Storage**: Use `/tmp/` directory (temporary, 512MB limit)
- **Memory**: 1024MB limit per function
- **Timeout**: 10 seconds for Hobby plan, 60 seconds for Pro

## Cost

- **Hobby Plan**: Free (with limitations)
- **Pro Plan**: $20/month (higher limits)
- **Enterprise**: Custom pricing

## Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Python Runtime**: [vercel.com/docs/runtimes#official-runtimes/python](https://vercel.com/docs/runtimes#official-runtimes/python)
- **Community**: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)
