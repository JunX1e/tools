import  urllib.request

response = urllib.request.urlopen('https://bat.fx.ctripcorp.com/d/n-3j5q6VkFLT/ji-piao-tripshang-yun-qmqshu-li-gong-ju?var-appId=100033849&var-consumerSubject=All&var-producerSubject=All&from=now-2d&to=now&orgId=0')
html = response.read().decode('utf-8')

print(html)