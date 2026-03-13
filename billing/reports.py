from datetime import datetime, timedelta
from typing import List, Dict
from uuid import UUID
import io

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from core.logging import setup_logging

logger = setup_logging()


class ReportGenerator:
    @staticmethod
    def generate_monthly_report(
        center_name: str,
        period_start: datetime,
        period_end: datetime,
        billing_events: List[Dict],
        total_amount: float
    ) -> bytes:
        buffer = io.BytesIO()
        
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        
        story = []
        
        title = Paragraph(
            f"Отчёт по подтверждениям записей",
            styles['Title']
        )
        story.append(title)
        story.append(Spacer(1, 1*cm))
        
        info = Paragraph(
            f"<b>Медицинский центр:</b> {center_name}<br/>"
            f"<b>Период:</b> {period_start.strftime('%d.%m.%Y')} - {period_end.strftime('%d.%m.%Y')}<br/>"
            f"<b>Всего подтверждений:</b> {len(billing_events)}<br/>"
            f"<b>Итоговая сумма:</b> {total_amount:.2f} руб.",
            styles['Normal']
        )
        story.append(info)
        story.append(Spacer(1, 2*cm))
        
        data = [['Дата', 'ID записи', 'Сумма (руб)']]
        
        for event in billing_events[:100]:
            data.append([
                event['billed_at'].strftime('%d.%m.%Y'),
                str(event['appointment_id'])[:8],
                f"{event['amount']:.2f}"
            ])
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        
        doc.build(story)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        logger.info(f"Generated PDF report: {len(billing_events)} events, {total_amount} RUB")
        
        return pdf_bytes
