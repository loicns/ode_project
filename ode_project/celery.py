"""
This module configures the Celery application for the 'myproject' project.

Celery is an asynchronous task queue/job queue based on distributed message passing. 
It is focused on real-time operation, but supports scheduling as well.

This module sets up the broker URL, result backend, accepted content types, 
task serializer, project directory, application name, and beat scheduler for Celery.

The broker URL and result backend are set to use RabbitMQ, a popular open-source 
message-broker software that implements the Advanced Message Queuing Protocol (AMQP).

The accepted content types are set to JSON, and the task serializer is also set to JSON, 
meaning that tasks will be serialized as JSON messages for transmission over the broker.

The project directory is set to the base directory of the 'myproject' project, 
and the application name is set to 'myproject'.

The beat scheduler is set to use django-celery-beat, a Celery Beat scheduler that 
uses the Django ORM for storing schedules and related information.
"""
import os

# Set the broker URL (replace with your RabbitMQ details)
CELERY_BROKER_URL = 'amqp://guest:Key4Work@localhost:15672/'

# Set the backend for task results (optional)
CELERY_RESULT_BACKEND = 'amqp://guest:Key4Work@localhost:15672/'

# Accept content types (JSON by default)
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'

# Set project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set Celery app name
CELERY_APP_NAME = 'myproject'  # Replace with your project name

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
