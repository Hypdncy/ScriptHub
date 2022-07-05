冰蝎 Suircata 规则，主要匹配请求响应的base64
```
alert http any any -> any any  (msg: "Behinder3 PHP HTTP Request"; flow: established, to_server; content:".php"; http_uri;  pcre:"/[a-zA-Z0-9+/]{1000,}=/i"; flowbits:set,behinder3;noalert; classtype:shellcode-detect; sid: 3016017; rev: 1; metadata:created_at 2020_08_17,by al0ne;)
alert http any any -> any any (msg: "Behinder3  PHP HTTP Response"; flow: established,to_client; content:"200"; http_stat_code; flowbits: isset,behinder3; pcre:"/[a-zA-Z0-9+/]{100,}=/i"; classtype:shellcode-detect; sid: 3016018; rev: 1; metadata:created_at 2020_08_17,by al0ne;)
```