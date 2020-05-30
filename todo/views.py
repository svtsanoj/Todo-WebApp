from django.shortcuts import render, redirect
from .forms import TodoForm, MailTodoForm
from . models import Todo
from datetime import datetime
from django.core.mail import send_mail

from django.contrib import messages

# Create your views here.
def todo(request, todaylist='0'):
    
    if(not request.user.is_authenticated):
        return redirect("login")

    current_user = request.user

    if(request.method == 'POST'):
        form = TodoForm(request.POST)
        
        if(form.is_valid()):
            entered_todo = Todo(text=request.POST['text'], owner = request.user, priority=request.POST['priority'])  
            entered_todo.save()
            return redirect("todo")

    date = datetime.today().date() 
    todoList = list(Todo.objects.filter(owner=current_user).order_by('complete','priority'))
    for todo in todoList:
        if(todo.date < date):
            todo.current = False
        else:
            todo.current = True

    todoListCurrent = list(Todo.objects.filter(owner=current_user, current=True).order_by('complete','priority'))
    todoListBacklog = list(Todo.objects.filter(owner=current_user, current=False).order_by('complete','priority'))
    
    todoListShow = todoList

    if(todaylist=='1'):
        todoListShow = todoListCurrent
    if(todaylist=='2'):
        todoListShow = todoListBacklog

    form = TodoForm()
    
    context = {'todoList': todoListShow, 
               'form': form,
               'date': date,
               'current_user' : current_user 
               }

    return render(request, 'todo.html', context=context)


def todayListToggle(request, thistodaylist):
    return todo(request, thistodaylist)

def completeTodoToggle(request, todo_id):
    todo = Todo.objects.get(pk=todo_id)
    if(todo.complete):
        todo.complete = False
    else:
        todo.complete = True
    todo.save()
    return redirect('todo')

def deleteCompleted(request):
    todoList = Todo.objects.filter(complete__exact=True)  
    if(len(todoList) > 0):
        todoList.delete()
    return redirect('todo')

def deleteAll(request):
    todoList = Todo.objects.all() 
    if(len(todoList) > 0):
        todoList.delete()
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

            mailId = request.POST.get('mailid', currentEmail)

            mailToSelf = request.POST.get('mailtoself')

            if(mailToSelf):
                mailId=currentEmail
                print("mailtoself true")
            print(mailid)
            
            mailContent = currentName+"'s Tasks!\n\n"
            todoList = Todo.objects.filter(owner=request.user).order_by('complete')
            if(len(todoList)>0):
                for todo in todoList:
                    checkComplete = todo.complete
                    if(checkComplete):
                        status = "Completed"
                    else:
                        status = "Incomplete"
                    prioritymap = { 0: "High Priority",
                                    1: "Moderate Priority",
                                    2: "Low Priority",}
                    
                    
                    mailContent += todo.text + "\t" + status + "\t" + prioritymap[todo.priority] + "\n"
            
            content = content + "\n\n" +mailContent
            title = currentName+"'s Todo List"
            send_mail(
                title,
                content,
                'sanojdjango@gmail.com',
                [mailId],
                fail_silently=True,
            )
            return redirect('mailtodo')

    form = MailTodoForm()

    contents = {'current_user': request.user,
                'form': form}
    return render(request, 'mailtodo.html', contents)
