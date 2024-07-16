from datetime import datetime
from django.shortcuts import render
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .models import Ticket, Train, Booking  
from .decorators import login_required, admin_required
from django.utils import timezone
from django.db.models import Sum  
import json

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            if not username or not password:
                return JsonResponse({'error': 'Missing username or password'}, status=400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({'message': 'User registered successfully'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful', 'token': request.session.session_key}, status=200)
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)


@csrf_exempt
@admin_required
def add_train(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            source = data.get('source')
            destination = data.get('destination')
            total_seats = data.get('total_seats')
            arrival_time = data.get('arrival_time')
            departure_time = data.get('departure_time')
            date = data.get('date')
            schedule = data.get('schedule')
            sections = data.get('sections')

            if not all([name, source, destination, total_seats, arrival_time, departure_time, date, schedule, sections]):
                return JsonResponse({'error': 'Missing fields'}, status=400)

            arrival_time_str = data.get('arrival_time')
            departure_time_str = data.get('departure_time')

            if arrival_time_str:
                data['arrival_time'] = datetime.strptime(arrival_time_str, '%H.%M').time()
            if departure_time_str:
                data['departure_time'] = datetime.strptime(departure_time_str, '%H.%M').time()

            train = Train.objects.create(
                name=name,
                source=source,
                destination=destination,
                total_seats=total_seats,
                arrival_time=arrival_time_str,
                departure_time=departure_time_str,
                date=date,
                schedule=schedule,
                sections=sections
            )

            return JsonResponse({'message': 'Train added successfully'}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        except ValueError as e:
            return JsonResponse({'error': f'Invalid datetime format: {str(e)}'}, status=400)
    
    return JsonResponse({'error': 'Invalid method'}, status=405)

@csrf_exempt
@login_required
def book_seat(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        train_id = data.get('train_id')
        section = data.get('section')
        seats = data.get('seats')
        
        if train_id and section and seats:
            try:
                train = Train.objects.get(id=train_id)
                
                if section not in train.sections:
                    return JsonResponse({'error': f'Section {section} does not exist for this train'}, status=400)
                
                booked_seats_in_section = Booking.objects.filter(train=train, section=section).aggregate(total_booked_seats=Sum('seats_booked'))['total_booked_seats']
                booked_seats_in_section = booked_seats_in_section if booked_seats_in_section else 0
                
                if booked_seats_in_section + int(seats) <= train.sections[section]:
                    with transaction.atomic():
                        remaining_seats = train.sections[section] - booked_seats_in_section
                        if remaining_seats > 0:
                            next_seat_number = train.sections[section] - remaining_seats + 1
                        else:
                            return JsonResponse({'error': f'No seats available in section {section}'}, status=400)

                        # Book the seat
                        booking = Booking(
                            user=user,
                            train=train,
                            section=section,
                            seats_booked=seats
                        )
                        booking.seat_number = next_seat_number
                        booking.save()

                        # Convert arrival_time and departure_time to datetime objects
                        arrival_time = datetime.combine(train.date, train.arrival_time)
                        departure_time = datetime.combine(train.date, train.departure_time)

                        # Save ticket details to Ticket model
                        ticket = Ticket(
                            train_name=train.name,
                            train_id=train.id,
                            section=booking.section,
                            seat_number=booking.seat_number,
                            train_arrival=arrival_time,
                            train_departure=departure_time,
                            booking_time=timezone.now(),
                            user=user,
                            status='Booked'
                        )
                        ticket.save()

                    # Return JSON response with success message and ticket details
                    ticket_data = {
                        'ticket_id': ticket.ticket_id,
                        'train_name': ticket.train_name,
                        'train_id': ticket.train_id,
                        'section': ticket.section,
                        'seat_number': ticket.seat_number,
                        'train_arrival': ticket.train_arrival.strftime('%Y-%m-%d %H:%M:%S'),
                        'train_departure': ticket.train_departure.strftime('%Y-%m-%d %H:%M:%S'),
                        'booking_time': ticket.booking_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'user': ticket.user.username,
                        'status': ticket.status
                    }
                    
                    return JsonResponse({'message': 'Seat booked successfully', 'ticket': ticket_data}, status=201)
                else:
                    return JsonResponse({'error': f'Not enough seats available in section {section}'}, status=400)
            
            except Train.DoesNotExist:
                return JsonResponse({'error': 'Train not found'}, status=404)
        
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
        
        return JsonResponse({'error': 'Missing fields'}, status=400)
    
    return JsonResponse({'error': 'Invalid method'}, status=405)

def get_seat_availability(request):
    if request.method == 'GET':
        source = request.GET.get('source')
        destination = request.GET.get('destination')
        
        if source and destination:
            trains = Train.objects.filter(source=source, destination=destination)
            
            response = []
            for train in trains:
                available_seats_per_section = {}
                
                for section_key, section_name in train.SECTION_CHOICES:
                    total_seats = train.sections.get(section_key, 0)
                    booked_seats = Booking.objects.filter(train=train, section=section_key).aggregate(total_booked_seats=Sum('seats_booked'))['total_booked_seats']
                    booked_seats = booked_seats if booked_seats else 0
                    available_seats = total_seats - booked_seats
                    available_seats_per_section[section_name] = available_seats
                
                total_booked_seats = Booking.objects.filter(train=train).aggregate(total_booked_seats=Sum('seats_booked'))['total_booked_seats']
                total_booked_seats = total_booked_seats if total_booked_seats else 0
                total_available_seats = train.total_seats - total_booked_seats
                
                response.append({
                    'train_id':train.id,
                    'train': train.name,
                    'source': train.source,
                    'destination': train.destination,
                    'total_seats': train.total_seats,
                    'available_seats': total_available_seats,
                    'available_seats_per_section': available_seats_per_section
                })
            
            return JsonResponse(response, safe=False, status=200)
        
        return JsonResponse({'error': 'Missing source or destination'}, status=400)
    
    return JsonResponse({'error': 'Invalid method'}, status=405)


@login_required
def get_booking_details(request):
    if request.method == 'GET':
        user = request.user  # Assuming user is authenticated
        
        # Fetch bookings for the current user
        bookings = Ticket.objects.filter(user=user)
        
        
        response = []
        for booking in bookings:
            ticket = {
                'ticket_id': booking.ticket_id,
                'train_name': booking.train_name,
                'train_id': booking.train_id,
                'section': booking.section,
                'seat_number': booking.seat_number,
                'train_arrival': booking.train_arrival.strftime('%Y-%m-%d %H:%M:%S'),
                'train_departure': booking.train_departure.strftime('%Y-%m-%d %H:%M:%S'),
                'booking_time': booking.booking_time.strftime('%Y-%m-%d %H:%M:%S'),
                'user': user.username,
                'status': booking.status
            }
            response.append(ticket)
        
        return JsonResponse(response, safe=False, status=200)
    
    return JsonResponse({'error': 'Invalid method'}, status=405)