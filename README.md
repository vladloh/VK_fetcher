# VK_fetcher
Fetch social graph

Реализован скрипт, который поддерживает выгрузку социального графа из vk и некоторый его анализ:  
1. команда `vk-parser fetch id [-d 2] [--ignore-cache]` должна выдавать, сколько людей в социальном графе находятся на расстоянии не больше чем `d` от пользователя `id`  
2. `vk-parser dist id1 id2 [-d 2] [--ignore-cache]` должна выдавать длину кратчайшего пути и сам путь в социальном графе между пользователями `id1` и `id2` с лимитом на длину `d`  
3. Также реализовано кэширование — если мы недавно уже скачивали друзей какого-то пользователя, то нет смысла скачивать их ещё раз — можно просто сохранить имеющийся список  
4. Кэширование отключается опцией `--ignore-cache`  
5. Получение друзей пользователя реализуется через API VK.  
6. Для работы скрипта необходим ключ VK, если очень нужно — могу его прислать  


## Examples

`poetry run vk-parser dist 5 707 -d 4`  
Shortest path have 3 edges:  
5 -> 142582 -> 131588 -> 707

`poetry run vk-parser fetch 239932`  
2010 users by dist <= 2  

`poetry run vk-parser dist 70 6`  
Shortest path have 2 edges:  
70 -> 10 -> 6  


## VK_TOKEN
Make sure `config.cfg` exists:  
``` 
[VK_API]
VK_TOKEN = *********
```   

Getting token: https://vk.com/dev/access_token?f=3.%20Сервисный%20ключ%20доступа  

