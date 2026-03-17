from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from web3.exceptions import TransactionNotFound
from django.core.paginator import Paginator
from Users.models import Evidence
from web3 import Web3
from django.conf import settings
import json
import datetime

with open("compiled_code.json") as f:
    compiled_sol = json.load(f)

abi = compiled_sol["contracts"]["TaskContract.sol"]["TaskContract"]["abi"]

with open("contract_address.txt") as f:
    contract_address = f.read().strip()

web3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER))
contract = web3.eth.contract(address=contract_address, abi=abi)

def adminhome(request):
    users = User.objects.filter(is_staff=False, is_superuser=False) 
    return render(request, "Admin/adminhome.html", {"users": users})

def admin_update_userstatus(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        
        user.is_active = not user.is_active
        user.save()

        if user.is_active:
            messages.success(request, f"User {user.username} has been activated.")
        else:
            messages.success(request, f"User {user.username} has been deactivated.")
        
        return redirect('adminhome')  
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('adminhome')
    

@staff_member_required
def admin_all_evidence(request):
    evidence_list = Evidence.objects.all().order_by('-submitted_at')
    paginator = Paginator(evidence_list, 10)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin/admin_all_evidence.html', {
        'page_obj': page_obj
    })

@staff_member_required
@require_POST
def update_evidence_status(request, evidence_id):
    evidence = get_object_or_404(Evidence, id=evidence_id)
    new_status = request.POST.get('status')

    if new_status in ['Approved', 'Rejected']:
        evidence.status = new_status
        evidence.save()
        messages.success(request, f"Evidence #{evidence.id} marked as {new_status}.")
    else:
        messages.error(request, "Invalid status update.")

    return redirect('admin_all_evidence')


@staff_member_required
def verify_transaction(request):
    context = {}

    if request.method == 'POST':
        tx_hash = request.POST.get('tx_hash', '').strip()

        try:
            # Fetch transaction from local Ganache blockchain
            tx = web3.eth.get_transaction(tx_hash)
            tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
            block = web3.eth.get_block(tx_receipt['blockNumber'])

            context['transaction'] = {
                'hash': tx.hash.hex(),
                'from': tx['from'],
                'to': tx['to'],
                'blockNumber': tx_receipt['blockNumber'],
                'status': 'Success' if tx_receipt['status'] == 1 else 'Failed',
                'gasUsed': tx_receipt['gasUsed'],
                'timestamp': datetime.datetime.fromtimestamp(block['timestamp'])
            }

        except TransactionNotFound:
            context['error'] = "Transaction not found in your local Ganache blockchain."
        except Exception as e:
            context['error'] = f"Error: {str(e)}"

    return render(request, 'Admin/verify_transaction.html', context)
