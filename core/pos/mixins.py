from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from config import settings
from core.pos.models import CashRegister


class ValidateCashRegisterMixin(LoginRequiredMixin, object):
    success_url = settings.LOGIN_REDIRECT_URL

    def get(self, request, *args, **kwargs):
        if not CashRegister.objects.filter(user=request.user, date_joined=datetime.now().date()).exists():
            messages.error(request, 'No puedes realizar ninguna venta si no has abierto ninguna caja')
            return HttpResponseRedirect(self.success_url)
        return super().get(request, *args, **kwargs)
