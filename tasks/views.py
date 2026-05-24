from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm, UserForm, UserEditForm

def root_redirect(request):
    """Redirect root path to dashboard if authenticated, else to login."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to ensure only staff/superusers (Admin role) can access views."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff
    
    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        if self.request.user.is_authenticated:
            return redirect('dashboard')
        return redirect('login')


class DashboardView(LoginRequiredMixin, View):
    """The main Dashboard homepage rendering the Kanban Board layout with filter selectors."""
    def get(self, request):
        queryset = Task.objects.all().select_related('assigned_to', 'created_by')
        
        # 1. Search Query (matches Task Name, Vendor/Source, Country, or Notes)
        q = request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(task_name__icontains=q) |
                Q(vendor_source__icontains=q) |
                Q(country__icontains=q) |
                Q(notes__icontains=q)
            )

        # 2. Filter by Assigned User (Username based)
        assigned_user = request.GET.get('assigned_to', '')
        if assigned_user:
            queryset = queryset.filter(assigned_to_id=assigned_user)

        # 3. Filter by Task Priority
        priority_val = request.GET.get('priority', '')
        if priority_val:
            queryset = queryset.filter(priority=priority_val)

        # Group tasks by board status columns
        board_columns = {status_val: [] for status_val, _ in Task.STATUS_CHOICES}
        for task in queryset:
            if task.status in board_columns:
                board_columns[task.status].append(task)

        # Construct board structure
        board_data = [
            {
                'value': status_val,
                'label': status_label,
                'tasks': board_columns[status_val]
            }
            for status_val, status_label in Task.STATUS_CHOICES
        ]

        # Get the predefined team users for the filter dropdown
        team_users = User.objects.filter(username__in=['hardik', 'aryan', 'harish', 'rasika']).order_by('username')

        context = {
            'board_data': board_data,
            'team_users': team_users,
            'priority_choices': Task.PRIORITY_CHOICES,
            'q': q,
            'selected_assignee': assigned_user,
            'selected_priority': priority_val,
        }
        return render(request, 'tasks/dashboard.html', context)


class TaskListView(LoginRequiredMixin, View):
    """List/Table view with switchable Board view for all tasks."""
    def get(self, request):
        queryset = Task.objects.all().select_related('assigned_to', 'created_by')
        
        q = request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(task_name__icontains=q) |
                Q(vendor_source__icontains=q) |
                Q(country__icontains=q) |
                Q(notes__icontains=q)
            )

        assigned_user = request.GET.get('assigned_to', '')
        if assigned_user:
            queryset = queryset.filter(assigned_to_id=assigned_user)

        priority_val = request.GET.get('priority', '')
        if priority_val:
            queryset = queryset.filter(priority=priority_val)

        status_val = request.GET.get('status', '')
        if status_val:
            queryset = queryset.filter(status=status_val)

        category_val = request.GET.get('category', '')
        if category_val:
            queryset = queryset.filter(category=category_val)

        country_val = request.GET.get('country', '')
        if country_val:
            queryset = queryset.filter(country=country_val)

        vendor_val = request.GET.get('vendor', '')
        if vendor_val:
            queryset = queryset.filter(vendor_source=vendor_val)

        # Sort
        sort_val = request.GET.get('sort', '-updated_at')
        allowed_sorts = ['-updated_at', 'task_name', 'status', 'priority', 'story_points', '-story_points']
        if sort_val in allowed_sorts:
            queryset = queryset.order_by(sort_val)

        # View mode
        view_type = request.GET.get('view', 'table')

        # Board data
        board_columns = {status_val_key: [] for status_val_key, _ in Task.STATUS_CHOICES}
        for task in queryset:
            if task.status in board_columns:
                board_columns[task.status].append(task)
        board_data = [
            {'value': sv, 'label': sl, 'tasks': board_columns[sv]}
            for sv, sl in Task.STATUS_CHOICES
        ]

        # Paginate results (table view)
        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
        total_filtered_count = queryset.count()
        paginator = Paginator(queryset, 15)
        page = request.GET.get('page', 1)
        try:
            tasks_page = paginator.page(page)
        except PageNotAnInteger:
            tasks_page = paginator.page(1)
        except EmptyPage:
            tasks_page = paginator.page(paginator.num_pages)

        # Dropdown data
        team_users = User.objects.filter(username__in=['hardik', 'aryan', 'harish', 'rasika']).order_by('username')
        countries = Task.objects.values_list('country', flat=True).distinct().order_by('country')
        vendors = Task.objects.values_list('vendor_source', flat=True).distinct().order_by('vendor_source')

        context = {
            'tasks_page': tasks_page,
            'board_data': board_data,
            'team_users': team_users,
            'users': team_users,
            'priority_choices': Task.PRIORITY_CHOICES,
            'status_choices': Task.STATUS_CHOICES,
            'category_choices': Task.CATEGORY_CHOICES,
            'countries': countries,
            'vendors': vendors,
            'q': q,
            'selected_assignee': assigned_user,
            'selected_priority': priority_val,
            'selected_status': status_val,
            'selected_category': category_val,
            'selected_country': country_val,
            'selected_vendor': vendor_val,
            'selected_sort': sort_val,
            'view_type': view_type,
            'total_count': total_filtered_count,
            'total_filtered_count': total_filtered_count,
        }
        return render(request, 'tasks/task_list.html', context)


class TaskDetailView(LoginRequiredMixin, View):
    """Render task detail attributes with workflow status pipeline."""
    def get(self, request, pk):
        task = get_object_or_404(Task.objects.select_related('assigned_to', 'created_by'), pk=pk)
        
        # Calculate current step index for the pipeline visual
        status_order = [s[0] for s in Task.STATUS_CHOICES]
        current_step = status_order.index(task.status) if task.status in status_order else 0
        
        context = {
            'task': task,
            'status_choices': Task.STATUS_CHOICES,
            'current_step': current_step,
        }
        return render(request, 'tasks/task_detail.html', context)


class TaskCreateView(AdminRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Create New Task"
        context['action_label'] = "Create Task"
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f"Task '{form.instance.task_name}' created successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.object.pk})


class TaskUpdateView(AdminRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Edit Task: {self.object.task_name}"
        context['action_label'] = "Save Changes"
        return context

    def form_valid(self, form):
        messages.success(self.request, f"Task '{form.instance.task_name}' updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.object.pk})


class TaskDeleteView(AdminRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        messages.success(self.request, f"Task '{task.task_name}' deleted successfully.")
        return super().delete(request, *args, **kwargs)


class UserManagementView(AdminRequiredMixin, View):
    def get(self, request):
        users = User.objects.all().order_by('username')
        form = UserForm()
        context = {
            'users': users,
            'form': form,
        }
        return render(request, 'tasks/user_management.html', context)

    def post(self, request):
        users = User.objects.all().order_by('username')
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User account for '{user.username}' created successfully.")
            return redirect('user_management')
        
        context = {
            'users': users,
            'form': form,
        }
        return render(request, 'tasks/user_management.html', context)


class UserEditView(AdminRequiredMixin, View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserEditForm(instance=user)
        context = {
            'managed_user': user,
            'form': form,
        }
        return render(request, 'tasks/user_edit.html', context)

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User account '{user.username}' updated successfully.")
            return redirect('user_management')
        
        context = {
            'managed_user': user,
            'form': form,
        }
        return render(request, 'tasks/user_edit.html', context)
