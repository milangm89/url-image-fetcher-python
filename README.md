## Simple python script to download all images from all the links in a website.
## This is a simple python script to get all the urls of a domain and download all the image files in those urls

Input: website name


Output: 
1. It will fetch all the urls under the domain
2. It will fetch all the image links under the urls fetched in the previous step.
3. Download all the images displayed in the second step to a folder.
4. Upload the downloaded image files on to s3


Prerequisite:

Install the python3 modules by running the below command.

```pip3 install -r requirements.txt```

Run the file by using the below command:

```python3 src/url-fetcher.py```

I have added the site "bgr.in" in the function main for an example.

```
if __name__ == "__main__":
    site = 'https://www.bgr.in'
```