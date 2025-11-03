# Label Studio Login Guide

## Quick Answer

**Label Studio has NO default credentials!**

You **must create an account** the first time you access it.

## First Time Access

1. Start Label Studio:
```bash
cd label_studio
docker compose up -d
```

2. Open browser: http://localhost:8080

3. You'll see a **Sign Up** page (not login!)

4. Create your account:
   - Email: `your-email@localhost` (can be anything)
   - Password: Choose a strong password
   - Click **Create Account**

5. You're in! This account is saved in the database.

## Subsequent Access

- Use the **same email and password** you created
- If you forgot, see [Password Reset](#password-reset) below

## Common Issues

### "I can't login"

**Possible reasons:**

1. **You never created an account**
   - Solution: Look for "Sign Up" link on login page
   - Create an account first

2. **Wrong password**
   - Solution: Reset password (see below)

3. **Browser cached old login**
   - Solution: Clear browser cache or use incognito mode

### "I forgot my password"

**Option 1: Start Fresh (Easy but loses data)**

```bash
cd label_studio

# Stop Label Studio
docker compose down

# Delete database (WARNING: all annotations will be lost!)
rm -rf data/

# Restart
docker compose up -d

# Open browser - you'll see Sign Up page again
firefox http://localhost:8080
```

**Option 2: Change Password (Keeps data)**

```bash
cd label_studio

# Access the container
docker compose exec label-studio bash

# Inside container, change password
python /label-studio/label_studio/manage.py changepassword your-email@localhost

# Follow prompts to enter new password

# Exit
exit
```

Then use your new password to login.

### "Sign up page doesn't appear"

The database might already exist with an account.

**Check if database exists:**
```bash
ls -la label_studio/data/label_studio.sqlite3
```

If it exists, someone already created an account. Try:
1. Ask who created it
2. Or reset database (see Option 1 above)

## Creating Additional Users

Label Studio supports multiple users:

1. Login as admin (first user created is admin)
2. Go to **Settings** → **Users**
3. Click **Add User**
4. Set email and password for new user
5. New user can login with their credentials

## Security Notes

- **Email doesn't need to be real** - it's just a username
- **Password is stored securely** in the database
- **Database is in** `label_studio/data/label_studio.sqlite3`
- **Backup your data** regularly if you have important annotations

## Default Database Location

```
label_studio/
└── data/
    ├── label_studio.sqlite3  # User accounts & project data
    └── media/                # Uploaded files
```

## Example First Login Session

```bash
# 1. Start Label Studio
cd /home/rafa/PycharmProjects/AnimalDetector/label_studio
docker compose up -d

# 2. Open browser
firefox http://localhost:8080

# 3. You see "Sign Up" page
# Fill in:
#   Email: rafa@localhost
#   Password: YourSecurePassword123
# Click "Create Account"

# 4. You're logged in!
# Create your first project

# 5. Next time you visit:
# Use same credentials:
#   Email: rafa@localhost
#   Password: YourSecurePassword123
```

## FAQ

**Q: What are the default credentials?**  
A: There are none. You create your own account on first use.

**Q: Can I have multiple accounts?**  
A: Yes! First user is admin and can create more users.

**Q: Where is my password stored?**  
A: Securely hashed in `label_studio/data/label_studio.sqlite3`

**Q: Can I use Label Studio without creating an account?**  
A: No, authentication is required.

**Q: I lost all my annotations after resetting!**  
A: Resetting the database (`rm -rf data/`) deletes everything. Always backup first:
```bash
tar -czf backup-$(date +%Y%m%d).tar.gz data/
```

**Q: Can I disable authentication?**  
A: Not recommended, but you can set environment variable `LABEL_STUDIO_DISABLE_SIGNUP_WITHOUT_LINK=false` in docker-compose.yml

## Backup Before Reset

**Always backup before deleting data:**

```bash
cd label_studio

# Create backup
tar -czf ../label-studio-backup-$(date +%Y%m%d-%H%M%S).tar.gz data/

# Now safe to reset
rm -rf data/
docker compose up -d
```

## Summary

- ✅ **No default credentials** - you create them
- ✅ **First user is admin** - can manage other users
- ✅ **Password stored securely** - in SQLite database
- ✅ **Reset if forgotten** - but loses data unless you change via Django command
- ✅ **Backup regularly** - `tar -czf backup.tar.gz data/`

---

**Quick Command Reference:**

```bash
# First time: just open browser and sign up
firefox http://localhost:8080

# Forgot password? Reset database (loses data)
docker compose down && rm -rf data/ && docker compose up -d

# Forgot password? Change it (keeps data)
docker compose exec label-studio python /label-studio/label_studio/manage.py changepassword your-email
```

---

**Date:** November 3, 2025  
**Topic:** Label Studio Authentication  
**Key Point:** NO default credentials - you create your own!

