#!/usr/bin/env bash

# 键盘映射
# sudo grep "//    key <PAUS>" /usr/share/X11/xkb/symbols/pc || sudo sed '/^    key <PAUS> {/,/};/ s/.*/\/\/&/g' /usr/share/X11/xkb/symbols/pc
# sudo grep "//    key <PAUS>" /usr/share/X11/xkb/symbols/pc && sudo sed '/\/\/    key <PAUS>/i\    key <PAUS> {\t[  Insert\t\t]\t};' >/usr/share/X11/xkb/symbols/pc

# sudoers
sed 's/%sudo\tALL=(ALL:ALL) ALL/%sudo\tALL=(ALL:ALL) NOPASSWD:ALL/g' /etc/sudoers

# terminator
apt install terminator
echo '\
[global_config]
  title_hide_sizetext = True
  suppress_multiple_term_dialog = True
  title_font = Sans Bold 11
[keybindings]
  cycle_next = None
  cycle_prev = None
  go_next = <Alt>n
  go_prev = <Alt>b
  split_horiz = <Alt>bracketleft
  split_vert = <Alt>bracketright
  close_term = <Alt>w
  copy = <Primary><Shift>c
  close_window = <Primary><Alt>w
  move_tab_right = None
  move_tab_left = None
  toggle_zoom = None
  scaled_zoom = None
  next_tab = None
  prev_tab = None
  reset = None
  reset_clear = None
  hide_window = <Primary><Alt>q
  ungroup_all = None
  group_tab = None
  ungroup_tab = None
  insert_number = None
  insert_padded = None
  edit_window_title = None
  edit_tab_title = None
  edit_terminal_title = None
  help = None
[profiles]
  [[default]]
    background_darkness = 0.8
    background_type = transparent
    cursor_color = "#aaaaaa"
    font = Ubuntu Mono Bold 16
    show_titlebar = False
    use_system_font = False
[layouts]
  [[default]]
    [[[window0]]]
      type = Window
      parent = ""
    [[[child1]]]
      type = Terminal
      parent = window0
      profile = default
[plugins]
' >~/.config/terminator/config

# snap
sudo apt-get purge snapd -y

# sudo add-apt-repository multiverse
sudo add-apt-repository multiverse
sudo apt install -y ubuntu-restricted-extras

# nvidia
sudo apt install -y nvidia-driver-450

# rime

sudo apt install -y ibus-rime
echo '\
patch:
  switches:
  - name: ascii_mode
      reset: 0
      states: ["中文", "西文"]
  - name: full_shape
      states: ["半角", "全角"]
  - name: zh_simp
      reset: 1
      states: ["漢字", "汉字"]
  - name: ascii_punct
      states: ["。，", "．，"]
' >~/.config/ibus/rime/build/luna_pinyin.custom.yaml

echo '\
patch:
  "ascii_composer/switch_key/Shift_L": commit_code
  schema_list:
    - schema: luna_pinyin_simp
' >~/.config/ibus/rime/build/default.custom.yaml

sudo ibus-daemon -drx

# vscode
sudo apt clean all
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
sudo apt update
sudo proxychains4 apt install code -y

# 全局截图
sudo apt install -y flameshot

# chmod 600 *

# v2ray
alias curl="curl --proxy socks5://127.0.0.1:1080"
curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh -o ./tmp/install-release.sh
sudo bash -x ./tmp/install-release.sh
unalias curl


