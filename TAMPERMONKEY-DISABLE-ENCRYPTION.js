// ==UserScript==
// @name         Element Web - Şifreleme Devre Dışı
// @namespace    http://localhost/
// @version      1.0
// @description  Element Web'de şifreleme toggle'ını tamamen gizler
// @author       Cravex
// @match        http://localhost:8080/*
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function() {
    'use strict';
    
    console.log('🔓 Şifreleme UI Gizleyici başlatıldı...');
    
    // CSS'i ekle
    const style = document.createElement('style');
    style.textContent = `
        /* ŞİFRELEME TOGGLE'INI GİZLE */
        .mx_Field:has(input[id*="enableEncryption"]),
        .mx_Checkbox:has(input[id*="enableEncryption"]),
        label:has(input[id*="enableEncryption"]),
        div:has(> input[id*="enableEncryption"]),
        [data-testid*="encryption"],
        .mx_CreateRoomDialog_e2ee,
        .mx_RoomSettingsDialog_e2ee {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        
        /* "Gelişmiş göster" linkini gizle */
        .mx_CreateRoomDialog_advanced,
        a[href="#advanced"] {
            display: none !important;
        }
        
        /* Encryption icon'ları gizle */
        .mx_E2EIcon,
        .mx_EventTile_e2eIcon,
        .mx_RoomSummaryCard_e2ee,
        svg[aria-label*="ncrypt"] {
            display: none !important;
        }
        
        /* Encryption warning mesajları */
        div:contains("can't disable this later"),
        div:contains("Bunu daha sonra devre dışı") {
            display: none !important;
        }
    `;
    
    // DOM yüklendikten sonra CSS ekle
    if (document.head) {
        document.head.appendChild(style);
    } else {
        document.addEventListener('DOMContentLoaded', function() {
            document.head.appendChild(style);
        });
    }
    
    // Mutation observer - dinamik elementler için
    const observer = new MutationObserver(function(mutations) {
        // Encryption checkbox'ı bul ve gizle
        const encryptionInputs = document.querySelectorAll('input[id*="enableEncryption"], input[id*="encryption"]');
        encryptionInputs.forEach(input => {
            // Input'u devre dışı bırak
            input.checked = false;
            input.disabled = true;
            
            // Parent elementleri gizle
            let parent = input.closest('.mx_Field, .mx_Checkbox, label, div');
            if (parent) {
                parent.style.display = 'none';
            }
        });
        
        // "Show advanced" linklerini gizle
        const advancedLinks = document.querySelectorAll('.mx_CreateRoomDialog_advanced, a[href="#advanced"]');
        advancedLinks.forEach(link => {
            link.style.display = 'none';
        });
    });
    
    // Observer'ı başlat
    observer.observe(document.documentElement, {
        childList: true,
        subtree: true
    });
    
    console.log('✅ Şifreleme UI gizleyici aktif!');
})();

