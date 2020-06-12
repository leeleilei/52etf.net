---
blog: true
date: 2020-06-12
title: 免费CDN的最正确使用姿势
categories: [Web]
tags: [CDN,jsdelivr,github]
draft: false
---

阿里的图床真的买瞎了，尼玛套餐包不包含下行流量，好比买了个车不让上高速，活久见。

用了两天，穿了不到10张图片，收了我8毛钱，这要是访问上万，我不背一身债啊。

思来想去还是Github的图床香，问题是速度慢，继续搜索方案时，找到了jsdelivr，果然神奇。

大陆唯一备案审批通过的外国站点CDN，可以加速npm和Github。

China --> jsdelivr --> Github (html/js/img/binary)

只要大小不超过10M，任何都可以加速，而且是免费的。

更高级的玩法是高清视频切割，制作一个播放列表m3ua，配合在线播放器可以完美在线视频。

但绕不开IP和主机，所以才得以审批通过，所以阿里的主机仍然要买，虽然很难用。

