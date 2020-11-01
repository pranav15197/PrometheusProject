from sqlalchemy import func, extract, desc
from models import Patient, Encounter, Procedure, Observation


DAY_MAP = {
    0.0: "Sunday",
    1.0: "Monday",
    2.0: "Tuesday",
    3.0: "Wednesday",
    4.0: "Thursday",
    5.0: "Friday",
    6.0: "Saturday",
}


def generate_data_size_report(session):
    print("---" * 10)
    # Now generating report

    print(f"{'Patients added':>20}", ":", session.query(Patient.id).count())
    print(f"{'Encounters added':>20}", ":", session.query(Encounter.id).count())
    print(f"{'Procedures added':>20}", ":", session.query(Procedure.id).count())
    print(f"{'Observations added':>20}", ":", session.query(Observation.id).count())


def generate_gender_report(session):
    print("---" * 10)
    print("Patients By Gender")
    print("")
    gender_groups = (
        session.query(Patient.gender, func.count(Patient.gender))
        .group_by(Patient.gender)
        .all()
    )
    for gender, count in gender_groups:
        print(f"{gender:>20} : {count}")


def generate_procedures_report(session):
    print("---" * 10)
    print("Top Procedures")
    print("")
    top_procedures = (
        session.query(
            Procedure.type_code, func.count(Procedure.type_code).label("count")
        )
        .group_by(Procedure.type_code)
        .order_by(desc("count"))
        .limit(10)
        .all()
    )

    print(f"{'type_code':>20} : {'count'}")
    for procedure_type_code, count in top_procedures:
        print(f"{procedure_type_code:>20} : {count}")


def generate_encounters_report(session):
    print("---" * 10)
    weekly_encounters = (
        session.query(
            extract("dow", Encounter.start_date).label("dow"),
            func.count(extract("dow", Encounter.start_date)).label("count"),
        )
        .group_by("dow")
        .order_by(desc("count"))
        .all()
    )
    print("Day with most encounters:", DAY_MAP[weekly_encounters[0][0]])
    print("Day with least encounters:", DAY_MAP[weekly_encounters[-1][0]])
    print("---" * 10)
