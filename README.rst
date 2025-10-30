Django Health Check Monitoring
==============================

Django Health Check Monitoring is a Python library designed to enhance monitoring capabilities in Django applications. It captures data emitted by Django Health Check and pushes it to backend services for visualization.

.. image:: https://img.shields.io/pypi/v/django-health-check-job.svg
   :target: https://pypi.org/project/django-health-check-job/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/django-health-check-job.svg
   :target: https://pypi.org/project/django-health-check-job/
   :alt: Python versions

.. image:: https://img.shields.io/badge/django-2.2%2B-blue.svg
   :target: https://www.djangoproject.com/
   :alt: Django versions

Features
--------

✨ **Enhanced Monitoring**: Provides additional monitoring capabilities for Django applications by capturing and analyzing health check data.

🔌 **Integration with Django Health Check**: Seamlessly integrates with Django Health Check, allowing you to leverage existing health checks in your application.

💾 **Database Persistence**: Optionally store health check results in your database for historical analysis.

📡 **Backend Services Integration**: Push captured health check data to backend monitoring services for visualization and analysis in real-time.

⏰ **Scheduled Monitoring**: Run health checks continuously at configurable intervals.

🎯 **Admin Interface**: View and filter health check results through the Django admin.

Quick Start
-----------

Installation
~~~~~~~~~~~~

Install using pip:

.. code-block:: bash

    pip install django-health-check-job

Add to your ``INSTALLED_APPS`` in ``settings.py``:

.. code-block:: python

    INSTALLED_APPS = [
        # ... other apps
        'django_health_check_job',
        'health_check',
        'health_check.db',
        'health_check.cache',
        'health_check.storage',
    ]

Run migrations:

.. code-block:: bash

    python manage.py migrate django_health_check_job

Configuration
~~~~~~~~~~~~~

Configure in your ``settings.py``:

.. code-block:: python

    # Health check interval in seconds
    HEALTH_CHECK_INTERVAL = 60
    
    # Enable database persistence
    PERSIST_HEALTH_CHECK_DATA = True
    
    # Enable syncing to external monitoring server
    SYNC_HEALTH_CHECK_DATA = True
    SYNC_SERVER_URL = "https://monitoring.example.com"
    SYNC_APP_ID = "my-django-app"

Usage
~~~~~

Run the monitoring command:

.. code-block:: bash

    python manage.py monitor

This will continuously run health checks at the configured interval and process the results.

Example output:

.. code-block:: text

    DatabaseBackend          ... working 
    CacheBackend            ... working 
    StorageHealthCheck      ... working

Documentation
-------------

For comprehensive documentation, see the ``docs/`` directory:

- `Quick Start Guide <docs/quickstart.md>`_ ⚡ - Get up and running in 5 minutes!
- `Installation Guide <docs/installation.md>`_ - Detailed installation instructions
- `Configuration <docs/configuration.md>`_ - All configuration options and examples
- `Usage Guide <docs/usage.md>`_ - How to use the monitor command and integrate with other systems
- `API Reference <docs/api-reference.md>`_ - Complete API documentation

Requirements
------------

- Python >= 3.7
- Django >= 2.2
- django-health-check >= 3.17.0
- schedule >= 1.2.1

Available Health Check Plugins
-------------------------------

Django Health Check Monitoring works with all django-health-check plugins:

- ``health_check.db`` - Database connectivity
- ``health_check.cache`` - Cache backend
- ``health_check.storage`` - Storage backend
- ``health_check.contrib.migrations`` - Migrations status
- ``health_check.contrib.celery`` - Celery workers
- ``health_check.contrib.psutil`` - System resources
- ``health_check.contrib.redis`` - Redis connectivity
- And more...

Contributing
------------

Contributions are welcome! Please see `CONTRIBUTING.md <CONTRIBUTING.md>`_ for guidelines.

To contribute:

1. Fork the repository
2. Create a feature branch (``git checkout -b feature/amazing-feature``)
3. Make your changes
4. Run tests (``python manage.py test``)
5. Commit your changes (``git commit -m 'Add amazing feature'``)
6. Push to the branch (``git push origin feature/amazing-feature``)
7. Open a Pull Request

License
-------

This project is licensed under the MIT License - see the `LICENSE <LICENSE>`_ file for details.

Links
-----

- **GitHub**: https://github.com/kaypee90/django-health-check-monitoring
- **Issues**: https://github.com/kaypee90/django-health-check-monitoring/issues
- **PyPI**: https://pypi.org/project/django-health-check-job/

Support
-------

If you encounter any issues or have questions:

1. Check the `documentation <docs/>`_
2. Search `existing issues <https://github.com/kaypee90/django-health-check-monitoring/issues>`_
3. Create a new issue with detailed information

Acknowledgments
---------------

- Built on top of `django-health-check <https://github.com/revsys/django-health-check>`_
- Uses `schedule <https://github.com/dbader/schedule>`_ for periodic task execution
