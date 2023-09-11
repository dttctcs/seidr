from datetime import datetime, date

from app import app, db
from app.models import Asset, Unit, Application



user = app.appbuilder.sm.find_user(username="admin")
if not user:
    app.appbuilder.sm.add_user(
        username="admin",
        first_name="admin",
        last_name="admin",
        email="admin@for.bar",
        role=app.appbuilder.sm.find_role("Admin"),
        password="admin"
    )

db.create_all()

unit = Unit(name="unit")
for i in range(100):
    asset = Asset(name=f"asset&{i}", date_time=datetime.now(), date=date.today())
    if i % 10 == 0:
        unit = Unit(name=f"unit&{int(i / 10)}")
        db.session.add(unit)
    asset.owner = unit
    db.session.add(asset)
db.session.commit()

for i in range(10):
    application = Application(name=f"application_{i}", description=f'info_{i}')
    db.session.add(application)
db.session.commit()

assets = db.session.query(Asset).all()
applications = db.session.query(Application).all()

for i, application in enumerate(applications):
    for j in range(i * 5, (i + 1) * 5):  # Associate each asset with 5 applications
        asset = assets[j % len(assets)]
        asset.applications.append(application)

db.session.commit()

app.run(host="0.0.0.0", port=6060, debug=True)
