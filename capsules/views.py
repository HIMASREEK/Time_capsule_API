from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now, make_aware
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Capsule
from .serializers import CapsuleSerializer


# ===========================
# 🔹 API VIEWS
# ===========================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_capsule(request):
    serializer = CapsuleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_capsules(request):
    capsules = Capsule.objects.filter(user=request.user)
    serializer = CapsuleSerializer(capsules, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def open_capsule(request, id):
    capsule = get_object_or_404(Capsule, id=id, user=request.user)

    if capsule.unlock_date > now():
        return Response({"message": "This capsule is locked 🔒"})

    capsule.is_opened = True
    capsule.save()

    return Response({
        "title": capsule.title,
        "message": capsule.message
    })


# ===========================
# 🔹 FRONTEND VIEWS
# ===========================

@login_required
def dashboard(request):
    capsules = Capsule.objects.filter(user=request.user)

    for c in capsules:

        # 📧 Send Email when unlocked
        if c.unlock_date <= now() and not c.is_opened:
            try:
                send_mail(
                    subject='Your Capsule is Unlocked! 🎉',
                    message=f'Your capsule "{c.title}" is now available.',
                    from_email='your_email@gmail.com',
                    recipient_list=[request.user.email or 'your_email@gmail.com'],
                    fail_silently=True
                )
            except Exception as e:
                print("Email error:", e)

            c.is_opened = True
            c.save()

        # 🔒 UI flag
        c.is_locked = c.unlock_date > now()

    return render(request, 'dashboard.html', {'capsules': capsules})


@login_required
def create_capsule_page(request):
    if request.method == 'POST':

        unlock_str = request.POST['unlock_date']
        unlock_dt = datetime.strptime(unlock_str, "%Y-%m-%dT%H:%M")
        unlock_dt = make_aware(unlock_dt)

        Capsule.objects.create(
            user=request.user,
            title=request.POST['title'],
            message=request.POST['message'],
            unlock_date=unlock_dt,
            image=request.FILES.get('image')
        )

        return redirect('dashboard')

    return render(request, 'create.html')


@login_required
def delete_capsule(request, id):
    capsule = get_object_or_404(Capsule, id=id, user=request.user)
    capsule.delete()
    return redirect('dashboard')


@login_required
def edit_capsule(request, id):
    capsule = get_object_or_404(Capsule, id=id, user=request.user)

    if request.method == 'POST':
        capsule.title = request.POST['title']
        capsule.message = request.POST['message']
        capsule.save()
        return redirect('dashboard')

    return render(request, 'edit.html', {'capsule': capsule})


# ===========================
# 🔗 SHARE VIEW (PUBLIC)
# ===========================
from django.utils.timezone import now

def share_capsule(request, token):
    capsule = get_object_or_404(Capsule, share_token=token)

    return render(request, 'shared_view.html', {
        'capsule': capsule,
        'now': now()   # 👈 IMPORTANT
    })