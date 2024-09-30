# MovieLen---Hybrid-Recommender-System
MovieLen - 10 Film Önerisi

# İş Problemi
Bu projede, film platformlarında kullanıcılara sunulan öneri sistemlerinin verimliliğini artırmak hedeflenmektedir. İlgili kullanıcı için hem item-based hem de user-based öneri yöntemlerini kullanarak, kullanıcının beğenisine uygun filmler önerilmeye çalışılacaktır. Her iki modelin önerilerini birleştirerek daha geniş ve zengin bir öneri seti sunmak amaçlanmaktadır.

# Veri Seti Hikayesi
Proje kapsamında kullanılan veri seti, MovieLens veritabanından alınmıştır. Bu veri seti, film öneri sistemlerinde yaygın olarak kullanılır ve kullanıcılara ait film puanlama bilgileri içerir.

Movie veri seti: Filmlerin ID’si, isimleri ve türlerini içerir.
Rating veri seti: Kullanıcıların izledikleri filmlere verdikleri puanlar ve oylama tarihlerini barındırır.

Bu iki veri seti birleştirilerek, kullanıcıların hangi filmleri izledikleri ve hangi puanları verdikleri analiz edilir. Proje boyunca, bu veri setleri kullanılarak hem item-based hem de user-based öneri sistemleri oluşturulacaktır.

# Proje Amacı
Bu projenin amacı, item-based ve user-based yaklaşımlar kullanarak kullanıcılara daha doğru film önerileri sunmaktır. Her iki modelin çıktılarının harmanlanmasıyla, kullanıcının beğenisine en uygun filmler önerilecek ve kullanıcı deneyimi iyileştirilecektir. Nihai hedef, kullanıcıların ilgisini çekecek filmleri tahmin ederek öneri sisteminin performansını artırmaktır.

## Aşamalar
# 1. Veri Hazırlama
Movie ve Rating veri setleri birleştirilir.
Kullanıcıların oy verdiği filmler analiz edilerek, yeterli sayıda oy almayan filmler filtrelenir ve veri setinden çıkarılır.
Kullanıcıların oy verdiği filmler, bir pivot tabloya dönüştürülerek, her kullanıcının hangi filmleri izlediği ve nasıl değerlendirdiği analiz edilir.

# 2. Öneri Yapılacak Kullanıcının Belirlenmesi
Rastgele bir kullanıcı seçilir ve bu kullanıcının izlediği filmler tespit edilir.
Bu filmleri izleyen diğer kullanıcıların verisi kullanılarak, öneri yapılacak kullanıcıya en benzer kullanıcılar belirlenir.

# 3. Benzer Kullanıcıların Belirlenmesi
Kullanıcının izlediği filmlerin %60 ve üstünü izleyen diğer kullanıcılar belirlenir.
Bu kullanıcılar ile öneri yapılacak kullanıcı arasındaki korelasyon hesaplanarak, en yüksek korelasyona sahip kullanıcılar seçilir.

# 4. User-Based Öneri Sistemi
Kullanıcılarla olan korelasyon kullanılarak, öneri yapılacak kullanıcıya benzer kullanıcıların izleyip yüksek puan verdiği filmler tespit edilir.
Her filmin öneri puanı, kullanıcıların korelasyonuna göre ağırlıklandırılarak hesaplanır ve en yüksek puanlı 5 film önerilir.

# 5. Item-Based Öneri Sistemi
Kullanıcının en son izlediği ve en yüksek puan verdiği film tespit edilir.
Bu film ile diğer filmler arasındaki korelasyon hesaplanarak, en çok benzeyen 5 film item-based yöntemle önerilir.

# 6. Nihai Öneri
Her iki yöntemle önerilen 5'er film birleştirilerek, toplamda 10 film önerisi oluşturulur.
