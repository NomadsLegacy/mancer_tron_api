from playfab import PlayFabClientAPI, PlayFabSettings

PlayFabSettings.TitleId = "D05EA"
email = "n3@m.com"
password = "123456"

request = {
    "Email": email,
    "Password": password
}


def callback(success, failure):
    if success:
        print("Congratulations, you made your first successful API call!")
        return success
    else:
        print("Something went wrong with your first API call.  :(")
        if failure:
            print("Here's some debug information:")
            print(failure)

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
            elif i == 4:
                username= pair[3]
        print(success)
    else:
        print("Something went wrong with your first API call.  :(")
        if failure:
            print("Here's some debug information:")
            print(failure.GenerateErrorReport())

request2 = {
    "Amount":20,
    "VirtualCurrency":"CY"
}

PlayFabClientAPI.LoginWithEmailAddress(request, callback)
PlayFabClientAPI.GetAccountInfo(request,callback2)
PlayFabClientAPI.AddUserVirtualCurrency(request2,callback)
PlayFabClientAPI.GetUserData(request2, callback)
