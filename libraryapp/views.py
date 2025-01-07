from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from .models import Book, User, Chat, DeleteRequest, Feedback
from django.views.generic import ListView
from .forms import ChatForm, BookForm, UserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView, DetailView
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import itertools
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404


# ---------------------------------------------------------------------------------------------- #
def login_form(request):
    return render(request, 'bookstore/login.html')


def logoutView(request):
    logout(request)
    return redirect('home')


def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('dashboard')
            elif user.is_librarian:
                return redirect('librarian')
            else:
                return redirect('publisher')
        else:
            messages.info(request, "invalid username and password")
            return redirect('home')


def register_form(request):
    return render(request, 'bookstore/register.html')


def registerView(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password = make_password(password)
        a = User(username=username, email=email, password=password)
        a.save()
        messages.success(request, "account created successfully")
        return redirect('home')
    else:
        messages.error(request, "registration failed. try again")
        return redirect('regform')


def logout(request):
    auth.logout(request)
    return redirect('login')


# ---------------------------------------------------------------------------------------#
def publisher(request):
    return render(request, 'publisher/home.html')


def useraddbook_form(request):
    return render(request, 'publisher/add_book.html')


def request_form(request):
    return render(request, 'publisher/delete_request.html')


def feedback_form(request):
    return render(request, 'publisher/send_feedback.html')


def about(request):
    return render(request, 'publisher/about.html')


def delete_request(request):
    if request.method == 'POST':
        book_id = request.POST['delete_request']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username
        user_request = username + "  want book with id  " + book_id + " to be deleted"
        # requesting_time = timezone.now()
        a = DeleteRequest(delete_request=user_request)  # , requesting_time=requesting_time)
        a.save()
        messages.success(request, 'Request was sent')
        return redirect('request_form')
    else:
        messages.error(request, 'Request was not sent')
        return redirect('request_form')


def send_feedback(request):
    if request.method == 'POST':
        feedback = request.POST['feedback']
        current_user = request.user
        user_id = current_user.id
        username = current_user.username
        feedback = username + " " + "  - " + " " + feedback

        a = Feedback(feedback=feedback)
        a.save()
        messages.success(request, 'Request was sent')
        return redirect('feedback_form')
    else:
        messages.error(request, 'Request was not sent')
        return redirect('feedback_form')


def useraddbook(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        year = request.POST['year']
        publisher = request.POST['publisher']
        desc = request.POST['desc']
        cover = request.FILES.get('cover', None)
        pdf = request.FILES.get('pdf', None)
        # saving current authenticated user
        current_user = request.user
        user_id = current_user.id
        username = current_user.username

        a = Book(title=title, author=author, year=year, publisher=publisher, desc=desc, cover=cover, pdf=pdf,
                 uploaded_by=username, user_id=user_id)
        a.save()
        return redirect('publisher')
    else:
        messages.error(request, "book not uploaded successfully")
        return redirect('uabook_form')


class UCreateChat(LoginRequiredMixin, CreateView):
    form_class = ChatForm
    model = Chat
    template_name = 'publisher/chat_form.html'
    success_url = reverse_lazy('ulchat')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class UListChat(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'publisher/chat_list.html'

    def get_queryset(self):
        return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')


class PBookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'publisher/book_list.html'
    context_object_name = 'books'
    paginate_by = 6

    def get_queryset(self):
        return Book.objects.order_by('-id')


class displaybookview(ListView):
    model = Book
    template_name = 'publisher/display_book.html'
    context_object_name = 'books'

    # paginate_by = 6

    def get_queryset(self):
        return Book.objects.order_by('-id')


class UViewBook(LoginRequiredMixin, DetailView):
    model = Book
    template_name = "publisher/book_details.html"


# def usearch(request):
#     query = request.GET['query']
#     print(type(query))
#
#     # data = query.split()
#     data = query
#     print(len(data))
#     if (len(data) == 0):
#         return redirect('publisher')
#     else:
#         a = data
#
#         # Searching for It
#         qs5 = models.Book.objects.filter(id__iexact=a).distinct()
#         qs6 = models.Book.objects.filter(id__exact=a).distinct()
#
#         qs7 = models.Book.objects.all().filter(id__contains=a)
#         qs8 = models.Book.objects.select_related().filter(id__contains=a).distinct()
#         qs9 = models.Book.objects.filter(id__startswith=a).distinct()
#         qs10 = models.Book.objects.filter(id__endswith=a).distinct()
#         qs11 = models.Book.objects.filter(id__istartswith=a).distinct()
#         qs12 = models.Book.objects.all().filter(id__icontains=a)
#         qs13 = models.Book.objects.filter(id__iendswith=a).distinct()
#
#         files = itertools.chain(qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)
#
#         res = []
#         for i in files:
#             if i not in res:
#                 res.append(i)
#
#         # word variable will be shown in html when user click on search button
#         word = "Searched Result :"
#         print("Result")
#
#         print(res)
#         files = res
#
#         page = request.GET.get('page', 1)
#         paginator = Paginator(files, 10)
#         try:
#             files = paginator.page(page)
#         except PageNotAnInteger:
#             files = paginator.page(1)
#         except EmptyPage:
#             files = paginator.page(paginator.num_pages)
#
#         if files:
#             return render(request, 'publisher/result.html', {'files': files, 'word': word})
#         return render(request, 'publisher/result.html', {'files': files, 'word': word})


# ----------------------------------------------------------------------------------------------- #
def librarian(request):
    book = Book.objects.all().count()
    user = User.objects.all().count()
    context = {"book": book, "user": user}
    return render(request, 'librarian/home.html', context)


def laddbook_form(request):
    return render(request, 'librarian/addbook.html')


def laddbook(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        year = request.POST['year']
        publisher = request.POST['publisher']
        desc = request.POST['desc']
        cover = request.FILES.get('cover', None)
        pdf = request.FILES.get('pdf', None)
        # saving current authenticated user
        current_user = request.user
        user_id = current_user.id
        username = current_user.username

        a = Book(title=title, author=author, year=year, publisher=publisher, desc=desc, cover=cover, pdf=pdf,
                 uploaded_by=username, user_id=user_id)
        a.save()
        messages.success(request, "book uploaded successfully")
        return redirect('librarianbook')
    else:
        messages.error(request, "book not uploaded successfully")
        return redirect('librarianbook')


class LBookListView(ListView):
    model = Book
    template_name = 'librarian/book_list.html'
    context_object_name = 'books'
    paginate_by = 6

    def get_queryset(self):
        return Book.objects.order_by('-id')


class LDeleteRequest(ListView):
    model = DeleteRequest
    template_name = 'librarian/delete_request.html'
    context_object_name = 'feedbacks'
    paginate_by = 6

    def get_queryset(self):
        return DeleteRequest.objects.order_by('-id')


class LViewBook(LoginRequiredMixin, DetailView):
    model = Book
    template_name = "librarian/book_detail.html"


class LEditView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "librarian/edit_book.html"
    success_url = reverse_lazy('librarianbook')
    success_message = "data was Updated successfully"


class LDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = "librarian/confirm_delete.html"
    success_url = reverse_lazy('lmanagebook')
    success_message = "data was delete successfully"


class LManageBook(ListView):
    model = Book
    template_name = 'librarian/manage_books.html'
    context_object_name = 'books'
    paginate_by = 6

    def get_queryset(self):
        return Book.objects.order_by('-id')


class LCreateChat(LoginRequiredMixin, CreateView):
    form_class = ChatForm
    model = Chat
    template_name = 'librarian/chat_form.html'
    success_url = reverse_lazy('llchat')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class LListChat(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'librarian/chat_list.html'

    def get_queryset(self):
        return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')


# ----------------------------------------------------------------------------------------------- #

def dashboard(request):
    book = Book.objects.all().count()
    user = User.objects.all().count()
    context = {"book": book, "user": user}
    return render(request, 'dashboard/home.html', context)


class ACreateChat(LoginRequiredMixin, CreateView):
    form_class = ChatForm
    model = Chat
    template_name = 'dashboard/chat_form.html'
    success_url = reverse_lazy('llchat')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class AListChat(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'dashboard/chat_list.html'

    def get_queryset(self):
        return Chat.objects.filter(posted_at__lt=timezone.now()).order_by('posted_at')


def adminaddbook_form(request):
    return render(request, 'dashboard/addbook.html')


def adminaddbook(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        year = request.POST['year']
        publisher = request.POST['publisher']
        desc = request.POST['desc']
        cover = request.FILES.get('cover', None)
        pdf = request.FILES.get('pdf', None)
        # saving current authenticated user
        current_user = request.user
        user_id = current_user.id
        username = current_user.username

        a = Book(title=title, author=author, year=year, publisher=publisher, desc=desc, cover=cover, pdf=pdf,
                 uploaded_by=username, user_id=user_id)
        a.save()
        messages.success(request, "book uploaded successfully")
        return redirect('adminbook')
    else:
        messages.error(request, "book not uploaded successfully")
        return redirect('adminbook')


class ABookListView(ListView):
    model = Book
    template_name = 'dashboard/book_list.html'
    context_object_name = 'books'
    paginate_by = 6

    def get_queryset(self):
        return Book.objects.order_by('-id')


class AManageBook(ListView):
    model = Book
    template_name = 'dashboard/manage_books.html'
    context_object_name = 'books'
    paginate_by = 6

    def get_queryset(self):
        return Book.objects.order_by('-id')


class AViewBook(LoginRequiredMixin, DetailView):
    model = Book
    template_name = "dashboard/book_detail.html"


class AEditView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "dashboard/edit_book.html"
    success_url = reverse_lazy('adminbook')
    success_message = "data was Updated successfully"


class ADeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = "dashboard/confirm_delete.html"
    success_url = reverse_lazy('amanagebook')
    success_message = "data was delete successfully"


class ADeleteRequest(ListView):
    model = DeleteRequest
    template_name = 'dashboard/delete_request.html'
    context_object_name = 'feedbacks'
    paginate_by = 6

    def get_queryset(self):
        return DeleteRequest.objects.order_by('-id')


class AFeedback(ListView):
    model = Feedback
    template_name = 'dashboard/feedback.html'
    context_object_name = 'feedbacks'
    paginate_by = 6

    def get_queryset(self):
        return Feedback.objects.order_by('-id')


def create_user_form(request):
    choice = ['1', '0', 'Publisher', 'Admin', 'Librarian']
    choice = {'choice': choice}
    return render(request, 'dashboard/add_user.html', choice)


class ListUserView(generic.ListView):
    model = User
    template_name = 'dashboard/list_user.html'
    context_object_name = 'users'

    # paginate_by = 4

    def get_queryset(self):
        return User.objects.order_by('-id')


def create_user(request):
    choice = ['1', '0', 'Publisher', 'Admin', 'Librarian']
    choice = {'choice': choice}
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        userType = request.POST['userType']
        email = request.POST['email']
        password = request.POST['password']
        password = make_password(password)
        print("USER TYPE")
        print(userType)
        if userType == "Publisher":
            a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password,
                     is_publisher=True)
            a.save()
            messages.success(request, "Member was created successfully")
            return redirect('listuserview')
        elif userType == "Admin":
            a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password,
                     is_admin=True)
            a.save()
            messages.success(request, "Member was created successfully")
            return redirect('listuserview')
        elif userType == "Librarian":
            a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password,
                     is_admin=True)
            a.save()
            messages.success(request, "Member was created successfully")
            return redirect('listuserview')
        else:
            messages.success(request, "member was not created")
            return redirect('create_user_form')
    else:
        return redirect('create_user_form')


class AViewUser(LoginRequiredMixin, DetailView):
    model = User
    template_name = "dashboard/user_detail.html"


class AEditUser(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'dashboard/edit_user.html'
    success_url = reverse_lazy('listuserview')
    success_message = "Data successfully updated"


class ADeleteUser(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'dashboard/confirm_delete2.html'
    success_url = reverse_lazy('listuserview')
    success_message = "Data Successfully deleted"
