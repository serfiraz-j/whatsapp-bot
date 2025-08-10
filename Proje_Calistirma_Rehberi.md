# Proje Kurulum ve Çalıştırma Rehberi

Bu rehber, "AI Clinic Assistant" projesini kendi bilgisayarınızda kurup çalıştırmanız için gereken tüm adımları detaylı bir şekilde açıklamaktadır.

---

## 1. Ön Gereksinimler (Bilgisayarınızda Olması Gerekenler)

Projeyi çalıştırmadan önce bilgisayarınızda aşağıdaki yazılımların kurulu olduğundan emin olmalısınız:

* **Docker Desktop**: Projenin tüm servislerini (veritabanı, backend, redis vb.) kendi izole ortamlarında (konteyner) çalıştırmamızı sağlayan ana araçtır.
    * [Windows için Docker Desktop İndir](https://docs.docker.com/docker-for-windows/install/)
    * [Mac için Docker Desktop İndir](https://docs.docker.com/docker-for-mac/install/)
    * [Linux için Docker Kurulumu](https://docs.docker.com/engine/install/)
* **Git**: Proje dosyalarını bilgisayarınıza indirmek için kullanılan bir versiyon kontrol sistemidir.
    * [Git İndir](https://git-scm.com/downloads)

---

## 2. Proje Dosyalarını İndirme

1.  Terminali (veya Komut İstemi'ni) açın.
2.  Proje dosyalarını bilgisayarınızda saklamak istediğiniz bir klasöre gidin. Örneğin:
    ```bash
    cd Belgeler/Projelerim
    ```
3.  Aşağıdaki `git clone` komutu ile projenin bir kopyasını bilgisayarınıza indirin:
    ```bash
    git clone [https://github.com/sizin-kullanici-adiniz/ai-clinic-assistant.git](https://github.com/sizin-kullanici-adiniz/ai-clinic-assistant.git)
    ```
    (Not: Yukarıdaki linki projenin gerçek GitHub linki ile değiştirmeniz gerekecektir.)
4.  İndirilen proje klasörünün içine girin:
    ```bash
    cd ai-clinic-assistant
    ```

---

## 3. Projeyi Yapılandırma (.env Dosyası)

Projenin çalışması için gerekli olan API anahtarları ve gizli bilgileri `.env` adlı bir dosyada saklayacağız.

1.  Proje ana dizininde bulunan `.env.example` dosyasının bir kopyasını oluşturun ve adını `.env` olarak değiştirin. Bunu terminalde şu komutla yapabilirsiniz:
    ```bash
    cp .env.example .env
    ```
2.  Oluşturduğunuz `.env` dosyasını bir metin düzenleyici (VS Code, Notepad++ vb.) ile açın. İçindeki değerleri aşağıdaki açıklamalar doğrultusunda doldurun:

    * **POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB**: Veritabanı için kullanıcı adı, parola ve veritabanı ismidir. Genellikle geliştirme ortamı için bu değerleri değiştirmeden bırakabilirsiniz.
    * **SECRET_KEY**: JWT token'larını imzalamak için kullanılacak gizli bir anahtardır. Buraya karmaşık ve uzun bir metin yazın. Örneğin: `bunu-kimsenin-tahmin-edemeyecegi-cok-guclu-bir-anahtar-yap`
    * **OPENAI_API_KEY**: OpenAI'nin yapay zeka modellerini (GPT-4) kullanmak için gereklidir.
        * [OpenAI Platform web sitesine gidin](https://platform.openai.com/api-keys).
        * Giriş yapın ve "Create new secret key" butonuna tıklayarak yeni bir API anahtarı oluşturun.
        * Oluşturulan `sk-...` ile başlayan anahtarı kopyalayıp bu alana yapıştırın.
    * **PINECONE_API_KEY** ve **PINECONE_ENVIRONMENT**: RAG özelliği için kullanılacak vektör veritabanı servisidir.
        * [Pinecone web sitesine gidin](https://www.pinecone.io/).
        * Ücretsiz bir hesap oluşturun.
        * Giriş yaptıktan sonra sol menüdeki "API Keys" bölümünden API Key ve Environment değerlerinizi alıp ilgili alanlara yapıştırın.
    * **TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER**: WhatsApp entegrasyonu için gereklidir.
        * [Twilio web sitesine gidin](https://www.twilio.com/).
        * Bir hesap oluşturun ve giriş yapın.
        * Konsol (Dashboard) ana sayfanızda Account SID ve Auth Token değerlerinizi bulabilirsiniz.
        * WhatsApp entegrasyonunu kurduktan sonra size verilen WhatsApp numarasını `whatsapp:+1...` formatında `TWILIO_WHATSAPP_NUMBER` alanına girin.

---

## 4. Projeyi Çalıştırma

Tüm yapılandırma adımları tamamlandıktan sonra projeyi çalıştırmak için tek bir komut yeterlidir.

1.  Terminalde projenin ana dizininde olduğunuzdan emin olun (içinde `docker-compose.yml` dosyasının olduğu dizin).
2.  Aşağıdaki komutu çalıştırın:
    ```bash
    docker-compose up --build
    ```
    * `--build` parametresi: İlk çalıştırmada veya Dockerfile'da bir değişiklik yaptığınızda Docker imajlarını yeniden oluşturur.

Bu komut, `docker-compose.yml` dosyasındaki tüm servisleri (db, redis, backend, worker) sırayla indirip, kurup, başlatacaktır. Bu işlem ilk seferde internet hızınıza bağlı olarak birkaç dakika sürebilir.

---

## 5. Kurulumu Doğrulama

Her şeyin yolunda gidip gitmediğini kontrol etmek için:

* **Docker Loglarını Kontrol Etme**: Komutu çalıştırdığınız terminalde servislerin logları akmaya başlayacaktır. Herhangi bir Error veya Crash mesajı olup olmadığını kontrol edin.
* **Konteynerleri Listeleme**: Yeni bir terminal açın ve `docker ps` komutunu çalıştırın. `clinic_db`, `clinic_redis`, `clinic_backend` ve `clinic_worker` isimli dört konteynerin de "Up" (Çalışıyor) durumunda olduğunu görmelisiniz.
* **API Dokümantasyonuna Erişme**: Bir web tarayıcısı açın ve `http://localhost:8000/docs` adresine gidin. Karşınıza projenin interaktif API dokümantasyonu (Swagger UI) geliyorsa, backend başarıyla çalışıyor demektir.

Artık projeniz çalışır durumda! API dokümantasyonu üzerinden endpoint'leri test etmeye başlayabilirsiniz.
