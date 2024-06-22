import requests

def check_application_status(url):
    try:
        response = requests.get(url)
        status_code = response.status_code
        if 200 <= status_code < 300:
            return 'up'
        else:
            return 'down'
    except requests.exceptions.RequestException as e:
        print(f"Error checking application status: {e}")
        return 'down'

def main():
    application_url = 'http://your-application-url.com'  # Update with the actual application URL
    status = check_application_status(application_url)
    print(f"The application is {status}.")

if __name__ == "__main__":
    main()
