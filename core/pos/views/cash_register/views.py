import json
from datetime import datetime

from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DeleteView, CreateView

from core.pos.forms import CashRegisterForm, CashRegister
from core.security.mixins import GroupPermissionMixin


class CashRegisterListView(GroupPermissionMixin, TemplateView):
    template_name = 'cash_register/list.html'
    permission_required = 'view_cash_register'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in CashRegister.objects.all():
                    data.append(i.toJSON())
            elif action == 'finish_cash_register':
                cash_register = CashRegister.objects.get(id=request.POST['id'])
                cash_register.final_amount = cash_register.current_amount
                cash_register.closing_date = datetime.now()
                cash_register.active = False
                cash_register.save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cajas Registradoras'
        context['create_url'] = reverse_lazy('cash_register_create')
        return context


class CashRegisterCreateView(GroupPermissionMixin, CreateView):
    model = CashRegister
    template_name = 'cash_register/create.html'
    form_class = CashRegisterForm
    success_url = reverse_lazy('cash_register_list')
    permission_required = 'add_cash_register'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    cash_register = CashRegister()
                    cash_register.user = request.user
                    cash_register.initial_amount = float(request.POST['initial_amount'])
                    cash_register.save()
            elif action == 'validate_data':
                data = {'valid': True}
                user_id = request.POST['user']
                if len(user_id):
                    data['valid'] = not CashRegister.objects.filter(date_joined=datetime.now().date(), user_id=user_id).exclude(active=False).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Nuevo registro de una Caja'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class CashRegisterDeleteView(GroupPermissionMixin, DeleteView):
    model = CashRegister
    template_name = 'delete.html'
    success_url = reverse_lazy('cash_register_list')
    permission_required = 'delete_cash_register'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context
