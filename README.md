SPR 2019度版
====

# branchを切ろう

### Overview
start_pkg:開始合図の認識

wait_and_turn_pkg:停止して、180度回る

requesting_an_operator_pkg:群衆認識、及び男女認識

the_riddle_game_pkg:リドルゲーム

Sound_source_localization_pkg:音源定位

## Requirement

RespeakerをSound_source_localization_pkgで使用します。
その際、Respeakerをudevで登録しないと使えません。
方法はRi-onewiki参照

[yamatomatsuda] (http://rione.org/protected/index.php?Member%2F15%E6%9C%9F%E7%94%9F%2F%E6%9D%BE%E7%94%B0%E5%A4%A7%E5%92%8C%2F%E9%96%8B%E7%99%BA%E6%97%A5%E8%AA%8C)

requesting_an_operator_pkgはopencvを使用します。etc内にopencvのversion3.1.1を入れてください。

## Usage
まずは

`roslaunch turtlebot_bringup minimal.launch`

次に

`roslaunch start_pkg spr.launch`

## Install

`git clone https://github.com/rionehome/spr.git`

`cd spr`

現状のヴァージョンはC_matsuブランチで

`git checkout C_matsu`

# 最後に

このブランチはデバグ中につき動作を保証しません