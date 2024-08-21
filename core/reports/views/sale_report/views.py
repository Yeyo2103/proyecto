import json

from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.views.generic import FormView

from core.pos.models import Sale
from core.reports.forms import ReportForm
from core.security.mixins import GroupModuleMixin


class SaleReportView(GroupModuleMixin, FormView):
    template_name = 'sale_report/report.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Sale.objects.filter()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
                total = float(queryset.aggregate(result=Coalesce(Sum('total'), 0.00, output_field=FloatField()))['result'])
                data.append({
                    'client': {'user': {'names': '---'}},
                    'date_joined': '---',
                    'payment_type': {'name': '---'},
                    'receipt': {'name': '---'},
                    'subtotal': '---',
                    'total_dscto': '---',
                    'total_iva': '---',
                    'total': total,
                })
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Ventas'
        return context
