# Database Repository

## Purpose

This folder contains all database-related assets used by the Odoo AI Audit Platform.

## Structure

- metadata/ : Database metadata extracted from Odoo
- exports/raw/ : Original exported files from Odoo (never modified)
- exports/processed/ : Cleaned and processed datasets
- exports/archive/ : Historical exports
- sql/ : SQL queries
- scripts/ : Database extraction scripts

## Security Rules

- Never store passwords.
- Never upload production database backups.
- Never modify files inside exports/raw.
- All processed files must be reproducible from raw exports.