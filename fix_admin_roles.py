import os
import django
import sys

# Siapkan lingkungan Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Impor model Role
from simple_shop.models import Role, User

def fix_admin_roles():
    print("Memeriksa dan memperbaiki role Admin...")
    
    # Periksa apakah ada duplikat role Admin
    admin_roles = Role.objects.filter(name='Admin')
    count = admin_roles.count()
    
    if count <= 1:
        print(f"Tidak ada duplikat. Ditemukan {count} role Admin.")
        return
    
    print(f"Ditemukan {count} role Admin. Memperbaiki...")
    
    # Ambil role Admin pertama untuk dipertahankan
    primary_role = admin_roles.first()
    print(f"Role Admin utama: ID={primary_role.id}")
    
    # Hapus role Admin lainnya, tapi pindahkan dulu semua pengguna ke role utama
    secondary_roles = admin_roles.exclude(id=primary_role.id)
    
    for role in secondary_roles:
        # Pindahkan semua pengguna dari role ini ke role utama
        affected_users = User.objects.filter(role=role)
        user_count = affected_users.count()
        
        if user_count > 0:
            print(f"Memindahkan {user_count} pengguna dari role ID={role.id} ke role ID={primary_role.id}")
            affected_users.update(role=primary_role)
        
        # Hapus role
        role_id = role.id
        role.delete()
        print(f"Menghapus role Admin duplikat dengan ID={role_id}")
    
    # Konfirmasi hasil
    final_count = Role.objects.filter(name='Admin').count()
    print(f"Selesai! Sekarang terdapat {final_count} role Admin.")

if __name__ == "__main__":
    fix_admin_roles()
    print("Proses selesai!")
