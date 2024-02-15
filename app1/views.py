from django.shortcuts import render,redirect
from .models import Users,Books
from django.contrib import messages
import bcrypt

def registration(request):
    user_id = request.session.get('user_id')
    
    if user_id:
        return redirect('app1:home')
    
    return render(request, "registration.html") 


def register(request):
    if request.method == "POST":
        
        errors = Users.objects.validate(request.POST)
        
        # There is some errors
        if len(errors) > 0:
            for error in errors.values():
                messages.error(request, error)
            return redirect('app1:registration')
        
        first_name_form = request.POST['first_name']
        last_name_form = request.POST['last_name']
        email_form = request.POST['email']
        password_form = request.POST['password1']
        confirm_password_form = request.POST['password2']
        
        if password_form == confirm_password_form:
            hash_password = bcrypt.hashpw(password_form.encode(), bcrypt.gensalt()).decode()
            
            new_user =Users.objects.create(
                first_name=first_name_form,
                last_name = last_name_form,
                email=email_form,
                password=hash_password)
            
            
            request.session['user_id'] = new_user.id
            request.session['first_name'] = new_user.first_name

            return redirect('app1:home')

        # if password didn't match
        else:
            messages.error(request, 'Password not match.')
            return redirect('app1:registration')



def login(request):
    if request.method == "POST":
        email_form = request.POST['email']
        password_form = request.POST['password1']
        
        users = Users.objects.filter(email=email_form)
        
        if len(users) == 0:
            messages.error(request, "Email doesn't exist.")
            return redirect('app1:registration')
        
        if bcrypt.checkpw(password_form.encode(), users.first().password.encode()):
            request.session['user_id'] = users[0].id
            request.session['first_name'] = users[0].first_name

            
            return redirect('app1:home')
        # if password is wrong
        else:
            messages.error(request, 'Password not correct.')
            return redirect('app1:registration')



def logout(request):
    request.session.flush()
    return redirect('app1:registration')


def home(request):
    user_id = request.session.get('user_id')
    # if user not logged in
    if not user_id:
        return redirect('app1:registration')
    
    all_books = Books.objects.all().order_by('-updated_at')
    current_user = Users.objects.get(id=user_id)
    
    context = {
        'books' : all_books,
        'user': current_user
    }    
    return render(request, "home.html", context)


def add_book(request):
    errors = Books.objects.validate(request.POST)
    if len(errors) > 0:
            for error in errors.values():
              messages.error(request, error)      #هان كأنه عملنا كونتكس عشان يزهر في تمبلت 

            return redirect('app1:registration')
        
    title = request.POST['title']
    description = request.POST['description']



# for create new book  we  get the user first and do that:لازم اجيب اليوزر عشان اعمل كريات بووك 
    user_id = request.session['user_id']
    user = Users.objects.get(id=user_id)
    
    book = Books.objects.create(title=title, description=description, uploaded_by=user)
    
    # To add book to user favorite books
    user.favorite_books.add(book)
    return redirect('app1:home')


def book(request, pk):
    book_to_view = Books.objects.get(id=pk)
    current_user = Users.objects.get(id=request.session['user_id'])
    
    context = {
        'book': book_to_view,
        'user': current_user
    }
    
    if book_to_view.uploaded_by == current_user:
        return render(request, 'if_uploaded_by.html', context)

    return render(request, "if_not_uploaded_by.html", context)


def add_to_favorite(request, pk):
    user = Users.objects.get(id=request.session['user_id'])
    book = Books.objects.get(id=pk)
    user.favorite_books.add(book)
    return redirect('app1:home')


def remove_from_favorite(request, pk):
    user = Users.objects.get(id=request.session['user_id'])
    book = Books.objects.get(id=pk)
    user.favorite_books.remove(book)
    return redirect('app1:home')

def updated(request, pk):
    title = request.POST['title']
    description = request.POST['description']
    
    book = Books.objects.get(id=pk)
    
    book.title = title
    book.description = description
    book.save()
    return redirect('app1:home',)


def delete(request, pk):
    book = Books.objects.get(id=pk)
    book.delete()
    return redirect('app1:home')


