from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta
from django.utils import timezone
from .models import WordQuery, Word, WordOccurence
import pytz


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.render_to_response(context)


# Number of days for which the word statistics are displayed 
PAST_DAYS = 15


class SearchView(LoginRequiredMixin, TemplateView):
    template_name = 'search.html'

    # TODO: Add 'ignore polish diacritics' checkbox functionality
    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        now = timezone.now()

        result_occurrences = [(i, []) for i in range(0, PAST_DAYS)]
        result_words = []
        words_not_in_system = set()

        if request.method == 'POST' and request.POST.get('search') is not None:
            words = request.POST.get('search').split(';')
            for i in range(len(words)):
                words[i] = words[i].strip()
            # TODO: Remove equivalent words if case insensitive checkbox is on
            words = set(words)  # removes duplicates, but does NOT preserve order
            words.discard('')

            for word in words:
                user_word, new = WordQuery.objects.get_or_create(client=user, time=now, word=word)
                user_word.save()

                if request.POST.get('case_ch'):
                    word_obj = Word.objects.filter(word__iexact=word)
                else:
                    word_obj = Word.objects.filter(word=word)

                if word_obj:
                    occurrences = [0 for _ in range(PAST_DAYS)]
                    word_occurrences = WordOccurence.objects.filter(word=word_obj[0])
                    for occ in word_occurrences:
                        comment = occ.comment
                        time_delta = now - comment.time
                        if 0 <= time_delta.days < PAST_DAYS:
                            occurrences[time_delta.days] += 1

                    result_words.append(word)
                    for day in range(0, PAST_DAYS):
                        result_occurrences[day][1].append(occurrences[day])
                else:
                    words_not_in_system.add(word)
                
        context['result_words'] = result_words
        context['result_occurrences'] = result_occurrences
        context['words_not_in_system'] = words_not_in_system
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
