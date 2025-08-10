AI Clinic Assistant - FastAPI BackendBu proje, klinikler (güzellik salonları, diş klinikleri, terapi merkezleri vb.) için özel olarak tasarlanmış, yapay zeka destekli bir WhatsApp asistanı için üretime hazır, çok kullanıcılı (multi-tenant) bir backend sistemidir. Ölçeklenebilir, özelleştirilebilir ve sağlam bir çözüm sunmak için Python, FastAPI ve bir dizi modern teknoloji ile oluşturulmuştur.✨ ÖzelliklerÇekirdek Backend:FastAPI: Yüksek performanslı asenkron web framework'ü.PostgreSQL: Veri kalıcılığı için sağlam ilişkisel veritabanı.Pydantic: Veri doğrulama ve ayar yönetimi.Celery & Redis: Arka plan işlemleri için asenkron görev kuyruğu.FastAPI Users & JWT: Güvenli kimlik doğrulama ve kullanıcı yönetimi.Ortam Bazlı Yapılandırma: Kolay yapılandırma için .env kullanımı.🤖 Yapay Zeka Entegrasyonu:OpenAI GPT-4: Konuşma tabanlı yapay zeka için en gelişmiş dil modeli.Dinamik Prompt Mühendisliği: "Prompt"lar (yapay zekaya verilen talimatlar) her klinik için (isim, servisler, ton vb.) özelleştirilir.Sohbet Geçmişi: Tüm konuşmalar, inceleme ve ince ayar için kaydedilir.Akış (Streaming) Yanıtları: Gerçek zamanlı mesaj akışı için Server-Sent Events (SSE).💬 WhatsApp Entegrasyonu:Twilio/360Dialog: Başlıca WhatsApp Business API sağlayıcılarıyla entegrasyona hazır.Mesaj Kuyruklama: Celery, gelen mesajların güvenilir bir şekilde işlenmesini sağlar.🧠 Vektör Veritabanı (RAG):Pinecone Entegrasyonu: Kliniğe özgü belgelerde verimli benzerlik araması için.Belge Yönetimi: Klinikler, yapay zeka için bağlam olarak kullanılacak belgeleri (SSS, hizmet listeleri) yükleyebilir.Retrieval Augmented Generation (RAG): Vektör deposundan alınan bilgilerle yapay zeka yanıtlarını zenginleştirir.⚙️ Yönetim & Özelleştirme:Çoklu Kullanıcı (Multi-Tenancy): Her klinik için veri izolasyonu.Yönetim Paneli (FastAPI üzerinden): Klinik kaydı, hizmet yönetimi ve yapay zeka ayarları için endpoint'ler.Sohbet Geçmişi Görüntüleyici: Her klinik için konuşmaları inceleme endpoint'i.🚀 DevOps & Dağıtım:Docker & Docker Compose: Kolay geliştirme ve dağıtım için konteynerize edilmiş kurulum.Gunicorn: Üretime hazır WSGI sunucusu.Loguru: Yapılandırılmış ve güçlü loglama.OpenAPI Dokümantasyonu: Otomatik interaktif API dokümanları.Health Check: Servis durumunu izlemek için endpoint.📂 Proje Yapısıapp/
├── main.py
├── config.py
├── database.py
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── chat.py
│   ├── clinic.py
│   └── user.py
├── schemas/
│   ├── __init__.py
│   ├── chat.py
│   ├── clinic.py
│   ├── token.py
│   └── user.py
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   ├── chat.py
│   └── clinic.py
├── services/
│   ├── __init__.py
│   ├── auth.py
│   ├── ai_engine.py
│   ├── vectorstore.py
│   └── whatsapp.py
├── utils/
│   ├── __init__.py
│   └── prompt_builder.py
├── background/
│   ├── __init__.py
│   └── tasks.py
└── admin/
    ├── __init__.py
    └── dashboard.py
.env.example
docker-compose.yml
Dockerfile
requirements.txt
🚀 BaşlarkenProjenin kurulumu ve çalıştırılmasıyla ilgili tüm adımlar için KURULUM_REHBERI.md dosyasına bakın.
