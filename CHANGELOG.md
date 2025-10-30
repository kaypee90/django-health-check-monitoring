# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation suite
  - Installation guide with step-by-step instructions
  - Configuration documentation with all settings explained
  - Usage guide with examples and best practices
  - API reference with complete function and model documentation
  - Contributing guidelines
- Example configurations for different environments
  - Development settings example
  - Production settings example
  - Docker Compose setup
  - Systemd service configuration
  - Supervisor configuration
- Enhanced README with badges, features list, and quick start guide

### Changed
- Improved README.rst with better structure and more examples
- Better documentation organization with dedicated docs directory

## [0.1.0] - 2023

### Added
- Initial release of Django Health Check Monitoring
- Core monitoring functionality with `monitor` management command
- Integration with django-health-check for plugin support
- Database persistence feature (`PERSIST_HEALTH_CHECK_DATA`)
  - `HeathCheckJob` model for storing health check results
  - Admin interface for viewing historical data
- External monitoring server sync feature (`SYNC_HEALTH_CHECK_DATA`)
  - POST health check data to external services
  - Configurable monitoring server URL and app ID
- Configurable health check interval (`HEALTH_CHECK_INTERVAL`)
- Scheduled health check execution using the `schedule` library
- Support for all standard django-health-check plugins:
  - Database connectivity checks
  - Cache backend checks
  - Storage checks
  - Migration checks
  - And more...

### Dependencies
- Django >= 2.2
- django-health-check >= 3.17.0
- schedule >= 1.2.1
- Python >= 3.7

## Release Notes

### v0.1.0 - Initial Release

This is the first release of Django Health Check Monitoring, providing basic but powerful health monitoring capabilities for Django applications.

**Key Features:**
- Continuous health monitoring with configurable intervals
- Dual storage options (local database and/or external monitoring service)
- Django admin integration for easy data access
- Support for all django-health-check plugins
- Simple configuration via Django settings

**Use Cases:**
- Development: Monitor application health during development with database persistence
- Production: Send health metrics to external monitoring services
- Compliance: Store health check history for auditing purposes
- Debugging: Review historical health check data to identify patterns

**Getting Started:**
1. Install: `pip install django-health-check-job`
2. Add to `INSTALLED_APPS`
3. Run migrations: `python manage.py migrate`
4. Configure settings
5. Run monitor: `python manage.py monitor`

For detailed installation and usage instructions, see the documentation in the `docs/` directory.

---

## Version History Summary

| Version | Release Date | Key Changes |
|---------|--------------|-------------|
| 0.1.0   | 2023         | Initial release with core monitoring features |

## Upgrade Guide

### Upgrading to Future Versions

When new versions are released, upgrade instructions will be provided here.

General upgrade process:
1. Review the changelog for breaking changes
2. Update the package: `pip install --upgrade django-health-check-job`
3. Run migrations: `python manage.py migrate`
4. Review and update settings if needed
5. Restart the monitor service

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## Support

- **Issues**: https://github.com/kaypee90/django-health-check-monitoring/issues
- **Documentation**: See `docs/` directory
- **Source**: https://github.com/kaypee90/django-health-check-monitoring
