"""Seed the database with initial data matching the original static site."""
from app import create_app, db
from app.models import User, Project, Service, TeamMember, SiteSetting

app = create_app()

with app.app_context():
    db.create_all()

    if User.query.count() == 0:
        admin = User(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        print('Admin user created: admin / admin123')

    if Service.query.count() == 0:
        services = [
            Service(title='Residential', description='Custom homes and residential complexes, engineered for comfort and built to last generations.', icon_name='building', order=1),
            Service(title='Commercial', description='Offices, retail, and mixed-use developments delivered on schedule and within budget.', icon_name='office', order=2),
            Service(title='Industrial', description='Warehouses and industrial facilities built for load, durability, and long-term operation.', icon_name='industry', order=3),
            Service(title='Structural Engineering', description='Load analysis, foundation design, and structural certification for new and existing builds.', icon_name='structure', order=4),
            Service(title='Renovation', description='Structural upgrades, extensions, and interior overhauls for buildings of any age.', icon_name='renovation', order=5),
            Service(title='Project Management', description='Single point of accountability across timeline, budget, contractors, and inspections.', icon_name='management', order=6),
        ]
        db.session.add_all(services)
        print('Services seeded.')

    if Project.query.count() == 0:
        projects = [
            Project(title='Hillside Villa', category='residential', year='2024', description='A premium hillside residential project.', order=1),
            Project(title='Orion Business Park', category='commercial', year='2023', description='Modern commercial business park.', order=2),
            Project(title='Northgate Warehouse', category='industrial', year='2023', description='Large-scale industrial warehouse facility.', order=3),
            Project(title='Maple Court Homes', category='residential', year='2022', description='Residential complex with modern amenities.', order=4),
            Project(title='Civic Center Annex', category='commercial', year='2022', description='Government civic center expansion.', order=5),
            Project(title='Riverline Plant', category='industrial', year='2021', description='Industrial processing plant.', order=6),
        ]
        db.session.add_all(projects)
        print('Projects seeded.')

    if TeamMember.query.count() == 0:
        members = [
            TeamMember(
                name='Lead Engineer',
                title='B.E. Civil \u00b7 Structural Lead',
                bio='Over a decade in structural design and site execution, specializing in load-bearing analysis, seismic-resilient design, and construction quality assurance for mid-to-large scale builds.',
                credentials='B.E. in Civil Engineering\nLicensed Structural Engineer\nCertified Site Safety Officer\n12+ Years Field Experience',
                license_no='PLACEHOLDER',
                experience='12 Years',
                registered_in='Karnataka, IN',
                is_lead=True,
                order=1
            ),
        ]
        db.session.add_all(members)
        print('Team members seeded.')

    if SiteSetting.query.count() == 0:
        settings = [
            SiteSetting(key='site_name', value='Rudraksh Construction Co.'),
            SiteSetting(key='site_email', value='contact@rudrakshconstructions.tech'),
            SiteSetting(key='site_phone', value='+91 00000 00000'),
            SiteSetting(key='site_address', value='Placeholder Address, Belgavi, Karnataka, IN'),
            SiteSetting(key='site_hours', value='Mon \u2013 Sat, 9:00 AM \u2013 6:00 PM'),
        ]
        db.session.add_all(settings)
        print('Site settings seeded.')

    db.session.commit()
    print('Database seeded successfully!')
