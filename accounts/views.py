from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from listings.models import Deposit

@login_required
def account_dashboard(request):
    # Pull only the deposits that the logged-in user paid for
    user_deposits = Deposit.objects.filter(user=request.user, paid=True)
    
    context = {
        'deposits': user_deposits
    }
    return render(request, 'account.html', context)
