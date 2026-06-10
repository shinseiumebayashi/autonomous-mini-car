# 自律走行ミニカー 🚗

Raspberry Pi 4・OpenCV・各種センサーを使って、自律走行できる小型ロボットカーをゼロから自作する個人プロジェクト。組み込みシステム、コンピュータビジョン、ソフトウェア設計のスキルを示すために制作。

> [English README](README.md)

## デモ

> 📹 デモ動画準備中

## 概要

ハードウェア組み立てからコンピュータビジョン、PID制御までフルスタックでロボットカーを構築するプロジェクト。差動駆動ではなく**後輪駆動 + 前輪操舵（アッカーマン式）**の構造を採用しているため、より自動車に近い動きを実現。

### 特徴

- 🎮 キーボード操作での走行（WASD）
- 📏 超音波センサーによる距離計測（HC-SR04）
- 📷 カメラによる画像取得（Pi Camera V2）
- ⚙️ PWMによるモーター・サーボ制御
- 🧱 クラス設計による再利用可能なモジュール構成

## 技術スタック

| カテゴリ | 内容 |
|--------|------|
| ハードウェア | Raspberry Pi 4 (2GB)、L298Nモータードライバ、MG90Sサーボ、HC-SR04超音波、Pi Camera V2 |
| ソフトウェア | Python 3.13、OpenCV 4.13、NumPy、RPi.GPIO、picamera2 |
| 制御 | PWMモーター制御、アッカーマン操舵 |
| ツール | VSCode + Remote-SSH、Git/GitHub |

## ロードマップ

- [x] **Phase 1**: 環境構築
- [x] **Phase 2**: 各パーツの単独動作確認
- [x] **Phase 3**: 車体組み立てとキーボード操縦
- [x] **Phase 4**: 超音波センサーによる障害物回避
- [x] **Phase 5**: OpenCV + PID制御でライントレース
- [ ] **Phase 6**: 統合とデモ動画

## プロジェクト構成

​```
autonomous-mini-car/
├── src/                    # ハードウェア抽象化モジュール
│   ├── config.py          # GPIOピン設定
│   ├── motor.py           # MotorController クラス
│   ├── servo.py           # ServoController クラス
│   ├── ultrasonic.py      # UltrasonicSensor クラス
│   └── camera.py          # Camera クラス
├── apps/                   # 実行可能アプリ
│   └── keyboard_drive.py  # キーボード操縦
├── tests/                  # 単体テスト
└── docs/                   # ドキュメント
​```

## 配線

| 部品 | GPIO (BCM) | 備考 |
|------|-----------|------|
| L298N ENA | 25 | 左モーター PWM |
| L298N IN1/IN2 | 17/27 | 左モーター方向 |
| L298N ENB | 6 | 右モーター PWM |
| L298N IN3/IN4 | 22/5 | 右モーター方向 |
| MG90Sサーボ | 21 | 前輪操舵 |
| HC-SR04 Trig | 23 | 超音波トリガ |
| HC-SR04 Echo | 24 | 1kΩ+2kΩの分圧経由 |

モーターは18650電池×2本（7.4V）→ L298N で給電。Pi本体は別電源（USB-C）。

## セットアップ

​```bash
git clone https://github.com/shinseiumebayashi/autonomous-mini-car.git
cd autonomous-mini-car

python3 -m venv --system-site-packages venv
source venv/bin/activate

pip install -r requirements.txt
​```

## 使い方

​```bash
# 各パーツの単独テスト
python3 tests/test_motor.py
python3 tests/test_servo.py
python3 tests/test_ultrasonic.py
python3 tests/test_camera.py

# キーボード操縦
python3 apps/keyboard_drive.py
​```

### キーボード操作

| キー | 動作 |
|------|------|
| W | 前進 |
| S | 後進 |
| A | 左操舵 |
| D | 右操舵 |
| X | モーター停止 |
| Z | 操舵中央 |
| Q | 終了 |

## 学んだこと

- マイクロ秒精度のGPIO制御（超音波センサーのタイミング処理）
- PWM信号生成によるモーター速度・サーボ角度の制御
- 電源系の分離（ロジック5V vs モーター7.4V）の重要性
- クラスベース設計でアプリケーションロジックとハードウェア詳細を分離
- アッカーマン操舵と差動駆動のトレードオフ

## ライセンス

MIT — LICENSE 参照。