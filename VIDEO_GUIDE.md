# 🎥 Video Demonstration Guide

## Overview
Create a 4-minute video demonstration covering application features, CI/CD pipeline, and technical explanations.

## Recording Requirements
- **Format**: MP4
- **Duration**: Maximum 4 minutes
- **Quality**: 1080p recommended
- **Audio**: Clear narration required
- **File Size**: Maximum 100MB
- **Platform**: YouTube (unlisted) or Google Drive

## Recommended Recording Tools
- **Windows**: OBS Studio, Camtasia, Xbox Game Bar
- **Mac**: QuickTime, ScreenFlow, OBS Studio
- **Linux**: OBS Studio, SimpleScreenRecorder

## Video Structure (4 minutes)

### Part 1: Application Demo (90 seconds)

**Script Template:**

"Hello, this is [Your Name], demonstrating my Library Management System for the DevOps coursework.

First, let me show you the application running on my production server at [your-domain].uz with a valid SSL certificate [show padlock in browser].

Here's the home page showing our library statistics and recent books [navigate home page].

Let me demonstrate the authentication system - I'll log in as a test user [perform login].

Now I'm in my dashboard where I can see my borrowed books [show dashboard].

Let me browse the book catalog [navigate to books page]. I can search and filter by category [demonstrate search].

Here's a book detail page [click on a book]. I can borrow this book [click borrow button, show success message].

In my borrowed books section, you can see the book I just borrowed with the due date [navigate to my books].

Now let me return this book [click return button, show confirmation].

The admin panel provides full management capabilities [show admin panel briefly].

This demonstrates all CRUD operations working correctly."

**What to Show:**
- ✅ Home page with statistics
- ✅ User login
- ✅ Book list with search
- ✅ Book detail page
- ✅ Borrow a book
- ✅ My borrowed books
- ✅ Return a book
- ✅ Admin panel

### Part 2: CI/CD Pipeline (90 seconds)

**Script Template:**

"Now let me demonstrate the CI/CD pipeline in action.

I'm going to make a small change to the code [open code editor]. I'll add a comment here in the home view [make visible change].

Now I'll commit and push this change to GitHub [show git commands]:

```bash
git add .
git commit -m 'Update home view documentation'
git push origin main
```

The push automatically triggers our GitHub Actions workflow [navigate to GitHub Actions page].

You can see the pipeline has four main stages:

First, Code Quality checks with Flake8 linting [show job running].

Second, the Test stage running our pytest suite with 15+ tests against a PostgreSQL database [show tests].

Third, the Build and Push stage creating our Docker image and pushing to Docker Hub [show Docker job].

Finally, the Deploy stage connecting to our production server via SSH, pulling the latest images, running migrations, and restarting services [show deployment job].

All stages are passing successfully [show green checkmarks].

Let me check Docker Hub - you can see our new image has been pushed with the latest tag and commit SHA [show Docker Hub].

And now refreshing the production site, our changes are live with zero downtime [show production site]."

**What to Show:**
- ✅ Make code change
- ✅ Git commit and push
- ✅ GitHub Actions workflow triggered
- ✅ All pipeline stages (Code Quality, Tests, Build, Deploy)
- ✅ Each stage's purpose explained
- ✅ Green checkmarks (all passing)
- ✅ Docker Hub showing new image
- ✅ Production site updated

### Part 3: Technical Explanation (60 seconds)

**Script Template:**

"Let me explain the technical architecture.

Here's our docker-compose.yml file [open file, scroll through].

We have three main services: PostgreSQL for the database, Django running on Gunicorn for the application, and Nginx as a reverse proxy.

Each service has its own configuration. The database uses a persistent volume for data retention [point to volumes section].

The Django service depends on the database health check, ensuring the database is ready before the app starts [point to depends_on].

Nginx serves static files directly and proxies dynamic requests to Gunicorn [point to nginx config].

Here's our Dockerfile [open Dockerfile]. We use a multi-stage build - the first stage installs dependencies, the second stage creates a lightweight production image under 200MB [scroll through].

We run as a non-root user for security [point to USER directive].

Our Nginx configuration [open nginx.conf] handles SSL termination, serves static files with caching, and includes security headers like HSTS and XSS protection.

The deployment is fully automated - any push to main triggers testing, building, and deployment to production."

**What to Show:**
- ✅ docker-compose.yml structure
- ✅ Three services explained
- ✅ Dockerfile multi-stage build
- ✅ Non-root user configuration
- ✅ Nginx configuration
- ✅ Volume and network setup

## Recording Tips

### Before Recording
1. ✅ Close unnecessary applications
2. ✅ Clear browser history and cache
3. ✅ Use incognito/private browsing
4. ✅ Prepare test data in database
5. ✅ Have all files open in tabs
6. ✅ Test microphone audio
7. ✅ Practice your script 2-3 times
8. ✅ Set browser zoom to 100%
9. ✅ Hide bookmarks bar
10. ✅ Close notification popups

### During Recording
1. Speak clearly and at moderate pace
2. Use your mouse to point at important elements
3. Pause briefly between sections
4. If you make a mistake, pause and continue (edit later)
5. Show your face (optional but adds personality)
6. Keep browser window maximized
7. Don't rush - 4 minutes is enough time

### After Recording
1. Trim any dead air at beginning/end
2. Add simple title card (optional)
3. Add captions/subtitles (optional but helpful)
4. Compress if file size > 100MB
5. Upload to YouTube as "Unlisted" or Google Drive
6. Test the link before submission

## File Size Reduction

If your video exceeds 100MB:

### Using HandBrake (Free)
1. Download HandBrake
2. Open your video
3. Preset: "Fast 1080p30"
4. Quality: RF 23-25
5. Start encode

### Using FFmpeg (Command Line)
```bash
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k output.mp4
```

### Using Online Tool
- CloudConvert.com
- FreeConvert.com
- YouCompress.com

## YouTube Upload Steps

1. Go to YouTube Studio
2. Click "Create" → "Upload video"
3. Select your video file
4. **Title**: "Library Management System - DevOps Project Demo"
5. **Description**: 
   ```
   Library Management System demonstration for DevOps coursework.
   
   Demonstrates:
   - Django web application with full CRUD operations
   - Docker containerization with multi-stage builds
   - CI/CD pipeline with GitHub Actions
   - Production deployment with HTTPS
   - PostgreSQL, Nginx, Gunicorn stack
   
   Student: [Your Name]
   Student ID: [Your ID]
   Date: February 2026
   ```
6. **Visibility**: Unlisted
7. **Audience**: Not made for kids
8. Click "Next" through all steps
9. Click "Publish"
10. Copy the video URL

## Quality Checklist

Before submitting your video:

- [ ] Duration is under 4 minutes
- [ ] File size is under 100MB
- [ ] Audio is clear and audible
- [ ] Screen recording is sharp (1080p)
- [ ] All required features demonstrated
- [ ] CI/CD pipeline shown in action
- [ ] Code change visible
- [ ] Deployment successful
- [ ] Technical architecture explained
- [ ] No sensitive information shown (passwords, keys)
- [ ] Video link is accessible (test in incognito)
- [ ] Video is set to "Unlisted" (not Private)

## Common Mistakes to Avoid

❌ **Don't:**
- Rush through sections
- Show passwords or API keys
- Use low quality recording (720p or less)
- Have long silent pauses
- Make video too long (over 4 minutes)
- Forget to narrate your actions
- Show messy desktop/files
- Upload as "Private" (assessor can't view)

✅ **Do:**
- Speak clearly and explain each action
- Use test/demo credentials
- Record in 1080p
- Keep it concise and focused
- Narrate everything you're doing
- Have clean, professional environment
- Upload as "Unlisted"

## Example Timeline

| Time | Content |
|------|---------|
| 0:00-0:10 | Introduction and overview |
| 0:10-1:40 | Application demo (features) |
| 1:40-3:10 | CI/CD pipeline demonstration |
| 3:10-4:00 | Technical explanation |

## Submission Format

Include in your submission document:

```
Video Demonstration Link: https://youtu.be/YOUR_VIDEO_ID

Video Password (if applicable): N/A

Video Duration: 3:45

Video uploaded to: YouTube (Unlisted)
```

## Need Help?

If you encounter issues:
- Test your recording setup beforehand
- Practice your script multiple times
- Record in segments if needed
- Use editing software to combine clips
- Ask a friend to review before submission

Good luck with your video! 🎬
