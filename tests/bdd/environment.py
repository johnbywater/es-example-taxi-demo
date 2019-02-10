from eventsourcing.application.sqlalchemy import SQLAlchemyApplication
from eventsourcing.application.system import SingleThreadedRunner

from taxisystem import TaxiSystem


def before_all(context):
    context.system = TaxiSystem(
        infrastructure_class=SQLAlchemyApplication,
        setup_tables=True,
    )
    context.runner = SingleThreadedRunner(context.system)
    context.runner.start()


def after_all(context):
    context.runner.close()
