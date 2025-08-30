# OneSignal ERPNext Integration

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Frappe](https://img.shields.io/badge/Frappe-15.0%2B-orange.svg)](https://frappeframework.com/)

A comprehensive OneSignal push notification integration for ERPNext, enabling real-time notifications with Progressive Web App (PWA) support.

## 🚀 Features

- **Push Notifications**: Send notifications to specific users, roles, or all users
- **PWA Support**: Convert your ERPNext instance into a Progressive Web App
- **Automatic Integration**: Seamlessly integrates with ERPNext's notification system
- **User Management**: Automatic user login/logout synchronization with OneSignal
- **Chunked Delivery**: Handles large recipient lists efficiently (2000 users per batch)
- **Error Handling**: Comprehensive error logging and handling

## 📋 Prerequisites

- ERPNext/Frappe Framework 15.0 or higher
- Python 3.10 or higher
- OneSignal account and app setup
- Admin access to your ERPNext instance

## 🛠️ Installation

### 1. Install the App

```bash
# Navigate to your bench directory
cd /path/to/your/frappe-bench

# Get the app from repository
bench get-app https://github.com/ebrahimHakimuddin/onesignal_erpnext.git

# Install the app on your site
bench --site your-site-name install-app onesignal_erpnext

# Restart your bench
bench restart
```

### 2. Configure OneSignal API Keys

Edit the API configuration file:

```bash
# Navigate to the app directory
cd apps/onesignal_erpnext/onesignal_erpnext/

# Edit api.py and update your credentials
nano api.py
```

Replace the placeholder values in `api.py`:

```python
settings = {
    "app_id": "YOUR_ACTUAL_ONESIGNAL_APP_ID",
    "api_key": "YOUR_ACTUAL_ONESIGNAL_REST_API_KEY",
}
```

## 🔧 Configuration

### OneSignal Setup

1. **Create OneSignal App**
   - Visit [OneSignal](https://onesignal.com/) and create an account
   - Create a new Web app
   - Note down your **App ID** and **REST API Key**

2. **Configure Website Settings**
   
   Navigate to **Website Settings** > **Header, Robots** section and add:

   ```html
   <script src="https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js" defer></script>
   <script>
     window.OneSignalDeferred = window.OneSignalDeferred || [];
     OneSignalDeferred.push(async function(OneSignal) {
       await OneSignal.init({
         appId: "YOUR_ONESIGNAL_APP_ID",
       });
     });
   </script>
   ```

3. **Add Website Script**
   
   Navigate to **Website Settings** > **Website Script** and add:

   ```javascript
   window.OneSignalDeferred = window.OneSignalDeferred || [];

   frappe.ready(() => {
     OneSignalDeferred.push(async function (OneSignal) {
       if (frappe.session.user === "Guest") {
         await OneSignal.logout();
       } else {
         await OneSignal.login(frappe.session.user);
       }
     });
   });
   ```

4. **Install OneSignal Service Worker**

   OneSignal requires a service worker file to handle push notifications. Create the required worker file in your site's public directory:

   ```bash
   # Navigate to your site's public directory
   cd /path/to/frappe-bench/sites/your-site-name/public

   # Create the OneSignal service worker file
   nano OneSignalSDKWorker.js
   ```

   In the `OneSignalSDKWorker.js` file, paste the following content:

   ```javascript
   importScripts("https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.sw.js");
   ```

   Save and exit the file (Ctrl+X, then Y, then Enter in nano).

   **Important**: Ensure the worker file is accessible at:
   - `https://your-domain.com/OneSignalSDKWorker.js`

### PWA (Progressive Web App) Setup

Transform your ERPNext instance into a mobile-installable PWA:

#### 1. Prepare Logo
- Upload an SVG logo as a public file in ERPNext
- Copy the public URL (e.g., `/files/logo.svg`)

#### 2. Create Manifest File

Create a `manifest.json` file with the following structure:

```json
{
  "name": "ERPNext Mobile",
  "short_name": "ERPNext",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#000000",
  "theme_color": "#000000",
  "description": "Mobile PWA for ERPNext",
  "categories": [
    "business",
    "productivity",
    "utilities"
  ],
  "icons": [
    {
      "src": "/files/logo.svg",
      "sizes": "48x48 72x72 96x96 128x128 256x256 512x512",
      "type": "image/svg+xml",
      "purpose": "any"
    }
  ],
  "id": "erpnext",
  "dir": "auto",
  "lang": "en",
  "orientation": "natural",
  "prefer_related_applications": false,
  "handle_links": "preferred",
  "launch_handler": {
    "client_mode": "navigate-existing"
  }
}
```

#### 3. Upload and Link Manifest

1. Upload `manifest.json` as a public file in ERPNext
2. Add the manifest link to **Website Settings** > **Header, Robots**:

```html
<link rel="manifest" href="/files/manifest.json">
```

3. Ensure the manifest URL is accessible without authentication

## 🎯 Usage

Once configured, the app automatically:

- Sends push notifications for ERPNext notifications
- Manages user authentication with OneSignal
- Handles notifications for specific users, roles, or all users
- Provides PWA installation prompts on supported browsers

### Notification Types

The app supports three notification scenarios:

1. **User-Specific**: Notifications sent to individual users
2. **Role-Based**: Notifications sent to all users with specific roles
3. **Broadcast**: Notifications sent to all active users (excluding Administrator and Guest)

## 🔍 Troubleshooting

### Common Issues

1. **Notifications not sending**
   - Verify OneSignal credentials in `api.py`
   - Check ERPNext error logs: `bench logs`
   - Ensure OneSignal script is properly loaded
   - **Check service worker files**: Verify `OneSignalSDKWorker.js` and `OneSignalSDKUpdaterWorker.js` are accessible at your domain root

2. **PWA not installing**
   - Verify manifest.json is accessible without login
   - Check browser console for manifest errors
   - Ensure HTTPS is enabled on your site

3. **User authentication issues**
   - Verify website script is properly configured
   - Check browser console for JavaScript errors
   - Ensure OneSignal SDK is loaded before custom scripts

4. **Service Worker Issues**
   - Ensure `OneSignalSDKWorker.js` is in the correct location: `/path/to/frappe-bench/sites/your-site-name/public/`
   - Check if the file is accessible: `https://your-domain.com/OneSignalSDKWorker.js`
   - Verify the file contains: `importScripts("https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.sw.js");`
   - Verify file permissions allow web server access
   - Clear browser cache and try again

### Error Logs

Check OneSignal-related errors in ERPNext:

```bash
# View error logs
bench --site your-site-name logs

# Or check specific error log
tail -f sites/your-site-name/logs/error.log | grep OneSignal
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Development Setup

1. **Install Pre-commit Hooks**

```bash
# Install pre-commit
pip install pre-commit

# Navigate to app directory
cd apps/onesignal_erpnext

# Install hooks
pre-commit install
```

2. **Code Quality Tools**

This project uses:
- **ruff**: Python linting and formatting
- **eslint**: JavaScript linting
- **prettier**: Code formatting
- **pyupgrade**: Python syntax upgrades

### Submitting Changes

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and ensure tests pass
4. Run pre-commit: `pre-commit run --all-files`
5. Commit your changes: `git commit -m "Add feature"`
6. Push to your fork: `git push origin feature-name`
7. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](license.txt) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/ebrahimHakimuddin/onesignal_erpnext/issues)
- **Documentation**: [Frappe Documentation](https://frappeframework.com/docs)
- **OneSignal Docs**: [OneSignal Documentation](https://documentation.onesignal.com/)

## 🙏 Acknowledgments

- [Frappe Framework](https://frappeframework.com/) for the excellent foundation
- [OneSignal](https://onesignal.com/) for their comprehensive push notification service
- The ERPNext community for continuous support and feedback

---

**Made with ❤️ for the ERPNext community**
