import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print("🧠 Debugging create_admin.py")
print("🚀 Script execution started")

try:
    print("🔍 Importing modules...")
    from models.models import db, User
    from app_config import app  # Import `app` from the new configuration file
    from werkzeug.security import generate_password_hash

    print("🔧 Entering app context...")
    with app.app_context():
        print("📦 Creating database tables...")
        db.create_all()

        print("🔍 Checking for existing admin user...")
        existing_admin = User.query.filter_by(role='Admin').first()
        if not existing_admin:
            print("🛠️ Creating new admin user...")
            user = User(
                username='admin',
                email='admin@hospital.com',
                password=generate_password_hash('admin123'),
                role='Admin'
            )
            db.session.add(user)
            db.session.commit()
            print('✅ Admin user created.')
        else:
            print('⚠️ Admin already exists.')
 
except Exception as e:
    print("❌ Error occurred:", e)
    import traceback
    traceback.print_exc()