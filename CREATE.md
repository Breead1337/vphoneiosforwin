# CREATE.md — как это делалось, что качали и как повторить

Полный лог проекта «iOS-гость на Windows x86-64 через эмулятор». Тут — цель и стратегия,
что именно скачали и откуда, как распаковали, как собрали машину и как её гонять, справка по
инструментам, что уже отреверсили и где стоим. Всё воспроизводимо с нуля на другой машине.

---

## 0. Цель и почему именно так

Хотим запустить iOS-гостя как в [vphone-cli](https://github.com/Lakr233/vphone) (Lakr233), но на
**Windows x86-64**. vphone поднимает iOS через **Virtualization.framework (VZ)** Apple — это
*аппаратная* виртуализация на Apple Silicon (гость исполняется нативно на ARM-железе). На x86 её нет
и быть не может, прямой порт невозможен.

Значит — **эмуляция ARM в софте**. Голый upstream QEMU Apple Silicon в TCG не тянет: нужны Apple-only
расширения (GXF/SPRR/PAC, кастомные sysreg'и, IOP/мейлбоксы). Всё это уже реализовано в форке **Inferno**
(ChefKiss) — там Apple-silicon машины (t8030 и т.п.) грузятся в TCG. Мы **не** берём готовую машину
Inferno: у Apple VZ своя платформа `vresearch101` (paravirtual, раскладка `vmapple`), поэтому пишем
СВОЮ машину поверх кода Inferno (каталог `overlay/`).

Итоговая цепочка: `AVPBooter` (ROM-загрузчик VZ) → SEP-хендшейк → iBoot → kernelcache iOS.

---

## 1. Что нужно поставить (инструменты)

| Инструмент | Зачем | Где взять |
|---|---|---|
| **WSL2 + Debian** | сборка и запуск QEMU (симлинки Inferno на NTFS битые — собирать ТОЛЬКО в WSL) | `wsl --install -d Debian` |
| **blacktop/ipsw** | скачивание/распаковка IPSW, расшифровка AEA, разбор IMG4/SEP/iBoot | https://github.com/blacktop/ipsw/releases (у нас `tools/ipsw.exe`) |
| **Ghidra 12.x** | реверс AVPBooter (headless через `tools/gh.sh`) | https://github.com/NationalSecurityAgency/ghidra/releases |
| **7-Zip** | читает APFS внутри `.dmg` (достать бинарники VZ из macOS) | https://www.7-zip.org |
| **Python 3 + capstone** | дизасм/трассировка (`tools/*.py`) | `pip install capstone` |
| **форк Inferno** | база QEMU с Apple TCG | клонировать в WSL: `~/inferno` (см. §4) |

Пакеты для сборки в Debian:
```bash
sudo apt install build-essential ninja-build meson python3-venv pkg-config \
  libglib2.0-dev libpixman-1-dev libslirp-dev zlib1g-dev libzstd-dev liblzo2-dev \
  libgtk-3-dev libsdl2-dev libnettle-dev libgnutls28-dev git
```

---

## 2. Раскладка на диске (референс: `D:\vphonewin`)

```
D:\vphonewin\
  NOTES.md            журнал вех
  fw\                 ПРОШИВКИ (не в git — качать самому, §3)
    cloudOS_26.4.ipsw
    cloud\            распакованный IPSW vresearch101 (iBoot/SEP/kernelcache/DeviceTree)
    macos\            macOS 26.6.2 installer .dmg + ext\ (распакованный)
    vz\               бинари VZ из macOS: AVPBooter.vresearch1.bin, AVPSEPBooter.vresearch1.bin,
                      com.apple.Virtualization.VirtualMachine (arm64e+x86_64 срезы)
  overlay\            НАШ код поверх Inferno (в git)
  re\                 реверс SEP + декомпил-выжимки (в git)
  tools\              скрипты (в git) + ipsw.exe/ghidra (НЕ в git)
  src\inferno\        клон Inferno на Windows — симлинки битые, НЕ собирать тут (не в git)
  ghidra\             проекты Ghidra (не в git — содержат декомпиляцию Apple)
  work\               сборки/логи (не в git)
```
В WSL клон Inferno лежит отдельно в `~/inferno` (см. §4) — из него и собираем.

---

## 3. Что качали и как распаковывали

### 3.1 cloudOS 26.4 IPSW — boot-цепочка `vresearch101`
Это прошивка виртуальной платформы Apple (Private Cloud Compute / research VM), в ней образы под
`vresearch101`. Скачать через ipsw и распаковать:
```bash
# найти/скачать нужный build IPSW (устройство vresearch101 / cloudOS)
tools/ipsw.exe download ...           # либо прямой URL -> tools/pget.py для параллельной качалки
# распаковать boot-цепочку и DeviceTree:
tools/ipsw.exe extract --kernel --dtree --iboot --sep  fw/cloudOS_26.4.ipsw -o fw/cloud
tools/ipsw.exe fw sep   fw/cloudOS_26.4.ipsw            # SEP firmware
tools/ipsw.exe fw iboot fw/cloudOS_26.4.ipsw            # iBoot/iBSS/SPTM/TXM
```
Внутри IPSW образы IMG4 могут быть в AEA — `ipsw` расшифровывает (`ipsw fw aea`, ключи из BuildManifest).
DeviceTree выгрузили в `fw/cloud/dt.txt` — из него взяли карту MMIO (см. §5).

### 3.2 macOS 26.6.2 — бинарники VZ
`AVPBooter` (ROM VZ) и фреймворк Virtualization лежат ВНУТРИ macOS, не в IPSW. Скачали installer
(`.dmg` / `InstallAssistant`), затем **7-Zip** читает APFS-том прямо из образа:
```
fw/macos/094-96884-092.dmg  ->  7z x  ->  fw/macos/ext/
```
Оттуда достали в `fw/vz/`:
- `AVPBooter.vresearch1.bin` — ROM-загрузчик для vresearch1 (наш `-bios`);
- `AVPSEPBooter.vresearch1.bin` — загрузчик SEP (нужен для BOOT_TZ0/IMG4);
- `com.apple.Virtualization.VirtualMachine` — бинарь VZ (реверс протоколов); из него вырезали
  срезы `VirtualMachine.arm64e` и `VirtualMachine.x86_64` (`ipsw macho ...` / lipo-подобно).

> Прошивки и эти бинари — **копирайт Apple**, в публичный git НЕ кладём. Каждый качает сам.

---

## 4. Inferno в WSL

```bash
# в WSL Debian:
git clone <fork-inferno-url> ~/inferno        # форк ChefKiss с Apple-silicon в TCG
cd ~/inferno
bash /mnt/d/vphonewin/tools/subm.sh           # подтянуть нужные submodule (кроме roms/)
```
`overlay/` накатывается поверх дерева Inferno скриптом сборки (§6). Клон на Windows (`src\inferno`)
держим только для чтения/грепа — на NTFS ломаются симлинки, собирать там нельзя.

---

## 5. Машина `vresearch101` — что известно про железо

Платформа `vresearch101` = раскладка **vmapple** из upstream QEMU (`hw/vmapple`) практически 1:1.
Взято из DeviceTree (`fw/cloud/dt.txt`) и реверса AVPBooter:

- **arm-io** база `0x10000000`; **GIC** `0x10000000`; **PL011 UART** `0x20010000`; **RAM** `0x70000000`.
- **AVPBooter** мапится по `0x100000`; гость стартует на **EL1** (без EL2/EL3), с GXF (GL1/GL2 через GENTER/GEXIT).
- Добавленные (сверх vmapple) узлы: **SEP-мейлбокс** `iop-sep,vpiop @0x30250000`, **avp-rtc** `@0x30240000`,
  **avp-ctrr** `@0x30260000`, **bdif** `@0x30000000`.
- Транспорт DFU AVPBooter/iBoot идёт через «virtio-usb» — свой транспорт VZ.

`overlay/hw/vmapple/vresearch101.c` строит эту машину, переиспользуя `bdif/cfg/aes/gfx` из vmapple;
`overlay/hw/vmapple/vr-sep-mbox.c` — модель SEP-мейлбокса (пока заготовка-ответчик).

---

## 6. Сборка и запуск (всё из PowerShell -> WSL)

> WSL звать из **PowerShell**, а не из Git-Bash (тот портит `/mnt`-пути).

```powershell
# собрать (накатывает overlay на ~/inferno и билдит qemu-system-aarch64):
wsl -d Debian -- bash /mnt/d/vphonewin/tools/build_inferno.sh

# запустить AVPBooter на N секунд (лог в ~/vrwork):
wsl -d Debian -- bash -lc "T=20 bash /mnt/d/vphonewin/tools/run1.sh"
```
`run1.sh` поднимает `-M vresearch101 -bios fw/vz/AVPBooter.vresearch1.bin` с двумя pflash
(`aux.img` 128M, `disk.img` 64G), UART в файл, `-d unimp,guest_errors`.

---

## 7. Справка по `tools/`

| Скрипт | Что делает |
|---|---|
| `build_inferno.sh` | накатить `overlay/` на `~/inferno` (с CRLF->LF) и собрать qemu |
| `run1.sh` | запуск гостя на `T` сек, UART+лог в `~/vrwork` (`D=` доп. `-d`, `EXTRA=` доп. флаги) |
| `trace.sh` | сборка + прогон с `-d exec` + анализ последних TB перед паникой (`tbstat.py`) |
| `mmio.sh` | прогон с трассировкой MMIO, сводка обращений по региону/оффсету |
| `before.sh PATTERN [N]` | N трасс-TB перед первой строкой лога по паттерну |
| `r.sh` / `rlong.sh` | поиск периода зацикливания в конце трассы / длинный прогон, счётчики SEP |
| `gh.sh import\|dec\|run` | Ghidra headless: импорт бинаря / декомпиляция адресов / запуск скрипта |
| `pget.py` / `pget.sh` | параллельная ranged-качалка больших файлов (IPSW/DMG) |
| `rzip.py` | список/извлечение членов удалённого zip по HTTP-range (без полной загрузки) |
| `armdis.py` | дизасм сырого arm64 (capstone) |
| `sysregs.py` | гистограмма msr/mrs/sys/GXF в сегментах Mach-O или сыром блобе |
| `tbstat.py` | разбор `-d exec` лога: последние TB, горячие TB, панк-адреса |
| `nettest.sh` | проверка доступности зеркал из WSL |
| `subm.sh` | инициализация нужных submodule Inferno (без `roms/`) |
| `ghidra_scripts/` | наши Ghidra-скрипты: `Decomp` (декомпиляция), `Xrefs`, `Callers`, `StrRefs`, `Const` |

---

## 8. Что уже отреверсили и где стоим

### Прогресс
- Машина `vresearch101` **собрана**, настоящий **AVPBooter Apple исполняется на x86** (TCG+GXF):
  проходит инициализацию GXF на EL1, читает конфиг, цепляется к bdif и упирается в **SEP-хендшейк**
  по мейлбоксу `@0x30250000`.
- **SEP-барьер #1 пройден**: формат SEP-сообщения раскрыт — LE u64 `{u8 ep; u8 tag; u8 op; u8 param; u32 data}`.
  Первый запрос `0x367ff` = ep `0xFF` (BOOTSTRAP), op `3` (GENERATE_NONCE).
- Полностью снят транспорт мейлбокса — регистры, объекты драйвера в RAM, кольцо, live-дампы:
  см. **[`re/SEP_MAILBOX.md`](re/SEP_MAILBOX.md)**.

### Карта регистров SEP (кратко, детали в SEP_MAILBOX.md)
- `0x200`=запрос AP->SEP; `0x100/0x108`=ответ SEP->AP (16 B); `0x1c/0x20`=статус (bit16=не готово);
  `0x10/0x14/0x18`=ранний хендшейк/doorbell.
- AP-драйвер: массив mailbox-объектов `@0x70028a30` (stride `0x1a0`), кольцо сообщений `@0x70028a00`.
- Send: `FUN_001063dc -> FUN_00106674 -> FUN_0010d450`; Recv (наш busy-wait): `FUN_0010d5c4`.

### Стратегический вывод
VZ-SEP-мейлбокс — **собственный паравиртуальный протокол Apple, НЕ RTKit**. AP-сторона (AVPBooter) —
C++/firebloom: сообщения = объекты с vtable в ROM, сериализация через vtable-вызов. Готовый SEP из
Inferno (`sep.c/sep-sim.c`, завязан на железный A7IOP/RTKit t8030) **не переиспользуется** — транспорт
другой. Значит SEP-хендшейк = реверс+реимплементация паравирт-протокола Apple с нуля, и это лишь ПЕРВЫЙ
барьер (дальше ядро, потом отсутствие графики — только soft-render).

### Текущий стоп
Заглушка-ответчик в `vr-sep-mbox.c` принимает op103 (GENERATE_NONCE), AVPBooter уходит в measured-boot
SHA (`FUN_0011b730` компрессия, `FUN_001399c0` финализация), но за 200 с реального времени хеш не
завершается и новых I/O нет = **runaway-цикл**: неверная длина/данные — нужен полный SEP-bootstrap
(nonce-данные + OOL SET_ADDR/SIZE + правильный порядок операций), а не latching-заглушки.

---

## 9. RESUME HERE — следующие шаги

1. **Реверс клиента SEP в AVPBooter**: что читается из ответа op103 и откуда берётся длина хешируемого
   региона (искать consumer `recv FUN_0010d5c4` и обработчик BOOTSTRAP).
2. Отдать корректные **nonce-данные** + обработать **CONTROL OOL SET_ADDR/SIZE**.
3. Операции **BOOT_TZ0(5)->105**, **BOOT_IMG4(6)->106** с отдачей образа (`AVPSEPBooter`/TZ0) в OOL-буфер.
4. Дальше — загрузка следующего образа с `bdif`, затем iBoot -> kernelcache.

Прогон цикла реверса:
```powershell
wsl -d Debian -- bash /mnt/d/vphonewin/tools/build_inferno.sh
wsl -d Debian -- bash -lc "T=8 bash /mnt/d/vphonewin/tools/trace.sh"   # либо run1/mmio
```
Лог — в `~/vrwork`. Оценка близости: до UI единицы %, feasibility доказана; до XNU-строк — недели,
до экрана — месяцы/фронтир.

---

## 10. Правовое

Только исследование совместимости (reverse engineering for interoperability). Прошивки, ROM и бинари
Apple в репозиторий **не входят** — участники получают их сами из легально скачанных IPSW/macOS.
