from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Member
import uuid
from datetime import datetime
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm

def member_card_template(request):
    """View to render the member card template."""
    try:
        # Get member ID from query parameters
        member_id = request.GET.get('id')
        if not member_id:
            return JsonResponse({
                'success': False,
                'message': 'Member ID tidak valid'
            })

        # Get member data
        member = Member.objects.get(id=member_id)
        
        # Render template with member data
        context = {
            'member': member,
            'member_name': member.name,
            'member_phone': member.phone,
            'member_id': str(member.id),
            'points': member.points or 0
        }
        return render(request, 'members/member_card_template.html', context)
        
    except Member.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Member tidak ditemukan'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        })

def member_search_page(request):
    """View for the member search page"""
    return render(request, 'members/search_member.html')

@require_http_methods(["GET"])
def member_search_api(request):
    """API endpoint for member search"""
    phone = request.GET.get('phone', '').strip()
    print(f"Search API called with phone: {phone}")  # Debug log
    
    try:
        member = Member.objects.filter(phone=phone).first()
        print(f"Search result: {member}")  # Debug log
        
        if member:
            # Pastikan semua data member terkirim dengan benar
            member_data = {
                'id': str(member.id),  # UUID harus dikonversi ke string
                'name': member.name,
                'phone': member.phone,
                'points': member.points or 0
            }
            print(f"Sending member data: {member_data}")  # Debug log
            
            return JsonResponse({
                'success': True,
                'member': member_data
            })
            
        return JsonResponse({
            'success': False,
            'status': 'not_found',
            'phone': phone,
            'message': f'Member dengan nomor {phone} tidak ditemukan'
        })
    except Exception as e:
        print(f"Error in search: {str(e)}")  # Debug log
        return JsonResponse({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        })

@csrf_exempt  # For testing only - in production use proper CSRF protection
@require_http_methods(["POST"])
def member_register_api(request):
    """API endpoint for member registration"""
    print("Register API called")  # Debug log
    
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        
        print(f"Registering member: {name} ({phone})")  # Debug log
        
        if not name or not phone:
            return JsonResponse({
                'success': False,
                'message': 'Nama dan nomor telepon harus diisi'
            })
            
        # Check if member exists
        existing_member = Member.objects.filter(phone=phone).first()
        if existing_member:
            return JsonResponse({
                'success': False,
                'message': 'Member dengan nomor telepon ini sudah terdaftar'
            })
            
        # Create new member
        member = Member.objects.create(
            name=name,
            phone=phone,
            points=0
        )
        
        print(f"Member created: {member.id}")  # Debug log
        
        return JsonResponse({
            'success': True,
            'message': 'Member berhasil didaftarkan',
            'member': {
                'id': str(member.id),
                'name': member.name,
                'phone': member.phone,
                'points': member.points
            }
        })
        
    except json.JSONDecodeError:
        print("Invalid JSON data")  # Debug log
        return JsonResponse({
            'success': False,
            'message': 'Format data tidak valid'
        })
    except Exception as e:
        print(f"Error in registration: {str(e)}")  # Debug log
        return JsonResponse({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        })

def debug_view(request):
    """Simple debug view to test if routing works"""
    return JsonResponse({
        'success': True,
        'message': 'Debug route berfungsi',
        'timestamp': str(datetime.now())
    })

def debug_search_page(request):
    """Halaman debug untuk tes pencarian"""
    return render(request, 'members/debug_search.html')

def test_api_page(request):
    """Halaman tes API untuk debugging"""
    return render(request, 'members/test_api.html')

def debug_form(request):
    """Halaman form debug untuk troubleshooting"""
    return render(request, 'members/debug_form.html')

def download_member_card(request, member_id):
    """Generate a member card PDF with simplified elegant design"""
    print(f"Generating streamlined member card for ID: {member_id}")
    
    try:
        member = Member.objects.get(id=member_id)
        
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.units import mm
        from reportlab.lib.colors import Color, HexColor
        from reportlab.lib.utils import ImageReader
        import qrcode
        from io import BytesIO
        
        # Set up PDF dimensions (credit card size)
        width, height = 85.6*mm, 53.98*mm
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=(width, height))
        
        # ===== SIMPLIFIED COLOR SCHEME =====
        # Clean, professional colors
        primary_color = HexColor('#1a237e')  # Deep indigo (main background)
        accent_color = HexColor('#42a5f5')   # Light blue (accents)
        dark_accent = HexColor('#0d47a1')    # Dark blue (details)
        
        # Simple clean background (single color with minimal decoration)
        c.setFillColor(primary_color)
        c.rect(0, 0, width, height, fill=1)
        
        # Add subtle top accent bar 
        c.setFillColor(dark_accent)
        c.rect(0, height-15*mm, width, 15*mm, fill=1)
        
        # Add minimal decorative element - just a single stripe on the left
        c.setFillColor(accent_color)
        c.rect(0, 0, 3*mm, height, fill=1)
        
        # ===== CARD HEADER =====
        # Brand logo area
        c.setFillColor(HexColor('#FFFFFF'))
        c.setFont("Helvetica-Bold", 16)
        c.drawString(8*mm, height-10*mm, "IQMart")
        
        # Member badge with clean styling
        c.setFillColor(accent_color)
        c.setFillAlpha(0.9)
        c.roundRect(width-25*mm, height-11*mm, 17*mm, 6*mm, 1.5*mm, fill=1)
        c.setFillAlpha(1)
        
        c.setFillColor(HexColor('#FFFFFF'))
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(width-16.5*mm, height-8*mm, "MEMBER CARD")
        
        # Simple divider line
        c.setStrokeColor(HexColor('#FFFFFF33'))
        c.setLineWidth(0.3)
        c.line(8*mm, height-16*mm, width-8*mm, height-16*mm)
        
        # ===== MEMBER INFORMATION SECTION =====
        # Name label
        c.setFillColor(accent_color)
        c.setFillAlpha(1)
        c.setFont("Helvetica", 6)
        c.drawString(8*mm, height-21*mm, "NAME")
        
        # Name value
        c.setFillColor(HexColor('#FFFFFF'))
        c.setFont("Helvetica-Bold", 11)
        name = member.name
        if len(name) > 20:
            name = name[:17] + "..."
        c.drawString(8*mm, height-25*mm, name)
        
        # Phone label
        c.setFillColor(accent_color)
        c.setFont("Helvetica", 6)
        c.drawString(8*mm, height-31*mm, "PHONE")
        
        # Phone value
        c.setFillColor(HexColor('#FFFFFF'))
        c.setFont("Helvetica", 9)
        c.drawString(8*mm, height-35*mm, member.phone)
        
        # ===== QR CODE SECTION =====
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=0,
        )
        qr.add_data(f"ID:{member.id}|PHONE:{member.phone}")
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        
        # Place QR code with simple white frame
        qr_width, qr_height = 16*mm, 16*mm
        qr_x = width-22*mm
        qr_y = height-37*mm
        
        # Clean white background for QR
        c.setFillColor(HexColor('#FFFFFF'))
        c.roundRect(qr_x-1*mm, qr_y-1*mm, qr_width+2*mm, qr_height+2*mm, 1*mm, fill=1)
        
        # Draw QR code
        c.drawImage(ImageReader(qr_buffer), qr_x, qr_y, width=qr_width, height=qr_height)
        
        # QR code caption
        c.setFillColor(accent_color)
        c.setFont("Helvetica", 5)
        c.drawCentredString(qr_x + (qr_width/2), qr_y-3*mm, "SCAN ME")
        
        # ===== CARD FOOTER =====
        # Clean footer
        c.setFillColor(dark_accent)
        c.rect(0, 0, width, 8*mm, fill=1)
        
        # Member ID with clean styling
        id_text = str(member.id)
        
        # ID label and value
        c.setFillColor(HexColor('#FFFFFF99'))
        c.setFont("Helvetica-Bold", 5)
        c.drawString(8*mm, 3*mm, "ID:")
        
        c.setFillColor(HexColor('#FFFFFF'))
        if len(id_text) > 15:
            c.setFont("Helvetica", 4)
        else:
            c.setFont("Helvetica", 5)
        c.drawString(12*mm, 3*mm, id_text)
        
        # Website
        c.setFillColor(HexColor('#FFFFFF'))
        c.setFont("Helvetica", 5)
        c.drawRightString(width-8*mm, 3*mm, "www.iqmart.id")
        
        # Issue date with clean placement
        if hasattr(member, 'created_at') and member.created_at:
            reg_date = member.created_at.strftime('%d/%m/%Y')
        else:
            reg_date = "N/A"
            
        c.setFillColor(HexColor('#FFFFFF99'))
        c.setFont("Helvetica", 5)
        c.drawString(8*mm, 10*mm, f"ISSUED: {reg_date}")
        
        # Validity with simpler styling
        c.setFillColor(HexColor('#FFFFFF'))
        c.setFont("Helvetica-Bold", 5)
        c.drawRightString(width-8*mm, 10*mm, "VALID PERMANENTLY")
        
        # Finish the PDF
        c.save()
        buffer.seek(0)
        
        return FileResponse(
            buffer,
            as_attachment=True,
            filename=f'member_card_{member.id}.pdf',
            content_type='application/pdf'
        )
        
    except Member.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'message': 'Member tidak ditemukan'
        })
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return JsonResponse({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        })
