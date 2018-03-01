import os        

def generate_project_params(runlevel):
    
    params = {
        # used by custom knoweng endpoints
        'API_PREFIX': 'api/v2/',

        # maximum upload size in bytes
        'MAX_CONTENT_LENGTH': 250 * 1024 * 1024,

        # limits on jobs, files (TODO tie these to account types)
        'MAX_FILES_TOTAL_BYTES_PER_USER': 5 * 1024 * 1024 * 1024,
        'MAX_JOBS_TOTAL_PER_USER': 40,
        'MAX_JOBS_RUNNING_PER_USER': 5,
        
        # fill in the following configuration values to enable HubZero authentication
        'HUBZERO_APPLICATION_HOST': 'FIXME',
        'HUBZERO_DATABASE_HOST': 'FIXME',
        'HUBZERO_DATABASE_USERNAME': 'FIXME',
        'HUBZERO_DATABASE_PASSWORD': 'FIXME',
        'HUBZERO_DATABASE_NAME': 'FIXME'
    }
    return params

def generate_project_users(runlevel):
    # Expected encoding: 'fakeuser:GARBAGESECRET:False;fakeadmin:GARBAGESECRET:True'
    users_encoded = os.getenv('SEED_USERS', '')

    users = []
    origin = 'nest'
    if runlevel == 'production':
        return users
    elif users_encoded == '':
        return users
    else:
        try:
            users_str_arr = users_encoded.split(';')
            for user_str in users_str_arr:
                user_fields = user_str.split(':')
                user_name = "fakeuser"
                user_pass = "GARBAGESECRET"
                is_su = False
                if len(user_fields) == 0:
                   print('improperly encoded user_str... skipping: ' + user_str)
                   continue
                if len(user_fields) >= 1:
                   user_name = user_fields[0]
                if len(user_fields) >= 2:
                   user_pass = user_fields[1]
                if len(user_fields) >= 3:
                   if user_fields[2] == 'True':
                       is_su = True
                users.append({
                    'username': user_name,
                    'password': user_pass,
                    'given_name': 'Fake',
                    'family_name': "Admin" if is_su else "User",
                    'origin': origin,
                    'is_superuser': is_su
                })
        except ValueError:
            print('improperly encoded SEED_USERS: ' + users_encoded)
    return users
