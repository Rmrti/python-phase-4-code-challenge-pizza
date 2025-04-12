import logging
from logging.config import fileConfig

from flask import Flask, current_app
from alembic import context

from server.app import create_app, db  # Ensure this is correctly importing your app and database

# Alembic configuration
config = context.config

# Configure logging
if config.config_file_name:
    fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

def get_engine():
    """Retrieve the SQLAlchemy engine safely."""
    try:
        return current_app.extensions["migrate"].db.get_engine()
    except (TypeError, AttributeError):
        return current_app.extensions["migrate"].db.engine

def get_engine_url():
    """Retrieve database URL safely from engine."""
    try:
        return get_engine().url.render_as_string(hide_password=False).replace("%", "%%")
    except AttributeError:
        return str(get_engine().url).replace("%", "%%")

# Set database URL dynamically
config.set_main_option("sqlalchemy.url", get_engine_url())

def get_metadata():
    """Retrieve metadata for migrations."""
    target_db = current_app.extensions["migrate"].db
    return target_db.metadatas[None] if hasattr(target_db, "metadatas") else target_db.metadata

def run_migrations_offline():
    """Run migrations in offline mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=get_metadata(), literal_binds=True)
    
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in online mode, ensuring correct app context."""
    app = create_app()
    
    with app.app_context():  # Ensures context is properly handled
        def process_revision_directives(context, revision, directives):
            if getattr(config, "cmd_opts", None) and getattr(config.cmd_opts, "autogenerate", False):
                script = directives[0]
                if script.upgrade_ops.is_empty():
                    directives[:] = []
                    logger.info("No changes in schema detected.")

        conf_args = current_app.extensions["migrate"].configure_args
        if conf_args.get("process_revision_directives") is None:
            conf_args["process_revision_directives"] = process_revision_directives

        connectable = get_engine()
        
        with connectable.connect() as connection:
            context.configure(connection=connection, target_metadata=get_metadata(), **conf_args)

            with context.begin_transaction():
                context.run_migrations()

# Determine the migration mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
