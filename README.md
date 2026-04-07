# Kafka Streaming Setup – Einführung

Dieses Projekt stellt einen einfachen Streaming-Workflow für Kreditkartentransaktionen bereit.
Ein **Producer** sendet Transaktionen als Stream in Kafka, ein **Consumer (Receiver)** liest diese Daten und verarbeitet sie weiter (z. B. für ML-Modelle).

---

## 🧩 Komponenten

### 1. Producer (`producer_stream.py`)

* Liest den Datensatz (Kaggle Credit Card Fraud)
* Sortiert nach `Time`
* Sendet Events in Echtzeit (oder beschleunigt) an Kafka
* Topic: `transactions_raw`

### 2. Consumer (`consumer_test.py`)

* Liest Events aus Kafka
* Gibt sie strukturiert aus
* Kann später für ML-Modelle erweitert werden

---

## ⚙️ Voraussetzungen

* Python 3.x
* Docker + Docker Desktop (laufend)
* Installierte Python Packages:

```bash
pip install kafka-python pandas kagglehub scikit-learn
```

---

## 🚀 Kafka starten

Im Projektordner:

```bash
docker compose up -d
```

Überprüfen:

```bash
docker ps
```

Es sollten laufen:

* `kafka`
* `zookeeper`

---

## ▶️ Stream starten

### Schritt 1: Consumer starten

```bash
python consumer_test.py
```

Der Consumer wartet nun auf eingehende Events.

---

### Schritt 2: Producer starten (in neuem Terminal)

```bash
python producer_stream.py
```

---

## 📡 Datenfluss

```text
Dataset → Producer → Kafka (Topic: transactions_raw) → Consumer
```

---

## 📦 Event-Format

Jedes Event enthält:

```json
{
  "event_id": int,
  "event_time": float,
  "event_time_real": "ISO timestamp",
  "amount": float,
  "features": [V1–V28],
  "label": 0/1
}
```

---

## 🧠 Hinweise

* Events werden in **zeitlicher Reihenfolge** gesendet
* Delay basiert auf der `Time`-Spalte (event-time replay)
* `event_time_real` dient für spätere Streaming-Analysen

---

## 🔄 Topic zurücksetzen (optional)

Falls alte Daten stören:

```bash
docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --delete --topic transactions_raw
```

---

## 📌 Ziel

* Demonstration eines echten Datenstreams
* Grundlage für ML-Anwendungen (z. B. Fraud Detection)
* Erweiterbar um Modelle im Consumer

---

Bei Fragen einfach melden 🙂
