from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.shortcuts import redirect

class AlreadyLoggedInMixin(AccessMixin):
    redirect_url = 'mafar/dashboard/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        return super().dispatch(request, *args, **kwargs)

class MustBeLoggedIn(LoginRequiredMixin):
    login_url = '/'