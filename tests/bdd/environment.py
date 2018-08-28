from eventsourcing.application.sqlalchemy import SQLAlchemyInfrastructureFactory

from taxisystem import TaxiSystem


def before_all(context):
    context.system = TaxiSystem(
        infrastructure_class=SQLAlchemyInfrastructureFactory,
        setup_tables=True,
    )
    context.system.setup()


def after_all(context):
    context.system.close()
