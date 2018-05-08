from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.render_to_response(context)


class SearchView(TemplateView):
    template_name = 'search.html'

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        if request.method == 'POST':
            phrases = request.POST.get('search').split(';')

        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class RankingView(TemplateView):
    template_name = 'ranking.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.render_to_response(context)


class LoginView(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.render_to_response(context)
