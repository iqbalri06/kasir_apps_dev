from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm, inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
import locale
from decimal import Decimal
from datetime import datetime
import base64
from django.conf import settings

locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

def get_qris_image_base64():
    qris_path = settings.BASE_DIR / 'simple_shop' / 'images' / 'qris.png'
    try:
        with open(qris_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except:
        return ''

def generate_receipt_pdf(sale):
    # Set page size to 80mm (standard receipt width)
    page_width = 80 * mm
    page_height = 297 * mm  # A4 height
    page_size = (page_width, page_height)
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=page_size,
        rightMargin=5*mm,
        leftMargin=5*mm,
        topMargin=5*mm,
        bottomMargin=5*mm
    )

    # Create custom styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='ReceiptHeader',  # Changed from 'Header'
        fontName='Helvetica-Bold',
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=2*mm
    ))
    styles.add(ParagraphStyle(
        name='ReceiptSubHeader',  # Changed from 'SubHeader'
        fontName='Helvetica',
        fontSize=8,
        alignment=TA_CENTER,
        spaceAfter=1*mm
    ))
    styles.add(ParagraphStyle(
        name='ReceiptText',  # Changed from 'Normal'
        fontName='Helvetica',
        fontSize=8,
        alignment=TA_LEFT,
        leading=10
    ))
    styles.add(ParagraphStyle(
        name='ReceiptSmall',  # Changed from 'Small'
        fontName='Helvetica',
        fontSize=7,
        alignment=TA_CENTER,
        spaceAfter=1*mm
    ))

    elements = []

    # Header
    elements.append(Paragraph("IQMart", styles['ReceiptHeader']))
    elements.append(Paragraph("Jalan Raya No. 123, Jakarta", styles['ReceiptSubHeader']))
    elements.append(Paragraph("Telp: (021) 123-4567", styles['ReceiptSubHeader']))
    elements.append(Spacer(1, 3*mm))

    # Add horizontal line
    elements.append(Table([['']], colWidths=[70*mm], style=TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 0.5, colors.black),
    ])))
    elements.append(Spacer(1, 2*mm))

    # Transaction info in table format
    trans_data = [
        ['No. Transaksi:', sale.transaction_number],
        ['Tanggal:', sale.created_at.strftime('%d/%m/%Y %H:%M')],
        ['Kasir:', sale.user.get_full_name() or sale.user.username]
    ]
    trans_table = Table(trans_data, colWidths=[20*mm, 45*mm])
    trans_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
    ]))
    elements.append(trans_table)

    # Member info if exists
    if sale.member:
        elements.append(Spacer(1, 2*mm))
        member_data = [
            ['Member Info:', ''],
            ['Nama:', sale.member.name],
            ['No. HP:', sale.member.phone],
            ['Poin:', str(sale.member.points)]
        ]
        member_table = Table(member_data, colWidths=[20*mm, 45*mm])
        member_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('ALIGN', (0,0), (0,-1), 'LEFT'),
            ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ]))
        elements.append(member_table)

    elements.append(Spacer(1, 3*mm))

    # Items table
    table_data = [['Item', 'Qty', 'Harga', 'Total']]
    col_widths = [25*mm, 10*mm, 17*mm, 18*mm]
    
    for detail in sale.details.all():
        table_data.append([
            Paragraph(detail.product.name, styles['ReceiptSmall']),
            str(detail.quantity),
            f"Rp{detail.price:,.0f}".replace(',', '.'),
            f"Rp{detail.subtotal:,.0f}".replace(',', '.')
        ])

    # Subtotal and discounts
    elements.append(Spacer(1, 2*mm))
    items_table = Table(table_data, colWidths=col_widths)
    items_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('LINEABOVE', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 0.5, colors.black),
    ]))
    elements.append(items_table)

    # Totals and payment details
    total_data = []
    if sale.discount_amount > 0:
        total_data.extend([
            ['Subtotal:', '', '', f"Rp{(sale.total_price + sale.discount_amount):,.0f}".replace(',', '.')],
            ['Diskon Poin:', '', '', f"-Rp{sale.discount_amount:,.0f}".replace(',', '.')],
        ])
    total_data.append(['Total:', '', '', f"Rp{sale.total_price:,.0f}".replace(',', '.')])
    
    # Add cash payment details if payment method is cash
    if sale.payment.method.lower() == 'cash' and sale.payment_details:
        cash_amount = float(sale.payment_details.get('cash_amount', 0))
        change_amount = cash_amount - float(sale.total_price)
        total_data.extend([
            ['Tunai:', '', '', f"Rp{cash_amount:,.0f}".replace(',', '.')],
            ['Kembalian:', '', '', f"Rp{change_amount:,.0f}".replace(',', '.')]
        ])

    total_table = Table(total_data, colWidths=col_widths)
    total_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('ALIGN', (-1,0), (-1,-1), 'RIGHT'),
    ]))
    elements.append(total_table)

    # Points info
    if sale.member:
        elements.append(Spacer(1, 2*mm))
        points_data = []
        if sale.points_earned > 0:
            points_data.append(['Poin Didapat:', f"+{sale.points_earned}"])
        if sale.points_used > 0:
            points_data.append(['Poin Digunakan:', f"-{sale.points_used}"])
        if points_data:
            points_table = Table(points_data, colWidths=[20*mm, 45*mm])
            points_table.setStyle(TableStyle([
                ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 8),
                ('ALIGN', (0,0), (0,-1), 'LEFT'),
                ('ALIGN', (1,0), (1,-1), 'RIGHT'),
            ]))
            elements.append(points_table)

    # Footer
    elements.append(Spacer(1, 5*mm))
    elements.append(Paragraph("Terima kasih atas kunjungan Anda", styles['ReceiptSubHeader']))
    elements.append(Paragraph("Barang yang sudah dibeli tidak dapat dikembalikan", styles['ReceiptSmall']))

    doc.build(elements)
    buffer.seek(0)
    return buffer

