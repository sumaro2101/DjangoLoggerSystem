# Django Logger Library

A lightweight library for Django providing automated log rotation with **zip compression** (`.zip`) to save disk space.

## ⚙ Environment Variables

Configure behavior in your `.env` file:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `DJANGO_LOG_LEVEL` | Minimum level (`INFO`, `DEBUG`, `WARNING`) | `INFO` |
| `LOG_ROTATION_MB_VALUE` | Max file size (MB) before rotation | `5` |
| `LOG_ROTATION_BACKUP_COUNT` | Number of `.zip` files to keep | `5` |

## 📥 Installation

1. Place `loggers/` folder in your project root.
2. Ensure `.env` is loaded in `manage.py`.

## 🛠 Usage Examples

### 1. Project Configuration (`config/settings.py`)
The library dynamically generates logging configurations for your apps.

```python
# config/settings.py
import os
import logging.config
from dotenv import load_dotenv
from loggers import zip_rotation_handler

load_dotenv()

# ... other settings ...

# Prepare directories
LOGDIR = BASE_DIR / 'logs'

# Initialize handlers for each app
for app_name in ['users', 'products']:
   # Returns (handler_config_dict, logger_config_dict)
   handler_config, logger_config = zip_rotation_handler(
       proj_name=app_name,
       root_dir=LOGDIR
   )

   # Inject into Django's LOGGING dictionary
   LOGGING['handlers'].update(handler_config)
   LOGGING['loggers'].update(logger_config)

logging.config.dictConfig(LOGGING)
```

### 2. Usage in Views/Models
Retrieve the logger by name (matching your `INSTALLED_APPS` entry).

```python
# users/views.py
import logging
from django.views.generic import TemplateView
from .apps import UsersConfig

# 1. Get the logger configured in settings
logger = logging.getLogger(UsersConfig.name)

class UserView(TemplateView):
   def get_context_data(self, **kwargs):
       # 2. Simple logging
       logger.info(f"User viewed with kwargs: {kwargs}")
       return super().get_context_data(**kwargs)
```

### 3. Output
The library creates directories inside `logs/`.
*   Current logs: `logs/users/users_file.log` (plain text).
*   Archived logs: `logs/users/users_file.zip` (compressed).
```