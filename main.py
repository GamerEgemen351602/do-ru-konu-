import random
import os
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr

recognizer = sr.Recognizer()

# Tüm kelimeler (Karışık Mod)
words = {
    "elma": "apple",
    "kitap": "book",
    "kedi": "cat",
    "köpek": "dog",
    "su": "water",

    "bilgisayar": "computer",
    "telefon": "phone",
    "öğretmen": "teacher",
    "araba": "car",
    "deneyim": "experience",

    "üniversite": "university",
    "geliştirici": "developer",
    "mühendis": "engineer",
    "sorumluluk": "responsibility",
    "albay": "colonel"
}

print("=" * 40)
print("🎤 DOĞRU KONUŞ OYUNU")
print("=" * 40)
print("Karışık Mod Başlıyor!")
print(f"Toplam {len(words)} kelime var.")
input("\nBaşlamak için Enter'a bas...")

kelimeler = list(words.items())
random.shuffle(kelimeler)

puan = 0
hata = 0
can = 3

fs = 44100
sure = 4

while can > 0 and len(kelimeler) > 0:

    turkce, ingilizce = kelimeler.pop()

    print("\n" + "-" * 40)
    print("Türkçe Kelime:", turkce)
    input("Hazırsan Enter'a bas ve İngilizcesini söyle...")

    print("🎤 Kayıt yapılıyor...")

    recording = sd.rec(
        int(fs * sure),
        samplerate=fs,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    wav.write("record.wav", fs, recording)

    with sr.AudioFile("record.wav") as source:
        audio = recognizer.record(source)

    try:
        recognized = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        recognized = recognized.lower().strip()

        print("Sen söyledin :", recognized)
        print("Doğru cevap  :", ingilizce)

        if recognized == ingilizce.lower():
            print("✅ DOĞRU!")
            puan += 10
        else:
            print("❌ YANLIŞ!")
            hata += 1
            can -= 1

    except sr.UnknownValueError:
        print("❌ Ses anlaşılamadı.")
        hata += 1
        can -= 1

    except sr.RequestError:
        print("❌ İnternet bağlantısı hatası.")
        break

    print("\nDurum")
    print("Puan :", puan)
    print("Hata :", hata)
    print("Can  :", can)
    print("Kalan Kelime :", len(kelimeler))

print("\n" + "=" * 40)
print("🎮 OYUN BİTTİ")
print("=" * 40)

print("Toplam Puan :", puan)
print("Toplam Hata :", hata)

if puan >= 100:
    print("🏆 Mükemmel!")
elif puan >= 50:
    print("👏 Güzel iş!")
else:
    print("📚 Biraz daha pratik yap!")

if os.path.exists("record.wav"):
    os.remove("record.wav")