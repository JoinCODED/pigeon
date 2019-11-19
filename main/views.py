from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from main.models import Group,Recipient
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

def recipientsList(request,query):
    search = request.GET.get('search')
    group = Group.objects.filter(id=query)
    if not group.exists():
        group = Group.objects.first()
    else:
        group = group.first()
    if request.method == "POST":
        requestType = request.POST.get('type')
        if requestType == "add":
            recipientId = request.POST.get('recipient')
            recipient = Recipient.objects.get(id=recipientId)
            group.members.add(recipient)
        elif requestType == "delete":
            recipientId = request.POST.get('recipient')
            recipient = Recipient.objects.get(id=recipientId)
            group.members.remove(recipient)
    if search:
        queryset = Recipient.objects.filter(Q(name__contains=search) | Q(email__contains=search) | Q(number__contains=search))
    else:
        queryset = Recipient.objects.all()
    queryset.order_by('pk')
    paginator = Paginator(queryset, 25)
    page = request.GET.get('page')
    recipients = paginator.get_page(page)
    context = {
        'group': group,
        'recipients': recipients,
    }
    if search:
        context['search'] = search
    
    return render(request,'admin/recipients.html',context)

def distributor(request,query):
    group = Group.objects.filter(id=query)
    if not group.exists():
        return redirect('/')
    else:
        group = group.first()
    if request.method == "POST":
        requestType = request.POST.get('type')
        if requestType == "sms":
            message = request.POST.get('message')
            group.sms(message)
        elif requestType == "email":
            template = request.FILES['template']
            fs = FileSystemStorage()
            filename = fs.save(template.name, template)
            
            subject = request.POST.get('subject')
            group.email(subject,str(fs.path(filename)))
            fs.delete(filename)
    context = {
        'group': group,
    }
    
    return render(request,'admin/distributor.html',context)