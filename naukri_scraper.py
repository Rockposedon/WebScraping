import requests

# Function to extract job details
def extract_job_details(data):
    job_details = []
    for job in data['jobDetails']:
        job_id = job.get('jobId', 'N/A')
        title = job.get('title', 'N/A')
        company_name = job.get('companyName', 'N/A')
        footer_label = job.get('footerPlaceholderLabel', 'N/A')
        tags_and_skills = job.get('tagsAndSkills', 'N/A')
        
        # Extract placeholders information
        placeholders = job.get('placeholders', [])
        experience = 'N/A'
        salary = 'N/A'
        location = 'N/A'
        for placeholder in placeholders:
            if placeholder['type'] == 'experience':
                experience = placeholder['label']
            elif placeholder['type'] == 'salary':
                salary = placeholder['label']
            elif placeholder['type'] == 'location':
                location = placeholder['label']
        
        job_description = job.get('jobDescription', 'N/A')
        
        job_details.append({
            'Job ID': job_id,
            'Job Title': title,
            'Company Name': company_name,
            'Footer Placeholder Label': footer_label,
            'Tags and Skills': tags_and_skills,
            'Experience': experience,
            'Salary': salary,
            'Location': location,
            'Job Description': job_description
        })
    return job_details

# Define the URL, headers, and common parameters
url = "https://www.naukri.com/jobapi/v3/search"

# why cookie is required 
# Define the session cookie for naukri.com.
# This cookie is essential for maintaining the session, user information, and necessary parameters for successful API requests.
# Note: Ensure compliance with naukri.com's terms of service and policies when using this cookie for web scraping.

headers = {
    'authority': 'www.naukri.com',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'appid': '109',
    'clientid': 'd3skt0p',
    'content-type': 'application/json',
    'cookie': '_t_s=direct; _t_ds=cdb1791699365060-40cdb179-0cdb179; _t_us=654A40C4; test=naukri.com; _t_s=direct; _t_r=1030%2F%2F; persona=default; _t_ds=cdb1791699365060-40cdb179-0cdb179; _abck=370FB7E71860E8432F0D794697C5C6B3~0~YAAQB8AsMQ4X3qiLAQAAvgkNqgpeyiX7uLHxTeXWohrol2EtEzNpPOIaEvv3JD+JdI3rS84j4nYDQKF7p0NIgpwBBGX5xAZ9AKzuTcc2Z40l4LOt7vnnBYFOtrQn0pckHV78IMGvznCh0ZHt8qIAa42FGEqRw6DmU4UUqwu9su3FZ1+6swkLeqDuEkwcZYA47+ELk//zE/uz2NI6DkcPeH3XiP1f/IqLv4csOtbRmjy3+z8VFGYXNtaz8ykorl1YNEthRa60UeBVhZt38BltTpCKZzkf8hMT1ROw18miALTF4c532sWrKLHA5jjrNDrxc7SuzYUmtr4GhPqXtD7SlUblveXo0lLp7PPj19rIQZeea5gGlUtKKD8YY3RNobitL59qU2nkhHELuYFVepx1ES2Ou1z71xM=~-1~||-1||~-1; bm_mi=FB878CE50EF5A9720F1237648310C5CE~YAAQZ0k0Fzq8hZWLAQAAwL26qhW7jpmEnSWtuU+8dq2TRcDJOaVFYUY0qF3S3MKQ9XDq3UO0tZ/OnmlspHISud8bSG56eQONrXPa3pRUU5trZ2UIoVIQrH13zZx//ZcWvpoowZbnqM9NH/Y4C0RCYzSBpjvqM7Jttvti+DZEgBa/fQuBeya0+qWtJq4PkUyWNDMzzzF9lLvBYNHjc3trUoEFvK6/LKmP/VSoLBhS4jggT2NRmzVf0ggbj3IWrC9Pv6Dj+1DeRhk1DItFrUXTpCnxucTUyA4PITGntGvjtZbi8J0tr7DTkZdqycmk/frzDKi26PL+IzCyhg==~1; bm_sv=B3140AAC7590D963EB7E7F19C5153313~YAAQZ0k0Fzu8hZWLAQAAwL26qhWmqot7f4DrMC+us1serQjW03izIns/MDZ4nZzHDxYUnaiF5iDHLhzg6KDat5PFr2hRGJtGR0sGlfucsAp/HAbebS8Busf3Z6VpXzGh6PmK3fasbAq3xJeoeB4LZVUfADa/P7P6glw0n7rWrgMaw9Fk4dZIs6LpojC+azGNJhJ5hcfmvGjiGBVUj23/T8VFP/JhcGtrAOEw0chdzC25P/DVaKD6Xyog3vYiDD55~1; ak_bmsc=2D0EBB2E423AA3278C56D270B2C5C295~000000000000000000000000000000~YAAQHNgsMWdFaJSLAQAArMPTqhVOCEe64z0wWGraX3eTSnlFHLMVjs6oXJh4gLbtKaLY9yeZUMJvYXmHyl7Nw9hDQflD6zF/8JlFDlg+F5EvE/i7QhrhrrP9xTnYp7ioNSEbOWgQxvdKw0SLmr+7g6fMY8HUoeMkX+pVWQAxXN6BpViuWy1O47RbXGBMaFRGwyQIPQaYGGbsdQU806Rwrsv3fOynicHY8ziKUCYFJbdMa3RnE5iZFXHaP7ma8eXQRn/ML2xAhRVRk+3n1yxWRp12gh6R0z2XTIOMwGBSCF2+SJkc92VpRwzuG+TiPFT5Ldm/i2sPNG6kBJ7Uhe63Rie5OoQO2cuFnbPvk1V8PinK+qwoDQfnMyUDIuZT461N5puOk353QtMeu/HPML+wgEr3h9R2NR+7oDWbH04ZiUfZ2sFmbSe8R8Cfply9ILRpMMX2haoIv8BHbKCmnBrVdGF4DCZYxZdeyduZ+YrSnilqWYqKItapXrX/AFQNVtfLE1UG5uxaB4Mi+SDTbwKYyXFe3M0SaHx/ML/WYc7KsjSA9q+/7WtxVflKQdH4TsA=',
    'gid': 'LOCATION,INDUSTRY,EDUCATION,FAREA_ROLE',
    'referer': 'https://www.naukri.com/developer-jobs-2?k=developer',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'systemid': 'Naukri',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}
params = {
    'noOfResults': '20',
    'urlType': 'search_by_keyword',
    'searchType': 'adv',
    'keyword': 'developer',
    'pageNo': '1',
    'sort': 'r',
    'k': 'developer',
    'seoKey': 'developer-jobs-2',
    'src': 'jobsearchDesk',
    'latLong': '',
    'sid': '16993781950467590',
}

results = []

# Loop through multiple pages
for page in range(1, 2000):
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        job_details = extract_job_details(data)
        results.extend(job_details)

    else:
        print(f"API request for page {page} failed with status code: {response.status_code}")

# Save the data to a text file
with open("naukri_jobs_data_lakhs.txt", "w", encoding="utf-8") as file:

    # Write job details to the file
    for job in results:
        file.write(f"Job ID: {job['Job ID']}\n")
        file.write(f"Job Title: {job['Job Title']}\n")
        file.write(f"Company Name: {job['Company Name']}\n")
        file.write(f"Footer Placeholder Label: {job['Footer Placeholder Label']}\n")
        file.write(f"Tags and Skills: {job['Tags and Skills']}\n")
        file.write(f"Experience: {job['Experience']}\n")
        file.write(f"Salary: {job['Salary']}\n")
        file.write(f"Location: {job['Location']}\n")
        file.write(f"Job Description: {job['Job Description']}\n")
        file.write("\n")

print("Data has been saved to naukri_jobs_data_lakhs.txt")
