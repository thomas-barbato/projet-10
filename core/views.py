from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    TemplateView,
    UpdateView,
)
from .models import (
    Users,
    Comments,
    Projects,
    Issues,
)

class JsonableResponseMixin:
    """
    Mixin to add JSON support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        """docstring"""
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        """docstring"""
        if self.request.is_ajax():
            data = {"message": "Successfully submitted form data."}
            return JsonResponse(data)
        return super().form_valid(form)


@method_decorator(csrf_exempt, name='dispatch')
class SignupView(FormView, JsonableResponseMixin, SuccessMessageMixin):

    def post(self, request, *args, **kwargs):
        response = request.AJAX
        return JsonResponse(response, status=200)