from django.http import JsonResponse
from .models import Wallet
from .serializer import Wallet_serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from playfab import PlayFabClientAPI, PlayFabSettings

PlayFabSettings.TitleId = "D05EA"



def callback(success, failure):
    if success:
        print("Congratulations, you made your first successful API call!")
        return success
    else:
        print("Something went wrong with your first API call.  :(")
        if failure:
            print("Here's some debug information:")
            print(failure)



@api_view(["GET","POST"])
def buying(request,format=None):

    if request.method == "GET":
        contract = Wallet.objects.all().values()
        serializer = Wallet_serializers(contract,many = True)
        return JsonResponse({"contract" : serializer.data})

    if request.method =="POST":
        serializer = Wallet_serializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status =status.HTTP_201_CREATED)
@api_view(["GET","PUT","DELETE"])
def contract_details(request,email,format=None):
    try:
        wallet = Wallet.objects.get(email_address = email)
        password = getattr(wallet, "password")
    except Wallet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_playfab = {
        "Email": email,
        "Password": password
    }

    #PlayFabClientAPI.GetAccountInfo(request_playfab, callback2)

    if request.method == "GET":
        serializer = Wallet_serializers(wallet)
        PlayFabClientAPI.LoginWithEmailAddress(request_playfab, callback)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = Wallet_serializers(wallet,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        wallet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def callback2(success, failure):
    if success:
        global username
        global address
        i=0
        def nested_dict_pairs_iterator(dict_obj):
            ''' This function accepts a nested dictionary as argument
                and iterate over all values of nested dictionaries
            '''
            # Iterate over all key-value pairs of dict argument
            for key, value in dict_obj.items():
                # Check if value is of dict type
                if isinstance(value, dict):
                    # If value is dict then iterate over all its values
                    for pair in nested_dict_pairs_iterator(value):
                        yield (key, *pair)
                else:
                    # If value is not dict type then yield the value
                    yield (key, value)

        # Loop through all key-value pairs of a nested dictionary
        for pair in nested_dict_pairs_iterator(success):
            i +=1
            if i==3:
                address= pair[2]
                print(address)
            elif i == 4:
                username= pair[3]
                print(username)
    else:
        print("Something went wrong with your first API call.  :(")
        if failure:
            print("Here's some debug information:")
            print(failure.GenerateErrorReport())

"""Tron send and recive functions"""
from tronpy import Tron
from tronpy.keys import PrivateKey

# integers representing half & one Tron
HALF_TRON = 500000
ONE_TRON = 1000000

# your wallet information
WALLET_ADDRESS = "TStntTFk5Ktn2ZdxRYAC2NDGvcVAd4Zfgx"
PRIVATE_KEY = "88aa0adceb2f843f96e17b0ea6b2d9aa93df475638a60fffb5449208b3cff81e"

# connect to the Tron blockchain
client = Tron(network='shasta')

def account_balance(address):
    balance = client.get_account_balance(str(address))
    return balance

# send some 'amount' of Tron to the 'wallet' address
def sell_for_tron(amount, wallet):
    try:
        priv_key = PrivateKey(bytes.fromhex(PRIVATE_KEY))

        # create transaction and broadcast it
        txn = (
            client.trx.transfer(WALLET_ADDRESS, str(wallet), int(amount))
            .memo("Transaction Description")
            .build()
            .inspect()
            .sign(priv_key)
            .broadcast()
        )
        # wait until the transaction is sent through and then return the details
        return txn.sign(priv_key).broadcast()

    # return the exception
    except Exception as ex:
        return ex

def buy_with_tron(amount, wallet,private_key):
    try:
        priv_key = PrivateKey(bytes.fromhex(private_key))

        # create transaction and broadcast it
        txn = (
            client.trx.transfer(wallet, str(WALLET_ADDRESS), int(amount))
            .memo("Transaction Description")
            .build()
            .inspect()
            .sign(priv_key)
            .broadcast()
        )
        # wait until the transaction is sent through and then return the details
        print(txn.sign(priv_key).broadcast())
        return txn.wait()

    # return the exception
    except Exception as ex:
        return ex

@api_view(["GET",])
def buying_crystals(request,email,format=None):
    try:
        wallet = Wallet.objects.get(email_address = email)
        password = getattr(wallet, "password")
        address = getattr(wallet,"wallet_address")
        private_key = getattr(wallet,"private_key")
        amount = getattr(wallet,"amount")
    except Wallet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    request2 = {
        "Amount": float(amount),
        "VirtualCurrency": "CY"
    }


    if request.method == "GET":
        serializer = Wallet_serializers(wallet)

        balance = account_balance(address)
        if balance > float(amount)+1:
            try:
                amount = float(amount)+1
                amount = amount*1000000
                buy_with_tron(amount,address,private_key)
            except Exception as ex:
                print("Error ", ex)
                return ex
            PlayFabClientAPI.AddUserVirtualCurrency(request2, callback)
        return Response(serializer.data)

@api_view(["GET",])
def selling_crystals(request,email,format=None):
    try:
        wallet = Wallet.objects.get(email_address = email)
        password = getattr(wallet, "password")
        adrress = getattr(wallet,"wallet_address")
        private_key = getattr(wallet,"private_key")
        amount = getattr(wallet,"amount")
    except Wallet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    request2 = {
        "Amount": float(amount),
        "VirtualCurrency": "CY"
    }


    if request.method == "GET":
        serializer = Wallet_serializers(wallet)

        balance = account_balance(WALLET_ADDRESS)
        if balance > 0:
            try:
                amount = float(amount)*1000000
                sell_for_tron(amount,adrress)
            except Exception as ex:
                print("Error ", ex)
                return ex
            PlayFabClientAPI.SubtractUserVirtualCurrency(request2, callback)
        return Response(serializer.data)
