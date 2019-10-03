from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Cause,Donation
from .forms import CauseDonateForm,CauseByBudgetForm

# Create your views here.

class CauseListView(ListView):
    model = Cause
    context_object_name = 'causes'
    template_name = 'causes.html'
    ordering = ['-date_posted']
    paginate_by = 3




class CauseDetailView(DetailView):
    model = Cause
    template_name = 'cause_detail.html'


class CauseCreateView(LoginRequiredMixin, CreateView):
    model = Cause
    template_name = 'cause_create.html'
    fields = ['title', 'description', 'catagory', 'goal', 'area', 'thumbnail']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CauseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Cause
    template_name = 'cause_create.html'
    fields = ['title', 'description', 'catagory','area', 'thumbnail']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        Cause = self.get_object()
        if self.request.user == Cause.author:
            return True
        return False


class CauseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cause
    template_name = 'cause_confirm_delete.html'
    success_url = '/causes'
    def test_func(self):
        Cause = self.get_object()
        if self.request.user == Cause.author:
            return True
        return False


@login_required
def causeDonate(request,pk):
    cause = Cause.objects.get(id=pk)
    if request.method == 'POST':
        form = CauseDonateForm(request.POST,instance=request.user)
        form.instance.donatorID = request.user
        if form.is_valid():
            cause.raised += form.cleaned_data['donate_amount']
            donation_object = Donation(donatorID=request.user,first_name=form.cleaned_data['first_name'],last_name=form.cleaned_data['last_name'],email=form.cleaned_data['email'],phone_number=form.cleaned_data['phone_number'],donate_amount=form.cleaned_data['donate_amount'])
            form.save() 
            cause.save()
            donation_object.save()
            cause.donation.add(donation_object)
            
            messages.success(request, f'Your account has been updated!')
            return redirect('cause-list')
    
    else:
        form = CauseDonateForm(instance=request.user)
        form.instance.donatorID = request.user
    context = {
                'form': form,
                'cause': cause
              }
    return render(request,'cause_donate.html',context)


def causeByBudget(request):
    causes = Cause.objects.all()
    paginate_by = 3
    if request.method == 'POST':
        maxBudget = request.POST.get('maxBudget')
        minBudget = request.POST.get('minBudget')
        requestedCause = []
        for cause in causes:
            if cause.goal >= int(minBudget) and cause.goal <= int(maxBudget):
                requestedCause.append(cause)
            causes = [cause for cause in requestedCause]
        # return redirect('cause-list')

    context = {
                'causes': causes
              }
    return render(request,'causes.html',context)