from django.shortcuts import render, redirect
import hashlib
import json
from web3 import Web3
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Evidence
from django.core.paginator import Paginator

with open("compiled_code.json") as f:
    compiled_sol = json.load(f)

abi = compiled_sol["contracts"]["TaskContract.sol"]["TaskContract"]["abi"]

with open("contract_address.txt") as f:
    contract_address = f.read().strip()

web3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER))
contract = web3.eth.contract(address=contract_address, abi=abi)

# Create your views here.
def userhome(request):
    user = request.user
    return render(request, 'User/userhome.html', {'user':user})

@login_required
def upload_evidence(request):
    user = request.user
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_data = uploaded_file.read()
        print("File size:", len(file_data))
        file_hash = hashlib.sha256(file_data).hexdigest()
        uploaded_file.seek(0) 
        tx_hash = contract.functions.storeEvidence(file_hash).transact({
            'from': web3.eth.accounts[1] 
        })
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        tx_id = tx_receipt.transactionHash.hex()

        Evidence.objects.create(
            user=user,
            session_id=request.session.session_key,
            file=uploaded_file,
            file_hash=file_hash,
            blockchain_tx=tx_id,
            status='Submitted',
        )

        messages.success(request, 'Evidence submitted and recorded on blockchain.')
        return redirect('my_evidences') 
    return render(request, 'User/upload.html')

@login_required
def my_evidences(request):
    user = request.user
    evidence_list = Evidence.objects.filter(user=user).order_by('-submitted_at')

    paginator = Paginator(evidence_list, 5)  # Show 5 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'User/my_evidences.html', {'page_obj': page_obj})