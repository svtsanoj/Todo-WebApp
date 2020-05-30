from django.shortcuts import render, redirect
from .forms import TodoForm, MailTodoForm
from . models import Todo
from datetime import datetime
from django.core.mail import send_mail

from django.contrib import messages

# Create your views here.
def todo(request):
    if(not request.user.is_authenticated):
        return redirect("login")

    current_user = request.user

    if(request.method == 'POST'):
        form = TodoForm(request.POST)
        
        if(form.is_valid()):
            entered_todo = Todo(text=request.POST['text'], owner = request.user, priority=request.POST['priority'])  
            entered_todo.save()
            return redirect("todo")


    todo_list = list(Todo.objects.filter(owner=current_user).order_by('complete','priority')) 
    print(todo_list)
    listlen = len(todo_list)
    form = TodoForm()
    date = datetime.today()  

    context = {'todo_list': todo_list, 
               'form': form,
               'date': date,
               'current_user' : current_user 
               }

    return render(request, 'todo.html', context=context)


def completeTodoToggle(request, todo_id):
    todo = Todo.objects.get(pk=todo_id) 
    if(todo.complete):
        todo.complete = False
    else:
        todo.complete = True
        todo.save()
    return redirect('todo')

def deleteCompleted(request):
    todo_list = Todo.objects.filter(complete__exact=True)  
    if(len(todo_list) > 0):
        todo_list.delete()
    return redirect('todo')

def deleteAll(request):
    todo_list = Todo.objects.all() 
    if(len(todo_list) > 0):
        todo_list.delete()
    return redirect('todo')




def mailtodo(request):
    if(not request.user.is_authenticated):
         return redirect("login")

   
    if(request.method == 'POST'):
        form = MailTodoForm(request.POST)
        
        if(form.is_valid()):
            currentName = request.user.first_name
            currentEmail = request.user.email
            print(currentEmail)
            content = request.POST.get('content','')

            mailid = request.POST.get('mailid', currentEmail)

            mailtoself = request.POST.get('mailtoself')

            if(mailtoself):
                mailid=currentEmail
                print("mailtoself true")
            print(mailid)
            
            mailcontent = currentName+"'s Tasks!\n\n"
            todo_list = Todo.objects.filter(owner=request.user).order_by('complete')
            if(len(todo_list)>0):
                for todo in todo_list:
                    checkcomplete = todo.complete
                    if(checkcomplete):
                        status = "Completed"
                    else:
                        status = "Incomplete"
                    prioritymap = { 0: "High Priority",
                                    1: "Moderate Priority",
                                    2: "Low Priority",}
                    
                    
                    mailcontent += todo.text + "\t" + status + "\t" + prioritymap[todo.priority] + "\n"
            
            content = content + "\n\n" +mailcontent
            title = currentName+"'s Todo List"
            send_mail(
                title,
                content,
                'sanojdjango@gmail.com',
                [mailid],
                fail_silently=True,
            )
            return redirect('mailtodo')

    form = MailTodoForm()

    contents = {'current_user': request.user,
                'form': form}
    return render(request, 'mailtodo.html', contents)
