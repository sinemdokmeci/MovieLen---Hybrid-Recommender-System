
#############################################
# PROJE: Hybrid Recommender System
#############################################

# ID'si verilen kullanıcı için item-based ve user-based recomennder yöntemlerini kullanarak tahmin yapınız.
# 5 öneri user-based modelden 5 öneri de item-based modelden ele alınız ve nihai olarak 10 öneriyi 2 modelden yapınız.

import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)

#############################################
# Verinin Hazırlanması
#############################################


# Movie ve Rating veri setlerini okutunuz.
# movieId, film adı ve filmin tür bilgilerini içeren veri seti
# UserID, film adı, filme verilen oy ve zaman bilgisini içeren veri seti

movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv') #Filmin numarası ve ismi vardır
rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv') #filmler hakkında bilgiler içeren veri setidir.


# Rating veri setine filmlerin isimlerini ve türünü movie film setini kullanrak ekleyiniz.
# Ratingdeki kullanıcıların oy kullandıkları filmlerin sadece id'si var.
# Idlere ait film isimlerini ve türünü movie veri setinden ekliyoruz.

df = movie.merge(rating, how="left", on="movieId") # İki dataframe i birleştiriyoruz
df.head()

# Herbir film için toplam kaç kişinin oy kullandığını hesaplayınız.Toplam oy kullanılma sayısı 1000'un altında olan filmleri veri setinden çıkarınız.
# Herbir film için toplam kaç kişinin oy kullanıldığını hesaplıyoruz.


# Toplam oy kullanılma sayısı 1000'in altında olan filmlerin isimlerini rare_movies de tutuyoruz.
# Ve veri setinden çıkartıyoruz
comment_counts = pd.DataFrame(df["title"].value_counts())
rare_movies = comment_counts[comment_counts["count"] <= 1000].index
common_movies = df[~df["title"].isin(rare_movies)]


# index'te userID'lerin sutunlarda film isimlerinin ve değer olarakta ratinglerin bulunduğu
# dataframe için pivot table oluşturunuz.
user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")


#  Yukarıda yapılan tüm işlemleri fonksiyonlaştıralım

def create_user_movie_df():
    import pandas as pd
    movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
    rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')
    df = movie.merge(rating, how="left", on="movieId")
    comment_counts = pd.DataFrame(df["title"].value_counts())
    rare_movies = comment_counts[comment_counts["count"] <= 10000].index #10000 yapmamın sebebi bilg yavaş çalıştığı için
    common_movies = df[~df["title"].isin(rare_movies)]
    user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
    return user_movie_df

user_movie_df = create_user_movie_df()

#############################################
# Öneri Yapılacak Kullanıcının İzlediği Filmlerin Belirlenmesi
#############################################

#  Rastgele bir kullanıcı id'si seçiniz.
random_user = int(pd.Series(user_movie_df.index).sample(1, random_state=45).values)


# Seçilen kullanıcıya ait gözlem birimlerinden oluşan random_user_df adında yeni bir dataframe oluşturunuz.
random_user_df = user_movie_df[user_movie_df.index == random_user]

# Seçilen kullanıcının oy kullandığı filmleri movies_watched adında bir listeye atayınız.
movies_watched = random_user_df.columns[random_user_df.notna().any()].tolist()

#############################################
# Aynı Filmleri İzleyen Diğer Kullanıcıların Verisine ve Id'lerine Erişmek
#############################################

# Seçilen kullanıcının izlediği fimlere ait sutunları user_movie_df'ten seçiniz ve movies_watched_df adında yeni bir dataframe oluşturuyoruz.
movies_watched_df = user_movie_df[movies_watched]

# Herbir kullancının seçili user'in izlediği filmlerin kaçını izlediği bilgisini taşıyan user_movie_count adında yeni bir dataframe oluşturunuz.
# Ve yeni bir df oluşturuyoruz.
user_movie_count = movies_watched_df.T.notnull().sum()
user_movie_count = user_movie_count.reset_index()


# Seçilen kullanıcının oy verdiği filmlerin yüzde 60 ve üstünü izleyenleri benzer kullanıcılar olarak görüyoruz.
# Bu kullanıcıların id’lerinden users_same_movies adında bir liste oluşturunuz.

user_movie_count.columns = ["userId", "movie_count"]

#Kullanıcının izlediği filmlerin en az %60 ını izleyenlerin üzerinden bir yorum yapabiliriz bu kişiden kişiye değişir
perc = len(movies_watched) * 60 / 100
users_same_movies = user_movie_count[user_movie_count["movie_count"] > perc]["userId"]



#############################################
# Öneri Yapılacak Kullanıcı ile En Benzer Kullanıcıların Belirlenmesi
#############################################

# user_same_movies listesi içerisindeki seçili user ile benzerlik gösteren kullanıcıların id’lerinin bulunacağı şekilde movies_watched_df dataframe’ini filtreleyiniz.
final_df = movies_watched_df[movies_watched_df.index.isin(users_same_movies)]

#  Kullanıcıların birbirleri ile olan korelasyonlarının bulunacağı yeni bir corr_df dataframe’i oluşturunuz.
corr_df = final_df.T.corr().unstack().sort_values().drop_duplicates()

#dataframe e çevirme
corr_df = pd.DataFrame(corr_df, columns=["corr"])
#isimlendirme
corr_df.index.names = ['user_id_1', 'user_id_2']

corr_df = corr_df.reset_index()

#corr_df[corr_df["user_id_1"] == random_user]



#  Seçili kullanıcı ile yüksek korelasyona sahip (0.65’in üzerinde olan) kullanıcıları filtreleyerek top_users adında yeni bir dataframe oluşturunuz.
top_users = corr_df[(corr_df["user_id_1"] == random_user) & (corr_df["corr"] >= 0.65)][
    ["user_id_2", "corr"]].reset_index(drop=True)
top_users.rename(columns={"user_id_2": "userId"}, inplace=True)

#  top_users dataframe’ine rating veri seti ile merge ediniz
rating = pd.read_csv('case_study/case_study_2/HybridRecommender-221114-235254/datasets/rating.csv')
top_users_ratings = top_users.merge(rating[["userId", "movieId", "rating"]], how='inner')
top_users_ratings = top_users_ratings[top_users_ratings["userId"] != random_user]




#############################################
#  Weighted Average Recommendation Score'un Hesaplanması ve İlk 5 Filmin Tutulması
#############################################

# Her bir kullanıcının corr ve rating değerlerinin çarpımından oluşan weighted_rating adında yeni bir değişken oluşturunuz.
top_users_ratings['weighted_rating'] = top_users_ratings['corr'] * top_users_ratings['rating']

#  Film id’sive her bir filme ait tüm kullanıcıların weighted rating’lerinin ortalama değerini içeren recommendation_df adında yeni bir
# dataframe oluşturunuz.
recommendation_df = top_users_ratings.groupby('movieId').agg({"weighted_rating": "mean"})

recommendation_df = recommendation_df.reset_index()

# Adım3: recommendation_df içerisinde weighted rating'i 3.5'ten büyük olan filmleri seçiniz ve weighted rating’e göre sıralayınız.
# İlk 5 gözlemi movies_to_be_recommend olarak kaydediniz.
movies_to_be_recommend = recommendation_df[recommendation_df["weighted_rating"] > 3.5].sort_values("weighted_rating", ascending=False)


# Tavsiye edilen 5 filmin isimlerini getiriniz.
movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
movies_to_be_recommend.merge(movie[["movieId", "title"]])["title"][:5]



#############################################
# Item-Based Recommendation
#############################################

# Kullanıcının en son izlediği ve en yüksek puan verdiği filmin adına göre item-based öneri yapınız.
user = 108170

# movie,rating veri setlerini okutunuz.
movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv') #Filmin numarası ve ismi vardır
rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv') #filmler hakkında bilgiler içeren veri setidir.

# Öneri yapılacak kullanıcının 5 puan verdiği filmlerden puanı en güncel olan filmin id'sinin alınız.
movie_id = rating[(rating["userId"] == user) & (rating["rating"] == 5.0)].sort_values(by="timestamp", ascending=False)["movieId"][0:1].values[0]

# User based recommendation bölümünde oluşturulan user_movie_df dataframe’ini seçilen film id’sine göre filtreleyiniz.
movie[movie["movieId"] == movie_id]["title"].values[0]
movie_df = user_movie_df[movie[movie["movieId"] == movie_id]["title"].values[0]]
movie_df

# Filtrelenen dataframe’i kullanarak seçili filmle diğer filmlerin korelasyonunu bulunuz ve sıralayınız.
user_movie_df.corrwith(movie_df).sort_values(ascending=False).head(10)


# Son iki adımı uygulayan fonksiyon
def item_based_recommender(movie_name, user_movie_df):
    movie = user_movie_df[movie_name]
    return user_movie_df.corrwith(movie).sort_values(ascending=False).head(10)


# Seçili film’in kendisi haricinde ilk 5 film’I öneri olarak veriniz.
movies_from_item_based = item_based_recommender(movie[movie["movieId"] == movie_id]["title"].values[0], user_movie_df)
# 1'den 6'ya kadar. 0'da filmin kendisi var. Onu dışarda bıraktık.
movies_from_item_based[1:6].index


# 'My Science Project (1985)',
# 'Mediterraneo (1991)',
# 'Old Man and the Sea,
# The (1958)',
# 'National Lampoon's Senior Trip (1995)',
# 'Clockwatchers (1997)']






