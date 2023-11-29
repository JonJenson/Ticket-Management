import random
import string
import pytz
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth import get_user_model
from .form import CreateTicketForm , AssignTicketForm
from . models import Ticket
from .form import AssignTicketForm

User = get_user_model()


def create_ticket(request):
    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.customer = request.user
            var.created_on = timezone.now()  # Set created_on with the current time in UTC
            var.save()

            # Convert created_on to local time in India
            if var.created_on:
                var.created_on = var.created_on.astimezone(pytz.timezone('Asia/Kolkata'))
            while not var.ticket_id:
                id =''.join(random.choices(string.digits, k=6))
                try:
                    var.ticket_id = id
                    var.save()
                    # email
                    subject = f'{var.ticket_title} # {var.ticket_id}'
                    message = 'Thank you  for crearting a ticket . A support engineer will be assigned soon'
                    email_from = 'jonjensons.aiml2022@citchennai.net'
                    recipient_list= [request.user.email ,]
                    send_mail(subject , message , email_from , recipient_list)
                    messages.success(request, 'Your ticket has been submitted. A Support Engineer would reach out soon.')
                    return redirect('customer-active-tickets')
                except IntegrityError:
                    continue
            
        else:
            messages.warning(request, 'Something went wrong. Please check form errors')
            return redirect('create-ticket')
    else:
        form = CreateTicketForm()
        context = {'form': form}
        return render(request, 'ticket/create_ticket.html', context)
    
#forcx viewing all active tickets
def customer_active_tickets(request):
    tickets = Ticket.objects.filter(customer = request.user , is_resolved = False).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request , 'ticket/customer_active_tickets.html' , context)

#for cx viewing all resolved tickets
def customer_resolved_tickets(request):
    tickets = Ticket.objects.filter(customer = request.user , is_resolved = True).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request , 'ticket/customer_resolved_tickets.html' , context)

#for engineer  viewing all his active tickets
def engineer_active_tickets(request):
    tickets = Ticket.objects.filter(engineer = request.user , is_resolved = False).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request , 'ticket/engineer_active_tickets.html' , context)

#for engineer viewing all his resolved tickets
def engineer_resolved_tickets(request):
    tickets = Ticket.objects.filter(engineer = request.user , is_resolved = True).order_by('-created_on')
    context = {'tickets':tickets}
    return render(request , 'ticket/engineer_resolved_tickets.html' , context)

#assign tickets to engineers
def assign_ticket(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id)

    if request.method == 'POST':
        form = AssignTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            # Save the form to update the fields in the Ticket model
            ticket = form.save(commit=False)
            
            # Update additional fields
            ticket.is_assigned_to_engineer = True
            ticket.status = 'Active'

            # Save the updated ticket
            ticket.save()

            messages.success(request, f'Ticket has been assigned to {ticket.engineer}')
            return redirect('ticket-queue')
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect('assign-ticket')  # Check this out later
    
    else:
        form = AssignTicketForm(instance=ticket)
        form.fields['engineer'].queryset = User.objects.filter(is_engineer=True)
        context = {'form': form, 'ticket': ticket}
        return render(request, 'ticket/assign_ticket.html', context)

# ticket details
def ticket_details(request, ticket_id):
    ticket = Ticket.objects.get(ticket_id=ticket_id) 
    context = {'ticket': ticket}
    return render(request, 'ticket/ticket_details.html', context)

# ticket queue (for only admins)
def ticket_queue(request):
    tickets = Ticket.objects.filter(is_assigned_to_engineer=False) 
    context = {'tickets': tickets}
    return render(request, 'ticket/ticket_queue.html', context)

def resolve_ticket(request ,  ticket_id):
    ticket = Ticket.objects.get(ticket_id = ticket_id)
    
    if request.method == 'POST':
        rs = request.POST.get('rs')
        ticket.resolution_steps = rs
        ticket.is_resolved= True
        ticket.status = 'Resolved'
        ticket.save()
        messages.success(request , "Ticket is now resolved and closed")
        return redirect('dashboard')








