SPR 2019JapanOpen版
====
### Overview
start:開始合図の認識

person_recognition:開始から人間検出まで行うノード

speech_recognition:リドルゲームから音源定位まで行うノード

## Requirement
RespeakerをSound_source_localization_pkgで使用します。
その際、Respeakerをudevで登録しないと使えません。
方法はRi-onewiki参照

[yamatomatsuda] (http://rione.org/protected/index.php?Member%2F15%E6%9C%9F%E7%94%9F%2F%E6%9D%BE%E7%94%B0%E5%A4%A7%E5%92%8C%2F%E9%96%8B%E7%99%BA%E6%97%A5%E8%AA%8C)

requesting_an_operator_pkgはopencvを使用します。etc内にopencvのversion3.1.1を入れてください。

# REQUIREMNT 追記

Ri-oneドライブからよっしー先輩の画像モデルをダウンロードして、その中のフォルダmale,femaleをrequesting_an_operator_pkgのimagesに入れてください。


## Usage
実装中

## Install

`git clone https://github.com/rionehome/spr.git`