from django.http import JsonResponse, HttpResponse
from .models import dev_data
from .serializer import Wallet_serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from playfab import PlayFabClientAPI, PlayFabSettings


"""Tron send and recive functions"""
from tronpy import Tron
from tronpy.keys import PrivateKey

# integers representing half & one Tron
HALF_TRON = 500000
ONE_TRON = 1000000

contract = dev_data.objects.all().values()
serializer = Wallet_serializers(contract,many = True)

PlayFabSettings.TitleId = contract[0]["TitleId"]

# your wallet information
WALLET_ADDRESS = contract[0]["wallet_address"]
PRIVATE_KEY = contract[0]["private_key"]

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
            client.trx.transfer(WALLET_ADDRESS, str(wallet), int(amount)*ONE_TRON)
            .memo("Transaction Description")
            .build()
            .inspect()
            .sign(priv_key)
            .broadcast()
        )
        # wait until the transaction is sent through and then return the details
        return txn.wait()

    # return the exception
    except Exception as ex:
        print(ex)
        return False

def buy_with_tron(amount, wallet,private_key):
    try:
        priv_key = PrivateKey(bytes.fromhex(private_key))

        # create transaction and broadcast it
        txn = (
            client.trx.transfer(wallet, str(WALLET_ADDRESS), int(amount)*ONE_TRON)
            .memo("Transaction Description")
            .build()
            .inspect()
            .sign(priv_key)
            .broadcast()
        )
        # wait until the transaction is sent through and then return the details
        return txn.wait()

    # return the exception
    except Exception as ex:
        print(ex)
        return False




def callback(success, failure):
    if success:
        print("Congratulations, you made your first successful API call!")
        return success
    else:
        print("Something went wrong with your first API call.  :(")
        if failure:
            print("Here's some debug information:")
            print(failure)


@api_view(["POST",])
def tron_balance(request):
    if request.method == "POST":
        tron = account_balance(request.data["public_key"])
        return JsonResponse({"data":[{"balance" : tron},{"result":1}]})


@api_view(["POST",])
def buying_crystals(request,format=None):

    def get_userdata_callback(success, failure):
        if success:
            print("Get UserData successful!")
            data = success["Data"]
            public_key = data["public_key"]['Value']
            private_key = data["private_key"]['Value']
            amount = request.data["amount"]
            balance = account_balance(public_key)

            request2 = {
                "Amount": float(amount),
                "VirtualCurrency": "CY"
            }

            if balance > float(amount) + 1:
                try:
                    amount = float(amount) + 1
                    amount = amount
                    result = buy_with_tron(amount, public_key, private_key)
                    if result != False:
                        PlayFabClientAPI.AddUserVirtualCurrency(request2, callback)
                except Exception as ex:
                    print("Error ", ex)
                    return ex
            return data
        else:
            print("Something went wrong with your first API call.  :(")
            if failure:
                print("Here's some debug information:")
                print(failure)

    if request.method == "POST":
        email = request.data["email_address"]
        password = request.data["password"]

        request_playfab = {
            "Email": email,
            "Password": password
        }

        request_userdata = {
            "Email": email,
            "Keys": ""
        }

        PlayFabClientAPI.LoginWithEmailAddress(request_playfab, callback)
        PlayFabClientAPI.GetUserData(request_userdata,get_userdata_callback)
        return Response(status=status.HTTP_200_OK)

@api_view(["POST",])
def selling_crystals(request,format=None):

    def get_userdata_callback(success, failure):
        if success:
            print("Get UserData successful!")
            data = success["Data"]
            public_key = data["public_key"]['Value']
            amount = request.data["amount"]

            request2 = {
                "Amount": float(amount),
                "VirtualCurrency": "CY"
            }

            try:
                amount = float(amount)
                result = sell_for_tron(amount, public_key)
                if result != False:
                    PlayFabClientAPI.SubtractUserVirtualCurrency(request2, callback)
            except Exception as ex:
                print("Error ", ex)
                return ex
            return data
        else:
            print("Something went wrong with your first API call.  :(")
            if failure:
                print("Here's some debug information:")
                print(failure)

    if request.method == "POST":
        email = request.data["email_address"]
        password = request.data["password"]

        request_playfab = {
            "Email": email,
            "Password": password
        }

        request_userdata = {
            "Email": email,
            "Keys": ""
        }

        PlayFabClientAPI.LoginWithEmailAddress(request_playfab, callback)

        balance = account_balance(WALLET_ADDRESS)
        if balance > 0:
            PlayFabClientAPI.GetUserData(request_userdata, get_userdata_callback)
        return Response(status=status.HTTP_200_OK)
