from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta
from django.utils import timezone
from .models import WordQuery
import pytz


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.render_to_response(context)


class SearchView(LoginRequiredMixin, TemplateView):
    template_name = 'search.html'

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        now = timezone.now()

        if request.method == 'POST':
            words = request.POST.get('search').split(';')
            for word in words:
                user_word, new = WordQuery.objects.get_or_create(client=user, time=now, word=word)
                user_word.save()

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class PreviousView(LoginRequiredMixin, TemplateView):
    template_name = 'previous.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        now = timezone.now()
        words = WordQuery.objects.filter(client=user, time__range=[now - timedelta(days=7), now]).\
            order_by('-time').values('word')
        context = {'words': words}
        return self.render_to_response(context)


class SignUpView(TemplateView):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        context = {'form': form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        return self.render_to_response({'form': form})
