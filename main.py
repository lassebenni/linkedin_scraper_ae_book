import requests
import json

from models.linkedin_response import LinkedInPost, LinkedInResponse

session = requests.Session()

url = "https://www.linkedin.com/voyager/api/graphql?variables=(start:6,origin:CLUSTER_EXPANSION,query:(keywords:fundamentals%20of%20analytics%20engineering,flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:resultType,value:List(CONTENT)),(key:searchId,value:List(15a49aba-1ed3-463a-b535-130735ab04e4)))),count:3)&queryId=voyagerSearchDashClusters.09f1c85c0e383740672f698538438a2b"

payload = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Accept": "application/vnd.linkedin.normalized+json+2.1",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "x-li-lang": "nl_NL",
    "x-li-track": '{"clientVersion":"1.13.19075","mpVersion":"1.13.19075","osName":"web","timezoneOffset":2,"timezone":"Europe/Amsterdam","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2,"displayWidth":3840,"displayHeight":2160}',
    "x-li-page-instance": "urn:li:page:d_flagship3_search_srp_content;oX0Tee1uTwiUKIIgsZvdnA==",
    "csrf-token": "ajax:1797525637115598100",
    "x-restli-protocol-version": "2.0.0",
    "x-li-pem-metadata": "Voyager - Content SRP=search-results",
    "Connection": "keep-alive",
    "Referer": "https://www.linkedin.com/search/results/content/?keywords=fundamentals%20of%20analytics%20engineering&origin=CLUSTER_EXPANSION&searchId=15a49aba-1ed3-463a-b535-130735ab04e4&sid=yVK",
    "Cookie": 'bcookie="v=2&b2020c86-5dc3-450f-8853-13bd30b0d156"; JSESSIONID="ajax:1797525637115598100"; bscookie="v=1&20211004095419a8a64eb7-c383-40c9-8b77-c363cfdfa0d4AQGBJ-9en2GmUJue1o18R5iGKPYf_YsJ"; li_alerts=e30=; G_ENABLED_IDPS=google; li_mc=MTsyMTsxNzE5NDM0NzA4OzI7MDIxDHdtVlZdvaX/5B9RD1cadKLT1sXzWbSBwQrpxxXE0P0=; li_theme=light; li_theme_set=app; li_at=AQEDARP6H5YEvw4xAAABhr2-6qQAAAGQXZs4I00Aqv8UK4cYlRjAJso8rFyKY5clmdxJxntps9-ZfAhuEq7jMqzrWezt-4WKncy6fL9dC4ak-XrICbqEsPG1Ba4CRPIZ8S6yCnZ9w8S57-q_QNulqsJe; liap=true; UserMatchHistory=AQKdNUH45MUZ8QAAAZBWT3Aqd5KvM1_V6K5t2ycHH5w1YOcCMjD4rH8T1c_TzXDTOSRXvIIL8O36U3iHDNVtqw2smXq8wMF_ZZBoIFgKI_90UA-jiyeLE25kvhSMFsrE-LXICYN75usQGojLjRVgxThQA8T5JROqND7woo07Pn9mE-eTBfeP7-T9eN0MTLEdj5CrRLmR3Qa58r_sH3zcl6YOJP0Wn3rrOEOEA3kBJtXLkl3s0aaGfHpHV3XvZBFS1pEBJhUtQwXrOSVIHvD4vlj0etyq_IzuFnISzengp9mHqDuVIn1eyRY0IeCd8onhwOBUJNPKcp1akNxZkXyS9ta-8c8Mt9oIdPzL0EDxOKo-; timezone=Europe/Amsterdam; dfpfpt=97ee2766a8f04da2a287da21030ad4f5; lidc="b=TB90:s=T:r=T:a=T:p=T:g=4069:u=895:x=1:i=1719434105:t=1719510095:v=2:sig=AQHyVMQZay47Zr9L28c-p6nf_Iu7FdWs"; lang=v=2&lang=nl-nl; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; lil-lang=en_US; s_ppv=www.linkedin.com%2Flearning%2Flearning-github-actions-2%2C83%2C42%2C1779%2C1%2C2; s_ips=912; s_tp=2148; s_cc=true; s_plt=12.33; s_pltp=www.linkedin.com%2Flearning%2Flearning-github-actions-2; s_sq=lnkdprod%3D%2526c.%2526a.%2526activitymap.%2526page%253Dwww.linkedin.com%25252Flearning%25252Flearning-github-actions-2%2526link%253DShow%252520less%2526region%253Dember47%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dwww.linkedin.com%25252Flearning%25252Flearning-github-actions-2%2526pidt%253D1%2526oid%253DShow%252520less%2526oidt%253D3%2526ot%253DSUBMIT; PLAY_LANG=nl; PLAY_SESSION=eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7InNlc3Npb25faWQiOiIyMmE4NDY5Mi03YjI4LTQ5MmItOWY4Yi1mMmJjOTIzMzEzNjF8MTY4MzcwNDE4OSIsImFsbG93bGlzdCI6Int9IiwicmVjZW50bHktc2VhcmNoZWQiOiIiLCJyZWZlcnJhbC11cmwiOiJodHRwczovL3d3dy5saW5rZWRpbi5jb20vaW4vbGFzc2UtYmVubmluZ2EtYTQ2MmIxOTQvZGV0YWlscy9leHBlcmllbmNlL2VkaXQvZm9ybXMvMjE3MjgzMDE1NS8_cHJvZmlsZUZvcm1FbnRyeVBvaW50PVBST0ZJTEVfU0VDVElPTiIsImFpZCI6IiIsInJlY2VudGx5LXZpZXdlZCI6IjU0ODU5MyIsIkNQVC1pZCI6IjzCssKKXHUwMDE2I8Olw7jDmFx1MDAxRMO1wpLDm1xudn_DmCIsImV4cGVyaWVuY2UiOiJlbnRpdHkiLCJ0cmsiOiIifSwibmJmIjoxNjgzNzA0MTkwLCJpYXQiOjE2ODM3MDQxOTB9.L-QxzNmGycKEjgL32niBt-Q0tVkwVrhLnvTC5k120n8; fptctx2=taBcrIH61PuCVH7eNCyH0J9Fjk1kZEyRnBbpUW3FKs9c%252fDr2Ws%252buGVR8BooaDBAy6%252fgBMP3WsJmhC69C4Nl7TKhnhUTUDNIfmQtr87B%252b79TcvaKUpsVjT80UDWU76l2Yu%252ftX2Cb1vhvFbftC83DOevE12g6O%252bjQaj4jCcM0gWRYONDgsxRYfUmGVckxr%252fQxB8yk7dPSbnZhXmw65yIXcDbvC49%252fFRJzO0zQ4LTIPemLUY02Iegk%252bWgXcAEqVE2RK8924g%252bZ9DipZr%252fUUYR1yJrzCZB9fNTOrU6dfBXbOT3KYFSSkcWL0teyA3mGyAS1MojYlaglCChSPeELZ7Kv0UsVQ%252by4uy8yrS8dsDoWlmXk%253d',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "DNT": "1",
    "Sec-GPC": "1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers",
}

response = session.get(url, headers=headers, data=payload)

res = response.json()

posts: list[LinkedInPost] = LinkedInResponse(**res).included

posts_dicts = [post.dict() for post in posts]

# Serialize the list of dictionaries to a JSON string and write it to a file
with open("posts.json", "w") as f:
    json.dump(posts_dicts, f, ensure_ascii=False, indent=4)
