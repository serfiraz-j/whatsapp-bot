# AI Clinic Assistant - FastAPI Backend

Bu proje, kliniklere (güzellik salonları, diş klinikleri, terapi merkezleri vb.) özel, **WhatsApp tabanlı AI asistan** için hazırlanmış, üretim seviyesinde, çok kiracılı (**multi-tenant**) bir backend çözümüdür.  
Python, FastAPI ve modern teknolojilerle ölçeklenebilir, özelleştirilebilir ve sağlam bir altyapı sunar.

---

## ✨ Özellikler

### **Core Backend**
- **FastAPI**: Yüksek performanslı asenkron web framework
- **PostgreSQL**: Veri saklama için güçlü ilişkisel veritabanı
- **Pydantic**: Veri doğrulama ve ayar yönetimi
- **Celery & Redis**: Arka plan görevleri için asenkron kuyruk sistemi
- **FastAPI Users & JWT**: Güvenli kimlik doğrulama ve kullanıcı yönetimi
- **Environment-based Config**: `.env` dosyası ile kolay yapılandırma

---

### 🤖 **AI Entegrasyonu**
- **OpenAI GPT-4**: En gelişmiş dil modeli ile konuşma AI
- **Dynamic Prompt Engineering**: Klinik adı, hizmetler, ton vb. ile özelleştirilmiş prompt’lar
- **Chat History**: Tüm konuşmalar kayıt altına alınır
- **Streaming Responses**: **Server-Sent Events (SSE)** ile gerçek zamanlı yanıt akışı

---

### 💬 **WhatsApp Entegrasyonu**
- **Twilio / 360Dialog**: Büyük WhatsApp Business API sağlayıcılarıyla hazır entegrasyon
- **Message Queueing**: Gelen mesajların güvenilir işlenmesi için Celery kuyruğu

---

### 🧠 **Vector Database (RAG)**
- **Pinecone Integration**: Klinik belgeleri üzerinde hızlı benzerlik araması
- **Document Management**: Klinikler, AI’nın kullanacağı belgeleri (SSS, hizmet listesi) yükleyebilir
- **Retrieval Augmented Generation (RAG)**: AI yanıtlarını vektör deposundan alınan bilgilerle zenginleştirir

---

### ⚙️ **Admin & Özelleştirme**
- **Multi-Tenancy**: Her klinik için veri izolasyonu
- **Admin Panel (FastAPI)**: Klinik kaydı, hizmet yönetimi ve AI ayarları
- **Chat History Viewer**: Klinik bazlı konuşma geçmişi görüntüleme

---

### 🚀 **DevOps & Deployment**
- **Docker & Docker Compose**: Kolay kurulum ve dağıtım için container yapısı
- **Gunicorn**: Üretim seviyesi WSGI sunucusu
- **Loguru**: Yapılandırılmış, güçlü logging
- **OpenAPI Documentation**: Otomatik interaktif API dokümanları
- **Health Check**: Servis durumunu izleme endpoint’i

---

## 📂 Proje Yapısı

``` 
app/
├── main.py
├── config.py
├── database.py
├── models/
│ ├── init.py
│ ├── base.py
│ ├── chat.py
│ ├── clinic.py
│ └── user.py
├── schemas/
│ ├── init.py
│ ├── chat.py
│ ├── clinic.py
│ ├── token.py
│ └── user.py
├── routers/
│ ├── init.py
│ ├── auth.py
│ ├── chat.py
│ └── clinic.py
├── services/
│ ├── init.py
│ ├── auth.py
│ ├── ai_engine.py
│ ├── vectorstore.py
│ └── whatsapp.py
├── utils/
│ ├── init.py
│ └── prompt_builder.py
├── background/
│ ├── init.py
│ └── tasks.py
└── admin/
├── init.py
└── dashboard.py

.env.example
docker-compose.yml
Dockerfile
requirements.txt
``` 

---

## 🚀 Başlangıç

### **Gereksinimler**
- Docker ve Docker Compose
- OpenAI API Key
- Pinecone API Key ve Environment bilgileri
- Twilio (veya başka bir sağlayıcı) hesabı: **SID, Auth Token, WhatsApp numarası**

### **Kurulum Adımları**

1. **Repo’yu klonla**

```bash
git clone <repo_url>
cd <repo_klasörü>
```

2. **Ortam dosyasını oluştur ve yapılandır**
```bash
cp .env.example .env
```

3. Docker ile çalıştır

```bash
docker-compose up --build
```
Bu işlem FastAPI uygulaması, PostgreSQL, Redis ve Celery worker’ını başlatır.

API Dokümantasyonuna eriş
Tarayıcıdan http://localhost:8000/docs adresine git.


## 🔍 Çalışma Mantığı

1. **Klinik Kaydı**  
   Klinik sahibi bir hesap oluşturur.

2. **Konfigürasyon**  
   Klinik bilgileri, hizmetler ve AI kişiliği ayarlanır.

3. **Belge Yükleme**  
   Yüklenen belgeler (örn. SSS) parçalara ayrılır, embed edilir ve Pinecone’a kaydedilir.

4. **WhatsApp Mesajı**  
   Müşteri, kliniğin WhatsApp numarasına mesaj gönderir.

5. **Mesaj Alma**  
   Twilio mesajı `/whatsapp/webhook` endpoint’ine iletir.

6. **AI İşleme**  
   - Mesaj Celery kuyruğuna eklenir.  
   - Pinecone’dan ilgili bilgiler çekilir (**RAG** yöntemi).  
   - Dinamik prompt oluşturulur.  
   - GPT-4’ten yanıt alınır.

7. **Yanıt Gönderme**  
   Üretilen yanıt, Twilio API’si aracılığıyla müşteriye iletilir.

8. **Kayıt**  
   Tüm konuşma veritabanına kaydedilir.
