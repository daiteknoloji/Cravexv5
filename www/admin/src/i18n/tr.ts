import turkishMessages from "ra-language-turkish";

import { SynapseTranslationMessages } from ".";

const tr: SynapseTranslationMessages = {
  ...turkishMessages,
  synapseadmin: {
    auth: {
      base_url: "Ana Sunucu URL",
      welcome: "Synapse Admin'e Hoş Geldiniz",
      server_version: "Synapse sürümü",
      supports_password_login: "Şifre ile giriş desteği",
      sso_sign_in: "SSO ile oturum aç",
    },
    users: {
      invalid_user_id: "Geçerli bir Matrix kullanıcı ID'si girmelisiniz.",
      tabs: { sso: "SSO" },
    },
    rooms: {
      details: "Oda detayları",
      tabs: {
        basic: "Temel",
        members: "Üyeler",
        detail: "Detaylar",
        permission: "İzinler",
        messages: "Mesajlar",
      },
    },
    reports: { tabs: { basic: "Temel", detail: "Detaylar" } },
  },
  import_users: {
    error: {
      at_entry: "Giriş numarası %{entry}: %{message}",
      error: "Hata",
      required_field: "Gerekli alan '%{field}' eksik",
      invalid_value: "Satır %{row}: '%{field}' için geçersiz değer. BOOLEAN olmalı",
      unreasonably_big: "Dosya aşırı büyük (%{size} MB), daha küçük bir dosya yükleyin",
      already_in_progress: "Bir içe aktarım zaten devam ediyor",
      id_exits: "ID %{id} zaten var",
    },
    title: "Kullanıcıları CSV ile içe aktar",
    goToPdf: "PDF'ye git",
    cards: {
      importstats: {
        header: "Kullanıcıları içe aktar",
        users_total: "Toplam kullanıcı: %{smart_count}",
        guest_count: "Misafir: %{smart_count}",
        admin_count: "Yönetici: %{smart_count}",
      },
      conflicts: {
        header: "Çakışma Stratejisi",
        mode: {
          stop: "Çakışma durumunda durdur",
          skip: "Çakışma durumunda kaydetme ve göster",
        },
      },
      ids: {
        header: "ID'ler",
        all_ids_present: "Her girdide ID var",
        count_ids_present: "%{smart_count} girdide ID var",
        mode: {
          ignore: "CSV'deki ID'leri yoksay ve yenilerini oluştur",
          update: "CSV'deki ID'leri kullanarak mevcut kullanıcıları güncelle",
        },
      },
      passwords: {
        header: "Şifreler",
        all_passwords_present: "Her girdide şifre var",
        count_passwords_present: "%{smart_count} girdide şifre var",
        use_passwords: "CSV'deki şifreleri kullan",
      },
      upload: {
        header: "CSV dosyası yükle",
        explanation: "Kullanıcıları oluşturmak veya güncellemek için virgülle ayrılmış değerler içeren bir dosya yükleyin.",
      },
      startImport: {
        simulate_only: "Sadece simüle et",
        run_import: "İçe aktarmayı çalıştır",
      },
      results: {
        header: "İçe Aktarım Sonuçları",
        total: "Toplam: %{smart_count} giriş",
        successful: "Başarılı: %{smart_count}",
        skipped: "Atlanan: %{smart_count}",
        download_skipped: "Atlananları indir",
        with_error: "Hatalı: %{smart_count}",
        simulated_only: "Sadece simülasyon",
      },
    },
  },
  resources: {
    users: {
      name: "Kullanıcı |||| Kullanıcılar",
      email: "E-posta",
      msisdn: "Telefon",
      threepid: "E-posta / Telefon",
      fields: {
        avatar: "Avatar",
        id: "Kullanıcı ID",
        name: "Ad",
        is_guest: "Misafir",
        admin: "Sunucu Yöneticisi",
        deactivated: "Devre Dışı",
        guests: "Misafirleri göster",
        show_deactivated: "Devre dışı kullanıcıları göster",
        user_id: "Kullanıcı ara",
        displayname: "Görünen Ad",
        password: "Şifre",
        avatar_url: "Avatar URL",
        avatar_src: "Avatar",
        medium: "Ortam",
        threepids: "3PID'ler",
        address: "Adres",
        creation_ts_ms: "Oluşturma zamanı",
        consent_version: "Onay sürümü",
        auth_provider: "Sağlayıcı",
        user_type: "Kullanıcı tipi",
        locked: "Kilitli",
      },
      helper: {
        password: "Şifre değiştirmek kullanıcıyı tüm oturumlardan çıkaracaktır.",
        deactivate: "Bir hesabı yeniden etkinleştirmek için şifre vermelisiniz.",
        erase: "Kullanıcıyı GDPR silinmiş olarak işaretle",
      },
      action: {
        erase: "Kullanıcı verilerini sil",
      },
    },
    rooms: {
      name: "Oda |||| Odalar",
      fields: {
        room_id: "Oda ID",
        name: "İsim",
        canonical_alias: "Takma ad",
        joined_members: "Üyeler",
        joined_local_members: "Yerel üyeler",
        joined_local_devices: "Yerel cihazlar",
        state_events: "Durum olayları / Karmaşıklık",
        version: "Sürüm",
        is_encrypted: "Şifreli",
        encryption: "Şifreleme",
        federatable: "Federasyona açık",
        public: "Oda dizininde görünür",
        creator: "Oluşturan",
        join_rules: "Katılma kuralları",
        guest_access: "Misafir erişimi",
        history_visibility: "Geçmiş görünürlüğü",
        topic: "Konu",
        avatar: "Avatar",
        message_type: "Tip",
        message_body: "Mesaj",
      },
      tabs: {
        messages: "Mesajlar",
      },
      helper: {
        forward_extremities:
          "Forward extremities, bir odadaki Directed acyclic graph (DAG) sonundaki yaprak olaylardır, yani çocuğu olmayan olaylardır. Bir odada ne kadar çok varsa, Synapse o kadar çok durum çözümlemesi yapmalıdır (ipucu: pahalı bir işlemdir). Synapse bir odada bunların aynı anda çok fazla olmasını engelleyen koda sahip olsa da, hatalar bazen bunların tekrar ortaya çıkmasına neden olabilir. Bir odada >10 forward extremity varsa, hangi odanın suçlu olduğunu kontrol etmeye ve #1760'ta bahsedilen SQL sorgularını kullanarak bunları kaldırmaya değer.",
      },
      enums: {
        join_rules: {
          public: "Herkese açık",
          knock: "Tıkla",
          invite: "Davet",
          private: "Özel",
        },
        guest_access: {
          can_join: "Misafirler katılabilir",
          forbidden: "Misafirler katılamaz",
        },
        history_visibility: {
          invited: "Davet edildiğinden beri",
          joined: "Katıldığından beri",
          shared: "Paylaşıldığından beri",
          world_readable: "Herkes",
        },
        unencrypted: "Şifrelenmemiş",
      },
      action: {
        erase: {
          title: "Odayı sil",
          content:
            "Odayı silmek istediğinizden emin misiniz? Bu geri alınamaz. Odadaki tüm mesajlar ve paylaşılan medya sunucudan silinecektir!",
        },
      },
    },
    reports: {
      name: "Bildirilen olay |||| Bildirilen olaylar",
      fields: {
        id: "ID",
        received_ts: "bildirim zamanı",
        user_id: "bildiren",
        name: "odanın adı",
        score: "puan",
        reason: "sebep",
        event_id: "olay ID",
        event_json: {
          origin: "kaynak sunucu",
          origin_server_ts: "gönderim zamanı",
          type: "olay tipi",
          content: {
            msgtype: "içerik tipi",
            body: "içerik",
            info: {
              mimetype: "mime tipi",
            },
          },
        },
      },
    },
    connections: {
      name: "Bağlantı |||| Bağlantılar",
      fields: {
        last_seen: "Tarih",
        ip: "IP adresi",
        user_agent: "Kullanıcı agent",
      },
    },
    devices: {
      name: "Cihaz |||| Cihazlar",
      fields: {
        device_id: "Cihaz ID",
        display_name: "Cihaz adı",
        last_seen_ts: "Zaman damgası",
        last_seen_ip: "IP adresi",
      },
      action: {
        erase: {
          title: "Cihazları kaldır",
          content: "%{smart_count} cihazı kaldırmak istediğinizden emin misiniz?",
          success: "%{smart_count} cihaz başarıyla kaldırıldı.",
          failure: "Cihazları kaldırırken hata oluştu.",
        },
      },
    },
    users_media: {
      name: "Medya",
      fields: {
        media_id: "Medya ID",
        media_length: "Dosya boyutu (Byte)",
        media_type: "Tip",
        upload_name: "Dosya adı",
        quarantined_by: "Karantinaya alan",
        safe_from_quarantine: "Karantinadan güvenli",
        created_ts: "Oluşturulma",
        last_access_ts: "Son erişim",
      },
    },
    delete_media: {
      name: "Medya",
      fields: {
        before_ts: "son erişim öncesi",
        size_gt: "daha büyük (Byte)",
        keep_profiles: "Profil resimlerini koru",
      },
      action: {
        send: "Medya sil",
        send_success: "İstek başarıyla gönderildi.",
        send_failure: "İstek gönderilirken hata oluştu.",
      },
      helper: {
        send: "Bu API, belirtilen koşullara uyan yerel medyayı siler.",
      },
    },
    protect_media: {
      action: {
        create: "Korumasız, korumayı ekle",
        delete: "Korumalı, korumayı kaldır",
        none: "Karantinada",
        send_success: "Koruma durumu başarıyla değiştirildi.",
        send_failure: "Koruma durumu değiştirilirken hata oluştu.",
      },
    },
    quarantine_media: {
      action: {
        name: "Karantina",
        create: "Karantinayla birlikte ekle",
        delete: "Karantinadan kaldır, karantinayla birlikte kaldır",
        none: "Karantinadan güvenli",
        send_success: "Karantina durumu başarıyla değiştirildi.",
        send_failure: "Karantina durumu değiştirilirken hata oluştu.",
      },
    },
    pushers: {
      name: "İtici |||| İticiler",
      fields: {
        app: "Uygulama",
        app_display_name: "Uygulama görünen adı",
        app_id: "Uygulama ID",
        device_display_name: "Cihaz görünen adı",
        kind: "Tür",
        lang: "Dil",
        profile_tag: "Profil etiketi",
        pushkey: "İtme anahtarı",
        data: { url: "URL" },
      },
    },
    servernotices: {
      name: "Sunucu bildirimleri",
      send: "Sunucu bildirimlerini gönder",
      fields: {
        body: "Mesaj",
      },
      action: {
        send: "Bildirim gönder",
        send_success: "Sunucu bildirimi başarıyla gönderildi.",
        send_failure: "Sunucu bildirimi gönderilirken hata oluştu.",
      },
      helper: {
        send: 'Bu kullanıcılara sunucu bildirimleri gönderir. "Sunucu Bildirimleri" özelliği sunucuda etkinleştirilmelidir.',
      },
    },
    user_media_statistics: {
      name: "Kullanıcı medya istatistikleri",
      fields: {
        media_count: "Medya sayısı",
        media_length: "Medya uzunluğu",
      },
    },
    forward_extremities: {
      name: "Forward Extremities",
      fields: {
        id: "Olay ID",
        received_ts: "Zaman damgası",
        depth: "Derinlik",
        state_group: "Durum grubu",
      },
    },
    room_state: {
      name: "Durum olayı |||| Durum olayları",
      fields: {
        type: "Tip",
        content: "İçerik",
        origin_server_ts: "Gönderilme zamanı",
        sender: "Gönderen",
      },
    },
    room_directory: {
      name: "Oda dizini",
      fields: {
        world_readable: "Misafir kullanıcılar üye olmadan okuyabilir",
        guest_can_join: "Misafir kullanıcılar katılabilir",
      },
      action: {
        publish: "Odayı oda dizininde yayınla",
        unpublish: "Odanın oda dizinindeki yayınını kaldır",
        publish_short: "Yayınla",
        unpublish_short: "Yayından kaldır",
        publish_success: "Oda başarıyla yayınlandı.",
        publish_failure: "Oda yayınlanırken hata oluştu.",
        unpublish_success: "Oda başarıyla yayından kaldırıldı.",
        unpublish_failure: "Oda yayından kaldırılırken hata oluştu.",
      },
    },
    destinations: {
      name: "Federasyon",
      fields: {
        destination: "Hedef",
        failure_ts: "Başarısızlık zamanı",
        retry_last_ts: "Son yeniden deneme zamanı",
        retry_interval: "Yeniden deneme aralığı",
        last_successful_stream_ordering: "Son başarılı akış",
        stream_ordering: "Akış",
      },
      action: {
        reconnect: "Yeniden bağlan",
      },
    },
    registration_tokens: {
      name: "Kayıt jetonu |||| Kayıt jetonları",
      fields: {
        token: "Jeton",
        valid: "Geçerli jeton",
        uses_allowed: "İzin verilen kullanımlar",
        pending: "Beklemede",
        completed: "Tamamlandı",
        expiry_time: "Son kullanma tarihi",
        length: "Uzunluk",
      },
      helper: { length: "Jeton için rastgele değer uzunluğu." },
    },
  },
};

export default tr;



