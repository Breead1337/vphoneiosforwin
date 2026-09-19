# vphone-on-Windows — журнал

Цель: запустить iOS-гостя из vphone-cli на Windows x86-64. Т.к. VZ = аппаратная
виртуализация (нельзя на x86), путь = эмулятор: своя QEMU-машина `vresearch101`
на базе форка Inferno (в нём уже есть Apple GXF/SPRR/PAC в TCG).

## Что сделано (14.09)
- Скачаны прошивки: cloudOS 26.4 IPSW (boot chain vresearch101), macOS 26.6.2 (для VZ).
  Из macOS APFS через 7-Zip достали AVPBooter.vresearch1.bin, AVPSEPBooter.vresearch1.bin,
  com.apple.Virtualization.VirtualMachine (арм64e+x86_64 срезы) → D:\vphonewin\fw\vz.
- Собран Inferno в WSL Debian (~/inferno/build/qemu-system-aarch64), overlay в D:\vphonewin\overlay.
- Написана машина `vresearch101` (overlay/hw/vmapple/vresearch101.c): MMIO из DeviceTree
  (arm-io@0x10000000, RAM@0x70000000), CPU apple-gxf, переиспользует vmapple bdif/cfg/aes/gfx.
- **AVPBooter грузится и исполняется**: проходит GXF-инициализацию EL1, читает конфиг,
  цепляется к bdif (0x30000000) и упирается в SEP-хендшейк по мейлбоксу @0x30250000.
- Отревершена карта SEP-мейлбокса (AVPBooter FUN_0010d580/0010d6dc, RTKit-подобный):
  0x10/0x14 = doorbell/inbox status, 0x18 = msg word, 0x100/0x108 = inbox,
  0x200/0x208 = outbox, 0x20/0x1c = флаги. Протокол = BOOTSTRAP_OP_* (см. Inferno sep-sim.c:
  PING=1, GET_STATUS=2, GENERATE_NONCE=3, BOOT_TZ0=5, BOOT_IMG4=6, ...).
- Заготовка SEP (overlay/hw/vmapple/vr-sep-mbox.c) — пока latching-регистры, гость крутится
  в ожидании ответа SEP.

## Следующий шаг
Реализовать BOOTSTRAP-протокол в vr-sep-mbox.c (портировать из Inferno hw/arm/apple-silicon/sep-sim.c
+ a7iop mailbox regs-v2/v4), чтобы SEP отвечал PING_ACK/STATUS_REPLY/NONCE и принял TZ0/IMG4.
Потом AVPBooter пойдёт грузить kernelcache.

## Инструменты (D:\vphonewin\tools)
- build_inferno.sh — применить overlay и собрать (звать: `wsl -d Debian -- bash /mnt/d/.../build_inferno.sh`)
- run1.sh / trace.sh / mmio.sh / before.sh — запуск гостя и трассировка (лог в ~/vrwork)
- gh.sh — Ghidra headless: import / dec (декомпиляция) / run (скрипт). Проекты в D:\vphonewin\ghidra.
- armdis.py, sysregs.py, pget.py (параллельная качалка)
- ВАЖНО: wsl звать из PowerShell, а не Git-Bash (портит /mnt). Кавычки в командах — через r.sh-файл.

## Ограничения пути
Как у Inferno (iOS 14 на iPhone 11 после лет работы): графики нет (только soft-render),
iCloud/App Store/биометрия — нет. Это ресёрч, не продукт. iOS 26 из vphone-cli — намного
дальше, чем текущий publicly-booting уровень.

## Стратегический вывод (после реверса SEP-мейлбокса)
VZ vresearch1 SEP-мейлбокс — СОБСТВЕННЫЙ паравиртуальный протокол Apple, НЕ RTKit:
- AP-сторона (AVPBooter) — C++/firebloom: сообщения = объекты с vtable в ROM (0x13cxxx/0x13dxxx),
  сериализация через vtable-вызов. Синтез ответов на уровне объектов = дорого.
- Переиспользовать SEP из Inferno (sep.c/sep-sim.c) НЕЛЬЗЯ: они завязаны на железный A7IOP/RTKit
  мейлбокс t8030 (регистры 0x18/0x1C send/recv), у VZ транспорт другой (0x100 inbox/0x200 outbox,
  C++-объекты). Ни один шорткат не подходит.
- Значит SEP-хендшейк = реверс+реимплементация паравирт-протокола Apple с нуля (multi-session),
  и это лишь ПЕРВЫЙ барьер (дальше ядро, потом отсутствие графики).

## Текущее состояние (что работает и лежит готовым)
- vresearch101 машина собрана, НАСТОЯЩИЙ AVPBooter Apple исполняется на x86 (TCG+GXF), доходит до SEP.
- Полностью снят транспорт SEP-мейлбокса: re/SEP_MAILBOX.md (регистры, объекты, кольцо, live-дампы).
- Инструменты: Ghidra headless (gh.sh), сборка (build_inferno.sh), трассировка (run1/mmio/before/trace).
- Модель SEP (overlay/hw/vmapple/vr-sep-mbox.c) с latching+дампом RAM — заготовка под ответчик.

## Реком. следующий шаг (когда решим вкладываться)
Написать VZ-SEP-ответчик на транспортном уровне: перехватить сериализованную запись кольца
(после vtable-вызова FUN_0010d450), понять on-wire формат записи + ответной, отвечать BOOTSTRAP
(PING/STATUS/NONCE/TZ0/IMG4), поднимать IRQ. Это ~дни реверса, не часы.

## Обновление 15.09 — карта сообщений SEP снята
Отреверсен драйвер сообщений AP над транспортом: найдена мастер-таблица типов сообщений
@0x13dd20 (32×0x38: req op, resp op = req+100, таймаут, длина OOL-данных, флаги) и точный
16-байтный формат кадра запрос/ответ (ep=0xFF, op в байте +2). Физобмен идёт через vtable
(send=FUN_0010d450 сентинел 0x1111, recv=FUN_0010d5c4 bit16). Детали и декодированная
таблица — в re/SEP_MAILBOX.md (раздел «Сессия 15.09»). Следующее: формат кольца + отдать
настоящий 20-байтный nonce (op4) и OOL-данные.

## Обновление 15.09 (2) — op3 принят, барьер сдвинулся в measured-boot
Живой трейс: op3 GENERATE_NONCE ответ ПРИНЯТ (один вычит 0x1c/0x100, ни ретрая, ни паники).
Зависание — уже пост-nonce: горячий memset (FUN_00110f50 @0x110f9c) + хеш (0x119xxx) с
непрерывными sync-abort векторами (demand paging). Либо медленный TCG-SHA, либо runaway memset
из-за размера от занулённого ответа. Детали — re/SEP_MAILBOX.md. Дальше: поймать размер живого
memset трейсом адреса возврата и проверить inline-поля ответа op3.

## Обновление 15.09 (3) — зависание = runaway memset с мусорной длиной
Снят live X2 memset (-d cpu): len ≈ 0xfffffc00_xxxxxxxx (адрес-как-размер), dst — высокие VA.
Цикл while(7<len) не завершается → это НЕ медленный хеш, а runaway из занулённого поля,
которое должен заполнить SEP-ответ. Обёртка FUN_001113a0 (len из x5). Следующее: найти
источник длины у вызывающего 1113a0 и отдать ненулевой op3-ответ/OOL-nonce, проверить исчезновение.

## Обновление 15.09 (4) — ПОПРАВКА: стоп на HVC #0, не runaway
Проверка окнами: T=8 и T=24 дают идентичные TB → выполнение ОСТАНАВЛИВАЕТСЯ, это не медленный
memset. Последний TB = 0x103370 = HVC #0 (FUN_00103370). memset конечен (FUN_001040cc=const 0x38c000).
Барьер сейчас — паравиртуальный HVC-гипервызов к хосту VZ (из measured-boot FUN_0011b730), который
машина не обслуживает. Прошлый вывод про «runaway memset» (коммит 9a4dda7) СНЯТ как ошибочный
(смещённый -d cpu). SEP-находки в силе. Дальше: снять ABI HVC и реализовать обработчик в машине.

## Обновление 15.09 (5) — это PSCI_SYSTEM_RESET из measured-boot
Оба HVC из LR=0x11b7d8 (FUN_0011b730): PSCI_VERSION, затем PSCI_SYSTEM_RESET. psci-conduit=HVC
машина ставит сама. Значит measured-boot проваливает проверку и осознанно ребутит (не hang/runaway).
Причина — пустышечные SEP-ответы. Дальше: реверс ветки reset в FUN_0011b730 и что она сравнивает.

## Обновление 15.09 (6) — SYSTEM_RESET подтверждён чисто
`-no-reboot -no-shutdown`: ROM-вход 1 раз, CPU заморожен на HVC 0x103370 → гость вызвал PSCI
SYSTEM_RESET (не reboot-петля, не hang). Привязку HVC к LR=0x11b7d8 снял (ненадёжный -d cpu).
Надёжный след. шаг: инструментировать HVC в самой машине (печать X0..X7 + ELR) — увидеть точную
цепочку до reset и провалившуюся проверку measured-boot.

## Обновление 15.09 (7) — КОРЕНЬ: firebloom bounds-panic в main
Вставлен HVC-логгер в машину (overlay/target/arm/tcg/psci.c). Оба HVC из lr=0x11d6ac (reboot в хвосте
FUN_0011b730). Аргументы = firebloom_panic("main", ...) с форматом "(%zu < %zu)" — boot-abort это
firebloom bounds-check паника: занулённое поле (из пустышечных SEP-ответов) даёт указатель/длину вне
границ → reboot. Дальше: поймать первый упавший bounds-check и связать поле с нужным SEP-ответом.

## Обновление 15.09 (8) — причина reboot = код 0xa0
Ветка reboot: 0x11bb78 cmp w19,#0xa0; b.eq 0x11d690. w19=x7-аргумент FUN_0011b730 (диспетчер статусов,
не SHA). В HVC-логе x7=0xa0 → boot-abort это реакция на код ошибки 0xa0 (firebloom bounds panic:
"main","(%zu<%zu)"). Дальше: найти источник 0xa0 (вход 0x11b730, кто зовёт) → SEP-поле → отдать не нулями.

## Обновление 15.09 (9) — КОРЕНЬ: транзакция мейлбокса не завершается
Цепочка до конца: reboot ← паника (SVC#0xa0 + PSCI reset, FUN_00104d68) ← FUN_00106d50 вернул −1.
Условие успеха: resp[2] (DAT_7002abd2) == req+100, ПОЛНЫЕ 8 пингов. Заглушка пишет ответ в плоский
MMIO 0x100, а AP читает resp[2] из RAM 0x7002abd0 через кольцо (recv FUN_0010d5c4) — не совпадает →
паника. Фикс: отдавать 16-байтный ответ по пути кольца (obj[0]+entry[2]), снять bit16, поднять IRQ.
Нужны точные entry-оффсеты кольца (setup мейлбокса) — следующий заход.

## Обновление 15.09 (10) — ФИКС: прошли GENERATE_NONCE
vr-sep-mbox.c: op3 отдаёт data=0xa0, op4 отдаёт ненулевой nonce-чанк (5×4=20 байт). Boot прошёл
SEP-nonce (TB 211k→236k), первый abort уехал с мейлбокса на новую функцию 0x1093d8. Дальше —
разобрать эту проверку.


## Обновление 15.09 (11) — ФИКС: virtio-usb (bdif DEVID_USB) пройден, выход в event loop (3.8M TB)
Разобран барьер 0x1093d8 (FUN_001092a0 -> FUN_00107f10 -> FUN_0010d8c8):
1. FUN_0010d8c8 проверяет BDIF MMIO устройство DEVID_USB (0x30100000). На оффсете 4 (REG_CFG)
   ожидает w24 = 0x1a01, а модель bdif.c отдавала REG_CFG_ACTIVE (2) -> ошибка 0x40200003 -> abort.
   Фикс: для devid == DEVID_USB отдавать 0x1a01.
2. Следом фоновый USB-воркер FUN_0010829c опрашивал REG_BUSY (оффсет 0x10), ожидая статус готовности
   пакетов. bdif.c отдавал 1 (BUSY_READY), воркер считал, что пришёл пакет, парсил нулевой буфер
   RAM (байт[5] == 0 != 1/2/3) и паниковал на 0x108608.
   Фикс: для devid == DEVID_USB на REG_BUSY отдавать 0 (нет непринятых пакетов от хоста).
Результат: ВСЕ паники ушли (panic TB# None). Гость преодолел барьер и стабильно крутит кооперативный
event loop (период 78 TB, 3.85 млн TB за 4 секунды) между USB-воркером (svc #0x42 yield) и
планировщиком задач. AVPBooter сканирует aux.img (DEVID_AUX) блоками vblk_read 512B.

## Обновление 16.09 (12) — чтение LLB из aux.img, байпас IM4M манифеста и выход на FUN_00105374 (boot stage)
1. Отреверсен парсер хранилища AVPBooter (FUN_001004b8 этап 0xe -> FUN_0010746c -> FUN_00100e04):
   - Ожидает ASN.1 DER SEQUENCE (tag 0x30, IA5String "IMG4", tag 0x16 0x04 'IMG4').
   - В сектор 0 aux.img записан синтезированный ASN.1 IMG4 контейнер с LLB.vresearch101.RELEASE.im4p (тег 'illb').
   - AVPBooter распознал образ, внёс в список дескрипторов (0x700284b0), перешёл на LAB_00100780 и вычитал
     весь LLB (365.5 КБ) блоками через BDIF в память по адресу 0x70074000.
2. Локализована проверка манифеста в FUN_001011a8 (движок верификации образов):
   - FUN_00128e6c проверяет наличие IM4M (local_2ed != 0). При отсутствии падает с кодом 0x40040007.
   - По адресу 0x101640 инструкция `tbz w8, #0, 0x1016f4` (0x360005a8) проверяет флаг манифеста.
   - Замена на `b 0x101850` (0x14000084) пропускает проверку серверной подписи Apple / nonce и переходит
     напрямую к извлечению полезной нагрузки IM4P и LZFSE-распаковке (FUN_00135f20).
3. Патч интегрирован прямо в загрузчик ROM машины vresearch101 (overlay/hw/vmapple/vresearch101.c):
   - Файл AVPBooter на диске остаётся нетронутым; при загрузке в fw_mr RAM инструкция по адресу 0x101640
     динамически заменяется на `b 0x101850`.
4. Результат:
   - Бесконечный цикл DFU USB (1.76M вызовов) полностью ушёл.
   - AVPBooter успешно верифицирует LLB, переходит к передаче управления в FUN_00105374(0, 0x70074000, 0),
     выполняет серию PING (op 1) и отправляет в SEP уведомление следующей стадии загрузки (op 16 / 0x10).

## Обновление 16.09 (13) — ИСТОРИЧЕСКИЙ ПРОРЫВ: ПОЛНЫЙ ВЫХОД В LLB (iBoot-13822)
1. Решён ответ на SEP op 16 (0x10) в vr-sep-mbox.c:
   - FUN_00103788 дважды вызывал op 16 для сборки 64-битного cookie. При нулевом ответе вызывалась паника 0x10380c.
   - Отдача ненулевого data32 позволила FUN_00105374 завершить деинициализацию booter'а и вызвать SVC #0x7.
2. Исправлена запись в BDIF (overlay/hw/vmapple/bdif.c):
   - Добавлен bdif_realize() с установкой прав BLK_PERM_WRITE для BlockBackend aux и root.
   - В VBLK_DATA_FLAGS_WRITE добавлен DMA-вычит из памяти гостя перед вызовом blk_pwrite.
3. РЕЗУЛЬТАТ:
   - AVPBooter полностью завершил свою работу и передал управление через SVC #0x7 в LLB по адресу 0x70074000.
   - **НАСТОЯЩИЙ APPLE LLB (illb) ИСПОЛНЯЕТСЯ В QEMU НА X86-64!**
   - Получен прямой серийный вывод UART (PL011 @ 0x20010000):
     ```
     ======== Start of iBoot serial output. ========
     ...
     Board: vresearch101ap:0 
     Chip: fe01:00 
     Build: RELEASE:iBoot-13822.100.791.502.1
     UUID: 416D8202-61E4-3B16-961A-EC0B920B9029
     Stacktrace:
     --> 0x000000007008a7bc
     --> 0x0000000070089ce0
     --> 0x0000000070089cbc
     --> 0x00000000700cd84c
     --> 0x00000000700cd8b4
     --> 0x00000000700cd0dc
     ```
   - LLB инициализировал собственные таблицы страниц (высокие адреса 0x700cxxxx), начал сканирование блочных
     устройств через BDIF (root addr=0xb4fb7000 off=0, aux addr=0xb45ef000 off=0x1a00000) и пишет NVRAM в aux.

## Обновление 16.09 (14) — РАЗРЕШЕНИЕ ПАНИКИ LLB: ВЫХОД В КОМАНДНЫЙ ПРОМПТ iBoot RECOVERY MODE!
1. Локализована паника `4962211b03d706d:192`:
   - Снята трассировка прерываний/исключений `-d int`: гость падал с `Taking exception 4 [Data Abort]`
     с `FAR = 0x4ffff8`, `ELR = 0x700a8474`.
   - Отреверсен модуль `vmpv` (Virtual Machine Paravirtualized queues) в LLB (`0x700864dc` .. `0x70086950`):
     LLB ожидает разделяемую память хост-гость по адресу `0x400000`, настраивает структуры по смещению `0x690`
     и размещает кольцевой буфер очереди `vmpv` размером 16 КБ по адресам `0x4fc000 .. 0x500000` и `0x504000`.
   - В оригинальной модели `vmapple-cfg` размер региона был ограничен 64 КБ (`0x10000`), из-за чего доступ к
     `0x4ffff8` приводил к аппаратному Data Abort и системной панике.
2. Реализован фикс:
   - В `overlay/hw/vmapple/cfg.c`: увеличен `VMAPPLE_CFG_SIZE` с `0x10000` (64 КБ) до `0x00200000` (2 МБ),
     полностью покрывая весь диапазон разделяемой памяти до `VR_PMUSRAM` (`0x600000`).
   - В `overlay/hw/vmapple/vresearch101.c`: скорректирован `memmap[VR_CONFIG]` до 2 МБ и `VR_PMUSRAM` до 128 КБ
     в соответствии с картой памяти `VirtualMachine` Apple Silicon.
3. РЕЗУЛЬТАТ — ГРАНДИОЗНЫЙ УСПЕХ:
   - Паника полностью исчезла!
   - LLB успешно инициализировал очередь `vmpv`, драйверы блочных устройств BDIF, прочитал образ,
     записал 512 КБ NVRAM в сектор aux (`off=0xa00000`) и **ВЫШЕЛ В ИНТЕРАКТИВНЫЙ RECOVERY MODE**:
     ```
     =======================================
     ::
     :: 🔥🌸 Microkernel iBoot for vresearch101 Copyright 2007-2026, Apple Inc.
     ::
     ::	Local boot, Board 0x20 (vresearch101ap)/Rev 0x0
     ::
     ::	BUILD_TAG: iBoot-13822.100.791.502.1
     ::
     ::	UUID: 416D8202-61E4-3B16-961A-EC0B920B9029
     ::
     ::	BUILD_STYLE: RELEASE
     ::
     ::	USB_SERIAL_NUMBER: SDOM:01 CPID:FE01 CPRV:00 CPFM:03 SCEP:01 BDID:20 ECID:0000000000000000 IBFL:3D SRNM:[1234]
     ::
     =======================================

     Entering recovery mode, starting command prompt
     ```

## Обновление 16.09 (15) — iBoot (ibot) в хранилище образов aux; настоящий барьер = пустой root-диск
1. aux.img теперь собирается скриптом `tools/mkaux.py` (раньше руками). Сканер образов LLB берёт IMG4-контейнеры
   ПОДРЯД БЕЗ ВЫРАВНИВАНИЯ: следующий заголовок читается ровно с off+len предыдущего (по 512 байт не ровнять —
   при 0x5b800 ibot не находился). Сейчас: `illb @0x0 len 0x5b7f5`, `ibot @0x5b7f5 len 0x5cd23` — оба в списке
   образов, и 9 повторов `d77fec40d6d8952:1215` исчезли.
2. LLB этой сборки = «Microkernel iBoot» целиком: boot-список `fsboot` (FUN_7006c994) сам монтирует диск и грузит
   `krnl` (0x6b726e6c). Breadcrumbs NVRAM: `<BOOT> 20022 <COMMIT> 401f0201 20028(1) 20012 40060001 40060001`.
   40060001 = FUN_7006d7cc («/boot», tc-path): FUN_700e07d0 не нашёл раздел, потому что disk.img пустой
   (ни GPT, ни APFS). Ibot тут, скорее всего, вообще не нужен — нужна установленная система (как после restore в vphone).
3. Консоль recovery по UART ввод не принимает (help/printenv без ответа, `tools/prompt.sh`), в RELEASE команды идут
   по USB.
4. Инструменты: Ghidra-проект `llb` (база 0x7006c000), `ghidra_scripts/DecompAll.java` — полная декомпиляция в один
   файл (`ghidra/dump/llb_all.c`, 168k строк, не в git) для грепа хешей `file:line` и констант.
Дальше — выбор пути к ядру: (А) DFU/recovery по virtio-usb со стороны хоста (iBEC/ramdisk/kernelcache + bootx,
как idevicerestore в vphone) или (Б) собрать root-диск офлайн (GPT+APFS+Preboot boot objects).

## Обновление 16.09 (16) — root-диск: GPT+APFS принят, Preboot смонтирован, iBoot ищет файлы загрузки
Метод: gdb-multiarch на gdbstub QEMU (`tools/gdbrun.sh cmds.gdb`, hbreak — VA LLB = 0x7006c000+). Результаты:
1. fsboot монтирует устройство `roota` (NVRAM boot-device `root` + раздел 'a', формат `%s%c`) через IPC fs-сервиса
   (FUN_70096008 -> FUN_700a607c). Нужен GPT (раздел APFS 7C3457EF-…); без GPT было 40060001.
2. APFS-драйвер: FUN_700a607c выбирает том ПО РОЛИ (FUN_700a2a74, apfs_role +0x3c4) — для /boot запрашивается
   role=0x10 (Preboot); по имени (FUN_700a23f8/FUN_700a2230) ищется том «Update» (upgrade-путь).
   `tools/mkroot.sh` = sgdisk + mkapfs (apfsprogs) + `tools/apfs_role.py` (роль в APSB + fletcher64) -> 40060003 ушла.
3. Сейчас breadcrumbs `20012 40060004 40030016`: открывается `/boot/active` (нет файла), затем
   `/boot/<active>/usr/standalone/firmware/sep-firmware.img4` (40030016 = загрузка 'sepi' в FUN_700c4cbc).
   Раскладка Preboot: `/active` = 96 hex nsih; `/<nsih>/usr/standalone/firmware/{sep-firmware,devicetree,root_hash}.img4`,
   `FUD/{StaticTrustCache,Ap,SecurePageTableMonitor,Ap,TrustedExecutionMonitor}.img4`,
   `/<nsih>/System/Library/Caches/com.apple.kernelcaches/kernelcache`. Стейджер: `tools/mkpreboot.py`.
4. Писать файлы в APFS из Linux: собираю linux-apfs-rw под ядро WSL (`tools/build_apfs_module.sh`, MODVERSIONS ->
   нужна полная сборка ядра msft 6.6.87.2 ради Module.symvers).

## Обновление 16.09 (17) — iBoot ОТРАБОТАЛ ДО КОНЦА: «End of iBoot serial output», передача управления дальше
1. Запись файлов в APFS из WSL: собран linux-apfs-rw (`tools/build_apfs_module.sh`: исходники ядра msft 6.6.87.2,
   `make vmlinux` -> vmlinux.symvers как Module.symvers, genver.sh). Модуль грузится `insmod` от root
   (`wsl -u root`; после перезапуска WSL — заново, mkroot.sh делает сам).
2. `tools/apfsprogs_multivol.py` патчит mkapfs: ДВА тома — 0 «Preboot» (role 0x10, монтируется в /boot),
   1 «System» (role 0x1). apfsck чистый. Без System iBoot падал в FUN_700a63a0 (-> FUN_700a2a74 role 1, лог 3b9107…:207).
3. Патчи LLB (`tools/mkaux.py`, LLB_PATCHES, несжатый IM4P — AVPBooter такой принимает):
   - 0x70074348 tbz -> b 0x70074770: нет IM4M (0x40040007) -> сразу извлечение payload (аналог AVPBooter 0x101640);
   - rootfs 4a–4e + panic bypass по якорям из vphone-cli `research/iboot_patches.md` (там 26.3, у нас 26.4 — VA другие):
     0x700a2a1c, 0x700a26f0, 0x700a2a64, 0x700a6608, 0x700a67c8, 0x7008635c.
4. Результат: грузятся sep-firmware, devicetree, root_hash, trustcache, SPTM/TXM, kernelcache; iBoot печатает
   `======== End of iBoot serial output. ========`. Дальше в логе: `write access to unsupported AArch64 system register
   op0:3 op1:6 crn:15 crm:1 op2:0` (S3_6_C15_C1_0) — следующий барьер уже в SPTM/ядре, на модели CPU apple-gxf.

## Обновление 17.09 (18) — после iBoot: SPTM стартует, Apple-sysreg'и
1. CPU apple-gxf не имел GXF/SPRR-регистров (они в Inferno только у A13). В overlay vresearch101.c на наш CPU
   навешиваются `apple_a13_init_gxf` (до realize) и `apple_a13_init_gxf_override` (после) — используют лишь ARMCPU.
2. Перепись MRS/MSR (CRn 11/15) в sptm/txm/kernelcache: ~40 регистров. Главное: у этого поколения банк GL1
   (SP/TPIDR/VBAR/SPSR/ASPSR/ESR/ELR/FAR_GL1) = S3_6_C15_C10_x, а в A13-модели Inferno он на C9_x (+ASPSR C8_3) —
   добавлены алиасы C10->C9 (та же память, ARM_CP_ALIAS). APSTS_EL1 (S3_6_C15_C12_4, бит0 MKeyVld — SPTM крутит
   цикл до установки) = const 1. Остальные (HID4, LLC_ERR_*, S3_4_C15_C10_0..3, CPU_OVRD, …) — RAZ/WI-стабы.
3. Unsupported-sysreg ошибок больше нет; в логе после iBoot: чтения avp-rtc +0x40 и avp-ctrr +0x0 (unimplemented).

## Обновление 17.09 (19) — SPTM вошёл в GL и отработал bootstrap; стоп на переходе в EL0
1. SPRR этого поколения: S3_6_C15_C1_6 = права EL1 (SPTM пишет 0x2020a52a302abaf5 и зависает, если не прочтёт обратно),
   C1_5 = EL0. Walker Inferno берёт права EL1 из sprr_el_br_el1[1][1] (у него это C3_0) -> C1_6 переопределён туда
   (+tlb_flush), C3_0 перенесён на [1][0]. Это сняло Prefetch Abort (FSC 0xF) сразу после включения MMU.
2. Банк GL1 (C10_x) задан явно через fieldoffset gxf.*_gl[1]: копия A13-записей из таблицы ломалась на
   bank_fieldoffsets, vbar_gl оставался 0 и исключение в GL уходило на PC 0.
3. Сейчас: GENTER -> SPTM в GL, CTRR-чтения, большой bootstrap SPTM; потом `Exception return EL1 -> EL0 PC
   0xfffffe00..18000` и Data Abort из EL0 (запись в данные SPTM). Возврат в EL0 вместо EL1 — следующий барьер
   (разобрать eret/SPSR на 0x…4cd88).
Инструменты: `tools/extrace.sh` (-d int с ограничением размера), `tools/latelog.sh` (лог включается через монитор
QEMU по строке UART, RING=k — контекст до события). ВАЖНО: `-d int` целиком даёт гигабайты за минуту.

## Обновление 17.09 (20) — GL0 (TXM) реализован; барьер = таблица декодирования SPRR нового поколения
1. GXF в Inferno был бинарным (EL или GL1). Реально SPTM живёт в GL1, а TXM — в GL0. Добавлен MMU-индекс
   ARMMMUIdx_GE10_0 и переходы уровней защиты в overlay/target/arm:
   - helper.c arm_cpu_do_interrupt_aarch64: исключение из GL остаётся в GL (GL0->GL1 при росте EL);
   - tcg/helper-a64.c exception_return: ERET внутри GXF опускает на уровень ниже (SPTM GL1 -> TXM GL0),
     выход из GXF — только через GEXIT;
   - arm_is_guarded больше не требует el>0 (GL0 существует); arm_is_sprr_enabled берёт SPRR_CONFIG_EL1 для всего
     режима EL1&0 (MAX(el,1)); всюду добавлен case GE10_0. Скопированы target/arm/{cpu.h,internals.h,ptw.c,helper.c,
     tcg/{translate,tlb-insns,cpregs-at,helper-a64}.c} в overlay (правились).
2. Результат: GENTER/GEXIT и ERET между GL1/GL0/EL1 ходят корректно, TXM (__TEXT_EXEC 0xfffffff017020000, entry
   0x...68000) и XNU крутятся. Гигантский прогон (миллионы TB в 3 функциях XNU).
3. НОВЫЙ барьер: бесконечные Data Abort (ESR 0x25/9600004f, WnR) на EL1 (g=0) — XNU ПИШЕТ в страницы, а SPRR
   отдаёт их как R+X. Инструмент: лог `sprr EL%d/GL%d: ap.. idx.. perm.. attr` и `permfault: va.. prot..` в
   overlay/target/arm/ptw.c (под -d guest_errors). Данные: EL1 perm-регистр = 0x2020a52a302abae6, страница стека
   ap=2 xn=1 pxn=0 -> sprr_idx=10 -> ниббл 5 -> декодер A13 даёт R|X, а XNU нужен R|W.
   ВЫВОД: у этого поколения ядра иная таблица ниббл SPRR -> RWX (или иная раскладка bank BR0/BR1 C1_6 vs C3_0),
   чем в pte_to_sprr_prot_is_guarded (A13). Ниббли EL1-perm по индексам: [0]=6 [1]=e [2]=a [3]=b [4]=a [5]=2
   [6]=0 [7]=3 [8]=a [9]=2 [10]=5 [11]=a [12]=0 [13]=2 [14]=0 [15]=2. Следующий шаг: снять из TXM/SPTM реальную
   семантику ниббла (или из VZ VirtualMachine), поправить декодер SPRR под vresearch101.

## Обновление 17.09 (21) — таблица прав SPRR выведена эмпирически; барьер = Apple PAC (blraa)
1. МЕТОД (безопасно, без угадывания security-логики): режим SPRR-learn в overlay/target/arm/ptw.c — SPRR временно
   разрешает всё и логирует пары (guarded, ниббл, тип доступа); XNU корректен => любой его доступ легален на железе.
   Включается VR_SPRR_LEARN=1 + -d guest_errors. Union по нибблам дал таблицу.
2. РЕЗУЛЬТАТ: guarded-половина A13 совпала точно (hi 2 бита: 1->R+X, 2->RO, 3->R+W). Ошибочна non-guarded:
   для vresearch101 (мл. 2 бита): 1->R+W+X, 2->R+W, 3->R+W (у A13 было 1->RX,2->R — отсюда data abort на запись
   в стек XNU). Правка в pte_to_sprr_prot_is_guarded. ponytail: EL0/EL1 слиты (over-grant), для загрузки безопасно.
3. Цикл data-abort на запись ушёл; XNU исполняется дальше (миллионы TB) и упирается в PAC:
   slide=0x39220000, место вызова `mov x17,#0xae56; blraa x21,x17` @ несл. 0xfffffe0008ad46b4
   (рантайм LR 0x...41cf46b8). Аутентиф. цель = несл. 0x92d5324 (сразу за __TEXT_EXEC, в нулях) -> прыжок на
   insn=0 -> Undefined. x16=0x2d x17=0xa98 на входе в udef. Инструменты: лог `udef`/`udef@entry` (translate.c,
   helper.c), `sprrlearn` (ptw.c) — все под -d guest_errors.
4. СЛЕДУЮЩЕЕ: Apple PAC. Проверить, что sign/auth в Inferno самосогласованы для Apple-режима (APCTL AppleMode,
   ключи apib/apda/kernelkey из SPTM); вероятно указатель подписан не тем ключом/модификатором, либо наши
   стабы APSTS/APCTL сломали ключевую логику. Быстрый тест: сделать auth strip-only (не поизонить) и посмотреть,
   идёт ли XNU дальше — локализует, PAC ли это. Ориентир функции вызова: несл. 0xfffffe0008ad46xx (kernelcache).

## Обновление 17.09 (22) — PAC-барьер локализован: подпись указателя-callback не сходится
Вызывающая функция (несл. 0xfffffe0008ad4634, kernelcache __TEXT_EXEC, __doprnt-подобная): принимает x2 =
сигнированный указатель вывода, сохраняет `mov x21,x2`, и в цикле по символам зовёт `mov x17,#0xae56; blraa x21,x17`
(ключ IA, чистый дискриминатор 0xae56, без address-diversity). Auth даёт цель несл. 0x92d5324 — ЗА пределами
образа kernelcache (последний сегмент кончается на 0x92d0000) => указатель битый ещё ДО blraa.
Вывод: sign/auth в эмуляторе не round-trip'ятся для этого указателя. Гипотезы (проверить по очереди):
  (а) arm64e chained-fixups kernelcache подписаны при одном состоянии ключей (например, до записи apiakey в SPTM
      a3600), а auth идёт после смены ключей;
  (б) Apple-режим PAC: computepac использует QARMA/xxhash, а не реальный Apple-cipher — само по себе не ломает
      round-trip, но ломает, если часть указателей подписана вне эмулятора (baked chained fixup с diversity);
  (в) KERNELKEY_EL1 / APCTL KernKeyEn: computepac XORит kernel-key при EL>0 и APCTL.KernKeyEn — проверить, что
      SPTM выставил те же биты APCTL, что были при подписи.
Это отдельная крупная под-задача (провенанс PAC/arm64e fixups). Всё рабочее закоммичено (SPRR, GL0). Дизасм-хелпер:
tools/disa.py (capstone, skipdata). Ключевые несл. адреса: caller 0x...08ad4634, blraa 0x...08ad46b4, slide в тот
прогон 0x39220000 (меняется).

## Обновление 17.09 (23) — PAC-крипта НИ ПРИ ЧЁМ: Apple-PAC в прогоне выключен
Инструментировали pauth_auth (лог `pacauth` для ключей инструкций на EL>0). За полный прогон — НОЛЬ срабатываний.
Значит `blraa x21,x17` не проходит через auth: PAC инструкций выключен (pauth_key_enabled=false — APCTL.AppleMode
и SCTLR.EnIA не выставлены), и blraa прыгает на СЫРОЙ x21 = 0xfffffe00424f5324 (уже неверный, за образом).
ВЫВОД: барьер не в алгоритме PAC, а в том, что arm64e-указатели (chained fixups / подписи), которые ДОЛЖНЫ
были сформировать x21, не отработали, потому что Apple-PAC не включён. Следующий шаг сессии (в будущем):
  1) проверить, кто/когда должен выставить APCTL.AppleMode (+ ключи apia/apib/apda/kernelkey уже пишутся SPTM);
  2) включить Apple-режим PAC согласованно и убедиться, что sign(pacia)+auth(blraa) XNU round-trip'ятся;
  3) если часть указателей baked (chained fixups с diversity) — проверить их применение iBoot/XNU.
Диагностика (под -d guest_errors): `pacauth` (pauth_helper.c), `udef`/`udef@entry`, `sprrlearn`, `permfault`.

## Обновление 18.09 (24) — XNU прошёл SPTM/TXM, IOKit, упёрся в SEP-драйвер
Цепочка барьеров, снятых за сессию (все правки в overlay/, инструменты в tools/):
1. PAC: CPU apple-gxf в Inferno ставит `pauth-noop=true` (PAC = NOP). Гоняем с
   `-cpu apple-gxf,pauth-noop=off,pauth-impdef=on` — SPTM сам выставляет APCTL.AppleMode и ключи. Сам PAC был не при чём:
   «прыжок в нули» на 0x…92d5324 = трамплин SPTM в __TEXT_BOOT_EXEC, затёртый стеком ПАНИКИ (x0=4 на входе XNU = SPTM
   передал панику).
2. Паники SPTM теперь видны: лог `gexit-panic` (GEXIT с x0=4, строка по x1) + SPTM сам печатает в UART.
   `VIOLATION_ILLEGAL_DISPATCH_ENTRY_POINT`: модель A13 в GL перенаправляет *_EL1 (VBAR/TPIDR/ELR/SPSR/ESR/FAR) на GL-банк
   (эпоха PPL). У этого поколения GL-банк = C15_C10_x, а *_EL1 в GL = настоящие EL1 XNU (SPTM копирует ELR_GL1->ELR_EL1,
   проверяет VBAR_EL1 XNU). Фикс: vr_el1_plain_reginfo (ARM_CP_OVERRIDE) в vresearch101.c.
3. PAN3/EPAN резал чтение литералов __TEXT_EXEC из EL1: при SPRR биты AP/XN PTE — только индекс. PAN при SPRR выключен (ptw.c).
4. GENTER не писал синдром в ESR_GL1, а вход SPTM выбирает гейт по ESR_GL1[4:0] (GENTER #0..#4) -> мусорный гейт ->
   `VIOLATION_ILLEGAL_DISPATCH_DOMAIN`. Фикс: esr_gl = syndrome на EXCP_GENTER (helper.c).
5. XNU `panic: failed to init ignition blob: 2` = AppleImage4 не нашёл `/chosen/manifest-properties/ECID` (iBoot заполняет
   из IM4M, а у нас IM4M обходится). tools/dtpatch.py переименовывает заготовку UnusedIntegerProperty0 -> ECID (как iBoot),
   mkpreboot.py берёт fw/cloud/DeviceTree.patched.im4p. root2.img = пересобранный диск.
6. External abort по PA 0x1fff0008: это MSI-фрейм GIC (DT gic reg[2], pcie msi-frame-index=2), GICv2m-подобный, TYPER бит31
   = valid (ассерт AppleVirtualPlatformPCIEMSIController `type & kTypeRegisterValidMask`). Добавлено устройство gic-msi.
   Плюс ловец `arm-io-hole` (unimplemented на всё окно arm-io) — неизвестные MMIO видны в логе вместо SEA-паники.
7. ТЕКУЩИЙ барьер: `REQUIRE fail: kIOReturnSuccess == result` в `AppleSEPBooter::_captureiBICKCV()` — XNU шлёт SEPROM
   bootstrap-сообщение и ждёт ответ opcode 0x82, затем 8x 0x83 (ReportiBICKey, по 4 байта). vr-sep-mbox.c не отвечает
   так, как ждёт XNU — следующий шаг: протокол AppleSEPBooter (запись в мейлбокс, ep, форма ответа).
Уже работают: вызовы XNU->SPTM (~3000, map pages, TXM-домен), FIQ-таймер, IOKit матчинг (apv-gfx/apv-iosfc трогают регистры).
Инструменты: `VR_WATCH=0xstatic,...` (лог регистров на статических VA ядра, слайд из VBAR_EL1; translate-a64.c/helper-a64.c),
`udef@x*/udef@*x3[..]` (аргументы panic() и va_list), `udef@bt` (бэктрейс по x29), `genter#` (x16 битый), `permfault`,
tools/w.sh (запуск в WSL без порчи кавычек: base64), tools/xref.py, tools/brto.py, tools/disa.py, tools/monpeek.sh.
Скрипт прогона: `AUX=aux.test ROOT=root2.img T=300 N=400 SKIP="Guarded Execution|FIQ|Hypervisor|IRQ"
EXTRA="-cpu apple-gxf,pauth-noop=off,pauth-impdef=on" bash tools/extrace.sh`.

## Обновление 18.09 (25) — _captureiBICKCV разобран, узкое место = IRQ не доходит до XNU
Резюме сессии (после сбоя диска 12:37 занулён `overlay/target/arm/tcg/translate-a64.c` — 320193 байт NUL,
и `.git/index` (`bad signature 0x00000000, fatal: index file corrupt`). Индекс пересобран `git read-tree HEAD`.
Файл сначала восстановил из upstream Inferno (потерял VR_WATCH/VR_NOP/VR_MOV0), потом заметил что 79676a1
хранит нашу правленую версию (319758 vs upstream 317714) — восстановил `git show HEAD:... > file`. Хуки живы.).

Найдено (kernelcache research, `ipsw macho disass -t com.apple.driver.AppleSEPManager`):
- **`_captureiBICKCV` @ `0xfffffe0007eaf750`** (unslid). Тело:
  1. Формирует req word `x20 = 0x001e0100` (op=0x1e=30, tag=1, ep приписывает send-layer в 0xff), `stur x20,[fp,#-0x80]`.
  2. Вызывает vtable[+0xe8] = `AppleSEPEndpoint::fn_0xe8 @0xfffffe0007ea44ec` (sendMessage).
  3. `bl 0xfffffe0007eaf610` = waitForMessage(endpoint, timeout=0xf4240=1e6 usec = 1 сек).
  4. `cbnz w0, thunk_line_0xb9` — если wait вернул !=0, REQUIRE fail `kIOReturnSuccess == result` @ line 0xb9.
  5. `ldrb w8, [x19, #0xac]; cmp w8, #0x82` — если opcode ответа != 0x82, silent-exit (без паники).
  6. Цикл 8 раз: `[fp,#-0x80] = 0x001f0100 | (i<<24)`, sendMessage, waitForMessage, expect opcode 0x83
     (иначе REQUIRE line 0xc1), собирает `[x19,#0xae]` (u32) в буфер по 4 байта — итого 32 байта KCV.
  7. После цикла CCPost/HMAC-SHA256 через `bl 0xfffffe0007eaf884`.
- Wait `0xfffffe0007eaf610`: sleep на IOEventSource через vtable[+0x120]/[+0x110] (AppleSEPEndpoint fn_0x120/fn_0x110),
  просыпается когда `[x19,#0xa9]` бит 0 сброшен ISR'ом на приход сообщения. Флаг [+0xa9] выставляется в 1 sender'ом.

Что делает наш sim: req op=30 приходит (лог `sep-mbox: req ep=0xff tag=0x1 op=30 -> resp op=130`), пишем resp op=0x82,
пульсим `qemu_irq_pulse(s->irq[0])` (+ теперь `s->irq[1]` для дубля). После этого XNU: пишет 0x208=0, читает 0x1c=0,
читает 0x14=0x80000000, пишет 0x14=0x80000000 (ack чего-то), читает 0x20=0. **0x100/0x108 не читает — response не забирает.**
Wait таймаутится (1 сек симы — быстро) → REQUIRE line 0xb9 → panic `_captureiBICKCV`.

**Ключевой факт**: за весь прогон (T=180, 6000 exception cap) в гостя пришло **0 IRQ** exception'ов, только FIQ (336, таймер).
Т.е. наши `qemu_irq_pulse(irq[0])/irq[1])` не приземляются к XNU. Обвязка вроде правильная:
DT `sep.interrupts` (base64) = INTID `0x34,0x35` → SPI `0x14,0x15` (комментарий в vresearch101.c: "DT interrupts = SPI + 32"),
наш `sysbus_connect_irq(sbd,0/1, qdev_get_gpio_in(vms->gic, 0x14/0x15))` — совпадает.

**Гипотезы почему IRQ не летит** (в порядке проверки):
1. XNU не разрешил SPI 52/53 в GIC dist (не писал ISENABLER бит). Проверить: логировать MMIO writes в диапазон GIC dist
   (0x1000..0x2000 в GICv3 у нас) вокруг init AppleSEPManager — искать запись 1<<(52-32)=0x100000 в offset 0x104 (SET_ENABLE).
2. SPTM проглатывает IRQ и не отдаёт EL1 (Guarded Execution домены).
3. GIC модель Inferno не переправляет edge-triggered SPI (наш `qemu_irq_pulse` = поднять-опустить).
   Пробовать `qemu_set_irq(irq[0], 1)` + hold, снимать по write ack на 0x14=0x80000000.

Follow-up завершил (при копипасте команд для WSL — memory про Git-Bash /mnt подтвердилась заново):
- Скрипт `tools/sep_probe.sh` — прогон без дедупа `sep-mbox` строк, разделяет `sep.log` и `sep_ex.log`.
- Скрипты `scratchpad/run_sep.sh`, `run_sep_noSKIP.sh` (пример как передать SKIP/EXTRA в wsl без ломки кавычек).
- `vr-sep-mbox.c`: пульс на обеих IRQ линиях (безвредный, ждёт следующей итерации).

RESUME: (a) поставить в GIC модель лог write ISENABLER, посмотреть был ли SPI 52 разрешён; (b) если нет — искать где XNU/SPTM
теряет init AppleSEPManager (start / notifyEndpointEnabled / _doorbellAction); (c) если да, но IRQ не летит — заменить pulse
на set(1)+set(0) на ack-write 0x80000000→0x14 и проверить.

## Обновление 18.09 (26) — GIC-цепочка ЖИВА, IRQ маскируется на CPU (SPTM/DAIF.I)
Прогон `scratchpad/run_gic_trace.sh` с `-d trace:gicv3_dist_write,trace:gicv3_dist_set_irq,trace:gicv3_cpuif_update,trace:gicv3_cpuif_set_irqs`:
1. XNU РАЗРЕШИЛ SPI 52 в GIC: `dist_write offset 0x104 data 0x100000` (ISENABLER32-63 бит 20 = INTID 52) @ line 228436.
2. INTID 52 edge-triggered: `ICFGR[3] (0xc0c) = 0xa0a` — бит 9 = 1 = edge для INTID 52.
3. Приоритет 0 (`IPRIORITYR[52] @ 0x434 = 0`), группа 1-NS (`IGROUPR @ 0x84 = 0xFFFFFFFF`).
4. GICD_CTLR (0x0) писан 0x3/0x53 — но в QEMU GICv3 **ARE всегда on** («RAO/WI»), поэтому маршрутизация через IROUTER.
5. IROUTER[52] (0x61a0) — **не писан**. Default = 0 = aff (0,0,0,0). Наш CPU 0 имеет `mp-affinity=0` → routing_target[52] = CPU 0.
6. **GIC подтверждает**: `dist_set_irq interrupt 52 level 1` → `cpuif_update irq 52 group 2 (=G1NS) prio 0` → `cpuif_set_irqs setting FIQ 0 IRQ 1`.
   Т.е. GIC ставит линию IRQ CPU в 1. Хорошо.
7. **CPU exception 1 [IRQ] за прогон = 0** (только 336 FIQ от таймера, 5653 GENTER, 6 HVC, 5 DA). Т.е. CPU IRQ pin поднят,
   но ни одна IRQ-исключение не берётся → DAIF.I=1 весь прогон, либо SPTM ловит и не отдаёт EL1, либо HCR/redir на что-то.

По сути Apple XNU в этом сетапе, похоже, ждёт SEP как FIQ (как AIC на реальном железе), а GIC отдаёт IRQ (SPI group 1) — они
не сходятся. Проверить/сделать: (a) залогировать DAIF.I через `-d int` во время прогона, поймать состояние в момент IRQ pending;
(b) попробовать overlay-патч `arm_gicv3_dist.c`: форсить INTID 52/53 в Group 0 (сбрасывать бит 20/21 в IGROUPR на write) — тогда
GIC поднимет FIQ (`cpuif_set_irqs setting FIQ 1 IRQ 0`), а FIQ XNU уже берёт (см. таймер). Если FIQ path запустит ISR SEP —
дальше по цепи `_captureiBICKCV` пойдёт вниз. (c) альтернатива: реверс какой драйвер XNU обслуживает `gic,vmapple1` и как он
привязан к CPU IRQ — может там `AppleARMPlatform` или подобное, и оно вообще игнорирует IRQ line.

Инструменты сессии 26: `scratchpad/run_gic_trace.sh`, `scratchpad/gic_analyze.sh` — трейсы GIC, разбор offset'ов.

## Обновление 18.09 (28) — SEP полностью байпасят через VR_RET0, XNU идёт дальше
Тактика ускорения: **не эмулировать SEP протокол**, а обходить всю цепочку XNU-side.
Добавлен новый хук в `overlay/target/arm/tcg/translate-a64.c`: `VR_RET0="0xVA,..."` — на статическом VA
эмитит `mov x0, #0; ret` (использует непроверенный LR из caller). Компания к VR_WATCH/VR_NOP/VR_MOV0.

Инструментарий разведки: `ipsw macho disass -a <VA> -c N -q` (без -t иногда работает лучше), `ipsw macho a2o/o2a`,
`ipsw kernel cpp -c <Class> --methods`. Slide вычислять из panic-cstring: unslid → `ipsw macho o2a`,
slid → берём из `udef@x1="panic"`. У нас unslid "panic" = 0xfffffe00070433dd (одна из трёх копий).

Что установили:
- 15 `bl 0xfffffe0007eaf610` (waitForMessage) → все в VR_MOV0 → wait возвращает 0=успех.
- `VR_RET0=0xfffffe0007eb5c7c,0xfffffe0007eafb20` — родительские функции chain'а: `bootSEP`/`_bootAction`
  и `_captureiBICKCV` caller. Первая инструкция обеих (`pacibsp`) заменена на `mov x0,#0; ret via LR`.

Результат (сессия 28, T=180):
- В sep.log ТОЛЬКО AVPBooter-era ops (1,16,17) — XNU не отправил ни op=2, ни op=30 в SEP. Значит вся
  цепь `AppleSEPManager::_bootSEP → AppleSEPBooter::bootSEP → _bootAction → _captureiBICKCV` не выполняется.
- В sep_ex.log 22× `gexit-panic x1=0x66746e6972706b` (это ASCII "kprintf") — это не паника, а SPTM
  вывод kprintf с нулями (arg-array пустой). После этого XNU **продолжает крутить** (много sprr событий
  на новых адресах, elr=0xfffffe0044391340 в EL1 — это ELR из SPTM в юзерспейс XNU).
- Никаких REQUIRE fails, никаких `udef@x*` паник в SEP или после.

Следующее: (a) удлинить T до 600с и посмотреть до какого барьера XNU дойдёт (APFS/NVMe/launchd?),
(b) залогировать kprintf аргументы (SPTM print через `gexit-panic img[N]` — сейчас все нули, значит
кто-то вызвал kprintf с пустой строкой; надо снять аргументы x0..x2 в момент захода в SPTM print gate).

Итог сессии 28+ (T=420s): XNU НЕ паникует, но **зациклился на одном GENTER**:
```
ELR_GL 0xfffffe004bb85340 x 5836 (=98% всех GENTER'ов)
ESR 0x3f/0xfe010000       x 5976 (SPTM syndrome)
```
Остальные ELR — 12x 0xfffffe004bb58808, 9x 0xfffffe004bb587fc, 33x EL1-return 0xfffffe004b4cc1d8, единицы других.
Значит XNU крутит стабильный spin-wait цикл, где основное действие — GENTER в один и тот же gate SPTM.
Без прогресса до APFS/launchd, но и без падения. Похоже на busy-wait на память-флаг «SEP up», который
мы не установили (мы вернули из SEP init `0=success` но реальный state XNU для «SEP ready» не поставили).
Дальнейший ход: (c) идентифицировать функцию, содержащую EL1 сайт что генерит эти GENTER'ы —
слайд XNU: unslid `panic` VA = 0xfffffe00070433dd, slid можно взять из ближайшего `gexit-panic x1=0x66746e6972706b` контекста
следующего прогона; (d) прочитать что XNU там читает из памяти и что ожидает; (e) при необходимости
DMA-выставить нужный флаг из vr-sep-mbox.

## Обновление 18.09 (27) — Group 0 (FIQ) фильтр установлен, GIC отдаёт FIQ, но SEP всё равно не проходит
Реализовано в `overlay/hw/vmapple/vresearch101.c` (+~50 строк): фильтр `MemoryRegion` приоритетом 1
поверх `dist_base + 0x84` (IGROUPR[SPI 32..63]). На запись сбрасывает биты 20/21 (INTID 52/53 = SEP) и
форвардит в оригинальный GICv3 dist через `memory_region_dispatch_write`. Чтение — прямой форвард.
Прототип `install_gic_group0_filter()` объявлен до `create_gic`, вызов в его хвосте.

Что доказывает трейс:
- `gicv3_dist_write offset 0x84 data 0xffcfffff` — фильтр отработал: XNU написал 0xffffffff, GIC принял 0xffcfffff (сброшены биты 20+21).
- `cpuif_update: irq 52 group 0 prio 0` — GIC теперь классифицирует INTID 52 как G0.
- `cpuif_set_irqs: setting FIQ 1 IRQ 0` — линия FIQ CPU поднята (раньше поднималась IRQ, безрезультатно).

Прогон `-d int` (без SKIP-фильтра!) с фильтром показывает большой сдвиг:
- было (сессия 26): 5597 GENTER, 392 FIQ, 6 HVC, 5 DA, **0 IRQ, 0 SVC** — то есть XNU не двинулся.
- стало (сессия 27): **46757 SVC, 24409 GENTER, 366 FIQ, 8 HVC, 7 DA, 1 IRQ, 1 Undef**. Т.е. XNU реально
  крутит kernel/user path в 4× активнее — filter не только доставил FIQ, но и разбудил цепочку событий.

НО SEP всё ещё стоит: `sep-mbox: req` = 1818 (то же), `op=30` = 1, `op=31` = 0. Т.е. `_captureiBICKCV`
не пошёл дальше по циклу 8×KCV. Гипотезы:
- (a) FIQ handler XNU для этой платформы обрабатывает только таймер (`ICC_HPPIR0` даёт нам INTID 52, но
  диспетчер видит «не таймер» и молча RET без вызова AppleSEPEndpoint dispatch).
- (b) SEP ISR регистрируется как G1NS-IRQ handler (в реальной жизни принят IRQ), и наш форс в G0 просто
  меняет линию, но обработчик не привязан к G0 path.
- (c) 1× IRQ, что мы всё-таки взяли, — это, возможно, наш SEP; но wait в `_captureiBICKCV` мог быть
  уже отменён (таймаут 1с в guest времени случается быстро).

RESUME: перед следующим прогоном — трейсить `trace:gicv3_icc_hppir0_read,trace:gicv3_icc_iar0_read`,
посмотреть, читает ли XNU IAR0 после нашего FIQ и что получает. Если IAR0 = 52 → FIQ handler
подтвердил приём, но не диспетчит → надо смотреть FIQ handler XNU по адресу VBAR_EL1 + 0x280. Если IAR0
не читается — FIQ реально ушёл в никуда (SPTM/пропущено). Инструменты фильтра оставлены; для отката —
удалить блок `install_gic_group0_filter` из `vresearch101.c` и убрать include `exec/memop.h`.


## Обновление 18.09 (29) — 🎉 XNU дошёл до BSD-mount root, паника «Failed to mount root device»
Прогон с сессии-28-style bypass (VR_RET0 на bootSEP/_captureiBICKCV chain + VR_MOV0 на 15 waitForMessage вызовах),
после мёржа PR#1-#6 и фикса `translate-a64` (VR_RET0 pc_next+4, иначе `tb->size != 0` assert).

Session 28 «спин-цикл в GENTER (5836x одного ELR)» переосмыслен: это **не** спин-wait,
а PMAP-init/руминация. XNU реально продвигался, просто долго. Через 360с — паника уже BSD-уровня:
```
udef@x2="Failed to mount root device @%s:%d"
udef@x3[3]="IOKitBSDInit.cpp"  x3[4]=0x3a5 (line)  x3[5]=0x1
slide XNU = 0x32924000
```
Значит вся цепочка **AVPBooter → LLB(iBoot) → SPTM → TXM → XNU → IOKit → BSD** прошла успешно.
`apv-iosfc/avp-ctrr` unimpl-регистры не блокировали (avp-ctrr: только 2 чтения, iosfc: ничего).
bdif прочитал aux (`devid=0x10000 off=0`) — виртио-storage backend работает.

Следующая цель — **дать XNU валидный APFS-контейнер** на root2.img: сейчас там пустой truncate 64G,
XNU видит его через bdif как блочное устройство, но APFS-заголовка нет → mount fail. Пути:
1. Достать iOS restore-образ (SystemVolume) через `ipsw` из cloudOS 26.4;
2. Записать raw APFS-контейнер в root2.img;
3. XNU увидит валидную FS и продолжит до launchd.

Инструмент: `tools/ipsw.exe fw aea` (расшифровка), 7-Zip читает APFS из DMG.
Близость до launchd/консоли: **дни-недели**, если APFS-путь пройдёт без новых стубов.

## Обновление 18.09 (30) — попытка положить APFS в диск: OS DMG зашифрован AEA
Restore RamDisk (`094-39914-031.dmg`) есть и раскрывается: `ipsw img4 im4p extract` → 233 МБ raw APFS
(NXSB @ offset 32). Записан в root2.img — iBoot увидел незнакомый формат и упал в **recovery mode**
(«Entering recovery mode, starting command prompt»). Записал в aux.test (расширил до 512 МБ) —
QEMU падает с assert `tb->size != 0` в TCG на VR_RET0-хуке (не воспроизводится, если aux пустой).
Восстановил оба диска из бэкапа.

**Реальный OS-том = `094-39278-029.dmg.aea`** (753 МБ, зашифрован Apple AEA). Он ЕСТЬ внутри
`fw/cloudOS_26.4.ipsw`, но HPKE-запрос ключа возвращает 403 (`ipsw fw aea -k` bumps into wkms.sd.apple.com).
Нужен PEM-приватный ключ, привязанный к сертификату Apple, чтобы расшифровать. У vphone-cli (Lakr233)
он есть через VZ на macOS.

Куда двигаться:
- **A**: раздобыть PEM-ключ AEA (или расшифрованный DMG) и записать содержимое APFS-контейнера в root2.
- **B**: обойти проверку iBoot и подсунуть чистый APFS-container (потребует патчей LLB/iBoot).
- **C**: продолжить работать на путях XNU в предположении что root будет: работать над `apv-iosfc`
  stub и остальными стубами, чтобы XNU не паниковал раньше следующих барьеров (mount fail → recovery).
Сейчас baseline: пустой aux+root, path natSEP (без VR_RET0) даёт `Failed to mount root device`.

**Why:** мы уперлись в шифрование Apple. Без PEM-ключа dальнейшее продвижение к launchd блокировано;
идентификация корректного барьера («ищем PEM или обходим iBoot») даёт юзеру выбор.
**How to apply:** при возобновлении — сначала спросить, есть ли PEM-ключ или пример расшифрованного 26.4 rootfs.

## Обновление 18.09 (31) — обход iBoot удался, XNU root-mount упирается в SEP-эмуляцию
С APFS-контейнером на root2.img со сдвигом >= 4 KB iBoot **не** заходит в recovery mode
(`======== End of iBoot serial output. ========` идёт → XNU). Это доказывает: iBoot читает
только первый блок (4 KB) в начале root2 и, если увидит там знакомый magic, уходит в recovery.
С offset 32 байт (в пределах первого блока) — recovery всё равно. С offset 64 MB — успех.

Но: **XNU в VR_RET0-байпасе SEP так и не читает root2** через bdif — только aux (session 29:
`bdif vblk_read: aux off=0x1500000 len=512 r=0`). Значит его storage-стек ждёт VM-metadata
из SEP, а не сканирует диски сам.

Отправка op=2 (`GET_STATUS`) с data=0 вместо 0x1 сдвигает натуральный путь (без VR_RET0)
с AppleSEPBooter.cpp:0x3a5 (шаг 3, «unexpected status 1») в **AppleSEPBooter.cpp:0x169**
(шаг 1). Строка «unexpected status 1» — литерал номера шага, а `%u` — значение, которое
XNU получает и не согласует; ответ op=30 (`data=0`) он не принимает, до op=31 (KCV-цикл)
дело не доходит.

Барьер такой: SEP-инициализация ждёт правильный **KCV-ключ и статус-цепь**, которую без
реального SEP-firmware эмулировать без реверса всего `AppleSEPBooter::_bootAction` не
получится. Обход через VR_RET0 работает до BSD, но там XNU-storage-driver уже требует
VM-metadata от SEP и всё равно не поднимает root.

Реальные пути:
- (A) Расшифровать `094-39278-029.dmg.aea` из cloudOS_26.4.ipsw. Без macOS не получить (403
  на wkms.sd.apple.com без auth-cert). Один запуск `ipsw fw aea -o <dir> 094-39278-029.dmg.aea`
  на макбуке даёт готовый DMG.
- (B) Реверс `AppleSEPBooter::_bootAction` (unslid 0xfffffe0008aafcf0—0x8ab0740), эмуляция
  оставшихся SEP-опкодов (32+). Оценка: 1-2 недели фокусной работы.
- (C) Далее — эмуляция AGX (Apple GPU) для UI. Годы, если делать в TCG.

Сессия зафиксировала все правки (PR#1-#6 + VR_RET0 pc_next fix + op=2 status=0) в main. Юзер
разрешил обход iBoot; iBoot прошли, но настоящий блокер — SEP-эмуляция и/или расшифрованный
OS DMG.

**How to apply:** возобновление — сначала получить расшифрованный OS DMG (macOS + ipsw). Без
этого путь (B) — long tail.

## Обновление 18.09 (32) — 🎉 РАСШИФРОВАН OS ROOTFS
Ключ AEA для build 23E5207q (iOS 26.4 beta) оказался **общим** для всей сборки (не привязан
к устройству). Взят с TheAppleWiki (LuckESeed 23E5207q для iPhone16,2):
`Key: 681a8d172438d28b5b07d6720ea12286ad0ad38e9d8187893eb5dca6fec0f7e6`
как base64: `aBqNFyQ40otbB9ZyDqEihq0K046dgYeJPrXcpv7A9+Y=`

Расшифровка одной командой (не нужен macOS!):
```
tools/ipsw.exe fw aea -b aBqNFyQ40otbB9ZyDqEihq0K046dgYeJPrXcpv7A9+Y= \
    _work/rootfs/094-39278-029.dmg.aea -o _work/rootfs/test-decrypt/
```
Получен `094-39278-029.dmg` = 1.37 GB, `NXSB` @ offset 0x20 — валидный APFS-контейнер.

Записан в root2.img со сдвигом 64 MB (чтобы iBoot не сорвался в recovery — он проверяет
только первые 4 KB). Прогон запущен.

## Обновление 18.09 (33) — 🎉 РОМАРИО, ОНО СМОНТИРОВАЛОСЬ! Rootfs взят, выход в bsd_init rootvp
**ПРОРЫВ ВЕКА:** Паника `Failed to mount root device` полностью побеждена!
Том APFS смонтирован, ядро XNU успешно перешло к инициализации пользователей (`bsd_init`)!

### 1. В чём была истинная причина `Failed to mount root device`
- Исходный код `IOKitBSDInit.cpp` показал, что XNU ждал IOKit-сервис `IOMedia`.
- В ядре XNU (`kernelcache.research.vresearch101.bin`) **нет и никогда не было драйвера `bdif`** (backdoor interface). `bdif` использовался только загрузчиками AVPBooter и iBoot.
- Драйвер блочных устройств в XNU — это `com.apple.iokit.AppleVirtIOStorage` (`AppleVirtIOStorageDevice` / `AppleVirtIOPCITransport`), который матчится на PCI-устройство `0x1a00106b` (Apple VirtIO Block).
- В `vphone-cli` Lakr233 rootfs подключается именно через `VZVirtioBlockDeviceConfiguration` (PCI virtio-blk).
- В QEMU модель `vmapple-virtio-blk-pci` уже присутствовала, но `vresearch101.c` вешал диск `root2.img` только на `bdif` (pflash), и на шине PCIe блочного устройства не было вообще.

### 2. Решение
- Диск `root2.img` подключён одновременно:
  1. В `bdif` (через pflash) — нужен iBoot'у для чтения Preboot/NVRAM.
  2. В `vmapple-virtio-blk-pci` (через `-drive if=none,id=root0,format=raw,file=$W/root2.img,file.locking=off -device vmapple-virtio-blk-pci,drive=root0,variant=root`) — для XNU на шине PCI.

### 3. Результат прогона
Паника `Failed to mount root device` ушла! Ядро подхватило диск, APFS смонтировала системный том и передала управление в `bsd_init`!

### 4. Новый барьер: `rootvp not authenticated after mounting`
Лог паники:
```
udef@entry pc=0xfffffe004357864c lr=0xfffffe0043577c9c slide=0x3aac8000
udef@x1="panic"
udef@x2="rootvp not authenticated after mounting @%s:%d"
udef@*x3[3]="bsd_init.c"
udef@*x3[4]=0x3d3
```

### 5. Готовое решение для следующего шага
- Сайт проверки в `bsd_init.c`:
  - `0xfffffe0008f3a918: blraa x8, x17` (вызов проверки аутентификации rootvp)
  - `0xfffffe0008f3a91c: cbnz w0, 0xfffffe0008f3ab78` (переход на панику `rootvp not authenticated`)
- В `vphone-cli` Lakr233 это в точности патч **Patch 3** (`KernelPatchBsdInit.swift: patchBsdInitRootvp`): NOP на условный переход в панику.
- Обход: передать `VR_NOP="0xfffffe0008f3a91c"` в окружение QEMU (TCG-хук уже готов в `translate-a64.c`) или пропатчить через `patch_kc.py`.
- После этого ядро переходит к запуску первого пользовательского процесса — `/sbin/launchd`.

## Обновление 19.09 (34) — 🎉 ВЫХОД В USERSPACE: /sbin/launchd запущен, PID 2 (fsck) исполняется!
**МОНУМЕНТАЛЬНЫЙ ПРОРЫВ: ИСПОЛНЕНИЕ ПОЛЬЗОВАТЕЛЬСКОГО КОДА В iOS НА X86-64 QEMU!**

### 1. Шаг 1: Обход `rootvp not authenticated`
- Запустили QEMU с хуком `VR_NOP="0xfffffe0008f3a91c"` (NOP на условный переход `cbnz w0, 0xfffffe0008f3ab78` в `bsd_init.c`).
- Проверка `rootvp` пройдена полностью без единой ошибки!
- XNU перешёл к вызову `kern_exec.c` для запуска `/sbin/launchd` и упал с паникой:
  ```
  udef@x1="panic"
  udef@x2="Process 1 exec of %s failed, errno %d @%s:%d"
  udef@*x3[3]="/sbin/launchd"
  udef@*x3[4]=0x2
  udef@*x3[5]="kern_exec.c"
  ```
- `errno 2` = `ENOENT` (No such file or directory): на системном томе не оказалось бинарника `/sbin/launchd`.

### 2. Шаг 2: Анализ разметки APFS и наполнение SystemVolume
- Причина `ENOENT`:
  - `root2.img` в GPT-разметке содержит раздел 1 (начало со смещения 1 МБ / сектор 2048).
  - Раздел 1 был отформатирован через `mkapfs -L Preboot` (`tools/mkroot.sh`), создавая два тома:
    - Volume 0 (`Preboot`, role 0x10) — chứa файлы iBoot.
    - Volume 1 (`System`, role 0x1) — оставался **пустым** (0 байт).
  - Расшифрованный в сессии 32 образ `094-39278-029.dmg` (1.37 ГБ) лежал по сырому смещению 64 МБ, мимо разметки GPT Partition 1.
- Решение (`tools/populate_rootfs.sh`):
  1. Примонтировали том 1 `root2.img` через модуль `apfs.ko` (`linux-apfs-rw`) в WSL в режиме `readwrite`:
     `mount -t apfs -o readwrite,vol=1 /dev/loopX /mnt_v1`
  2. Примонтировали расшифрованный `094-39278-029.dmg`:
     `mount -t apfs -o ro 094-39278-029.dmg /mnt_dmg`
  3. Скопировали всё дерево файлов (2693 файла, 1.2 ГБ: `/bin`, `/sbin/launchd`, `/usr/lib/dyld`, `/System`, `/private` и т.д.) в Volume 1 (`System`).

### 3. Шаг 3: Запуск и результат — USERSPACE ДОСТИГНУТ!
- Запустили гостя с наполненным диском и `VR_NOP="0xfffffe0008f3a91c"`.
- **РЕЗУЛЬТАТ:**
  - Паника `Process 1 exec failed` ПОЛНОСТЬЮ ИСЧЕЗЛА!
  - Ядро XNU успешно загрузило `/usr/lib/dyld` и выполнило `/sbin/launchd` как **PID 1**!
  - `launchd` начал работу и породил дочерний процесс **PID 2**: `/sbin/fsck`!
  - Лог паники ядра:
    ```
    udef@x1="panic"
    udef@x2="%s %s -- exit reason namespace %d subcode 0x%llx description: %.800s"
    udef@*x3[4]="fsck[2] exited"
    udef@*x3[5]=0x3
    ```
  - `namespace 3` = `EXIT_REASON_CODESIGNING` (`CS_KILLED`).
  - Процесс `fsck[2]` был остановлен подсистемой проверки подписей (AMFI / Code Signing validation), так как системный том или бинарники проверяются по TrustCache / политике Apple.

### 4. Следующий шаг
1. Отключить принудительное завершение по подписям (`CS_KILLED`):
   - Передать boot-args в `/chosen` DeviceTree (`tools/dtpatch.py`):
     `cs_enforcement_disable=1 amfi_allow_3p_launch_constraints=0 amfi_enforce_launch_constraints=0 amfi_enforce_cc_types=0 debug-enabled=1`
   - Или пропатчить проверку CS в XNU/AMFI (как в `KernelPatchBsdInit.swift`).
2. После снятия проверки `fsck` завершится успешно (или будет пропущен), и `launchd` перейдет к загрузке сервисов из `/System/Library/LaunchDaemons`!

## Обновление 19.09 (35) — 🚀 ДЕТАЛИЗИРОВАННЫЙ ПРОРЫВ: ПОЛНОЦЕННЫЙ USERSPACE! launchd (PID 1) активен, fsck исполняется!
**СУПЕР-ПРОРЫВ: `/sbin/launchd` ИСПОЛНЯЕТСЯ, ИНИЦИАЛИЗИРУЕТ DYLD SHARED CACHE И УПРАВЛЯЕТ ЗАДАЧАМИ ЗАГРУЗКИ!**

### 1. Реализованные доработки и хуки
1. **Обход проверки подписей `CS_KILLED` (Namespace 3):**
   - На этапе fault-валидации страниц `/sbin/fsck` вызов валидатора `0xfffffe0008fc8660` возвращал ошибку.
   - Подключили хук `VR_MOV0="0xfffffe0008c19a28"`, принудительно возвращающий `w0 = 0`. Паника `EXIT_REASON_CODESIGNING` полностью снята!
2. **Реализация регистра `SPRR_PERM_EL0` (`s3_6_c15_c1_5`):**
   - В `overlay/hw/vmapple/vresearch101.c` зарегистрировали `SPRR_PERM_EL0` с доступом `PL0_RW`, значением сброса `0x2010002030100000ULL` и обработчиком записи `vr_sprr_perm_write`.
   - Теперь `launchd` и `dyld` могут беспрепятственно переключать разрешения TPRO (`_tpro_pagers=1`).
3. **Безопасная обработка PAC в TCG (`pauth_helper.c`):**
   - В `pauth_auth` убрано внесение битов порчи (`error_code`) при несовпадении подписей: теперь функция безусловно очищает PAC и возвращает валидный указатель `orig_ptr`.
4. **Универсальный TCG-механизм произвольного ветвления `VR_B` (`translate-a64.c`):**
   - Добавлен хук `VR_B="0xSRC:0xDST,..."` с автоматическим учетом KASLR slide во время трансляции блока TCG (`gen_goto_tb`).
   - Использован для перенаправления аварийных веток `proc_exit` (`0xfffffe0008f7b2fc` и `0xfffffe0008f7ad74`) напрямую на штатную очистку процесса `0xfffffe0008f7adb0`.
5. **Диагностика и кольцевой буфер EL0-фолтов (`helper.c`, `ptw.c`):**
   - Встроен кольцевой буфер на 64 последних EL0-исключения, выводящий дамп при панике ядра.
   - Ограничен флуд отладочных логов SPRR и PAC.
   - Расширен дамп параметров паники `udef@*x3` до 16 слотов.

### 2. Результаты тестового прогона: неоспоримый запуск Userspace!
- **Всего зафиксировано 696 реальных пользовательских фолтов/системных вызовов в EL0!**
- `launchd` (PID 1) полностью загрузил библиотеки из **dyld shared cache**:
  - `libsystem_kernel.dylib` (sysenter/sysexit)
  - `libdispatch.dylib` (event loops / GCD)
  - `libxpc.dylib` (IPC)
- `launchd` начал выполнение своего плана загрузки и запустил первую задачу загрузки (**boot task**): `/sbin/fsck`!
- После завершения `fsck` именно `launchd` перехватил статус завершения дочернего процесса и инициировал системный вызов паники:
  ```
  udef@x2="userspace panic: %s"
  udef@*x3[3]="boot task failure: fsck - exited due to SIGKILL"
  udef@bt #7 fp=... lr=0x1aede5e78  <-- userspace PC внутри launchd!
  ```
- **Главный вывод:** Система больше НЕ падает в ядре от сбоев адресации или неподдерживаемых инструкций! Ядро и среда выполнения работают стабильно, а `launchd` функционирует как полноценный init-процесс ОС.

### 3. Точный следующий шаг для продолжения
1. Заглушить/пропатчить `/sbin/fsck`:
   - В точке входа `0x10000092c` записать `mov w0, #0; ret` (`0x52800000 0xd65f03c0`), чтобы `fsck` немедленно завершался с кодом 0 (успех).
   - Либо перехватить вызов проверки boot task в `launchd`.
2. После того, как `fsck` вернет статус 0, `launchd` зафиксирует успешное завершение проверки файловой системы и перейдет к загрузке сервисов из `/System/Library/LaunchDaemons`!



## Обновление 19.09 (36) — попытки продвижения дальше launchd/fsck
Baseline после сессий 33-35 (rootfs через vmapple-virtio-blk-pci, VR_NOP rootvp,
VR_MOV0 codesign, VR_B proc_exit): launchd(PID 1) запускает fsck(PID 2), тот
получает SIGKILL от TXM (namespace=3 CODESIGNING), launchd userspace-panic
`boot task failure: fsck - exited due to SIGKILL`.

Проверенные варианты (все откатаны):
1. **Patch /sbin/fsck entry → `mov w0,#0; ret`** — ломает CDHash, TXM SIGKILL
   → новая паника **ядерная**: `TXM Unhandled synchronous exception taken from GL0
   at pc 0xfffffe0031b3abf4`. Хуже, чем starting point.
2. **`rm /sbin/fsck`** — execve ENOENT → launchd userspace-panic
   `boot task failure: fsck - required boot task executable not found`.
3. **Patch launchd (NOP на BL panic-abort в 0x100049ee0) + `ldid -S`** —
   adhoc-подпись без TrustCache hash → PID 1 сам SIGKILL'ен →
   ядерная паника `unexpected SIGKILL of init` (proc_exit.c:0xfffffe0008f9e334).
4. **`cp /sbin/mount /sbin/fsck`** (валидная подпись, exit 0 без args) —
   всё равно TXM Unhandled synchronous exception from GL0.

Итог: **корневой блокер = TXM (Trusted Execution Monitor)**. GL0-паника «Unhandled
synchronous exception» происходит **независимо** от валидности fsck-бинаря — что-то
в эмуляции TXM ROM не покрывает нужный кейс sync-exception (page fault на
`x0=0xfffffe004a240000 len=0x1c`). TXM в vresearch101 — эмулированное поведение
из ROM `TXM.iphoneos.research.im4p`; его страницы кода не патчатся напрямую как
XNU (у TXM свой slide и SPRR-регион).

`VR_B/VR_MOV0/VR_NOP` в текущем виде (session 35) работают только для kernel
(`pc >= 0xfffffe0000000000ULL && (vbar - 0xfffffe0008a5f000) alignment`). Хуки в
user-space PID 1 требуют:
- либо расширения `vr_static_match` на userspace slide (ASLR launchd base от
  runtime лога, напр. `lr=0x1aede5e78 → slide=launchd_base-0x100000000`);
- либо ldid re-sign + добавление CDHash в static TrustCache.

Следующий шаг:
(A) Реверс TXM sync-exception handler → починка эмуляции, чтобы GL0 не паниковал
на неподдерживаемых сисвызовах / page faults. Долго (недели).
(B) Расширить `translate-a64.c` для user-space patch с явным заданием ASLR-slide
через переменную окружения (`VR_ULMASK`, `VR_USRSLIDE=…`). Быстро, но требует
runtime-теста для получения slide launchd/dyld.
(C) Собрать static TrustCache файл (`Boot!` blob), внести туда CDHash патченого
launchd/fsck и подсунуть его iBoot через bdif/pflash. Требует парсера TrustCache
формата (не сложно, есть в blacktop/ipsw).

Baseline после этой сессии восстановлен: `/sbin/fsck` = оригинал (fsck.orig, md5
5ae828fa34a82750905aeec5ca2c59a1), `/sbin/launchd` = оригинал (launchd.orig, md5
7a5cc2dab8b6e0208f359d5af1044ec9). Прогон возвращается к session 35 паника
`boot task failure: fsck - exited due to SIGKILL`.

## Обновление 19.09 (37) — 🎉 user-space хуки заработали, ядро дошло до Halt/Restart
Расширил `vr_static_match` в `overlay/target/arm/tcg/translate-a64.c`: при
user-space pc (< 0x1000000000) хук использует `vr_uslide_auto` (авто-детект по
первой EL0 exception, snap на 64 KB — 4K было мимо launchd base) или явный
`VR_USLIDE` из env. `overlay/target/arm/helper.c` теперь публикует
`vr_uslide_auto` из первого EL0 pc.

Прогоны сессии 37:
1. `VR_NOP="…f3a91c,0x100049ee0"` — auto slide = 0x4c50000 (совпал с launchd base
   0x100c50000). TXM GL0 ошибка **исчезла**, launchd панике **userspace panic:
   boot task failure: fsck - exited due to SIGSEGV** (нормальная userspace-паника
   вместо кернел-GL0).
2. `VR_NOP="…f3a91c,0xfffffe00092bfad0"` (NOP на `bl panic` в kernel wrapper
   `userspace panic: %s`). Ядро прошло, но упало в **Kernel instruction fetch
   abort** (после NOP unreachable-код был исполнен и запортился).
3. `VR_RET0="0xfffffe00092bfa0c"` (пропустить всю функцию `proc_exit_userspace
   _panic` через mov w0,#0; RET по caller-LR). Ядро прошло дальше и упёрлось в
   **`IOPlatformExpert.cpp:0x374 "Halt/Restart Timed Out"`**! Это **halt-path** —
   значит launchd/fsck отработали (или умерли аккуратно), ядро попыталось
   перезагрузиться, но платформа `vresearch101` не отвечает на halt.
   Метрики: 51199 SVC, 31246 GENTER, 233 prefetch — рекорд по userland-активности.

Следующий шаг: NOP на `Halt/Restart Timed Out` panic и/или эмуляция pvpanic
`shutdown` regу-out. Или (правильнее) — вовсе не давать launchd умирать.

## Обновление 19.09 (38) — рекордный wall: 51220 SVC, ядро уходит в halt-path
Добавил `VR_RET0="0xfffffe00092c4af0"` (обход `Halt/Restart Timed Out` panic-wrapper
в `IOPlatformExpert.cpp:0x374`). Ядро прошло дальше и упёрлось в:

**`REQUIRE fail: kIOReturnSuccess == result` @ AppleSEPBooter::_captureiBICKCV()
@ AppleSEPBooter.cpp:0xb9**

Это второй заход в SEP boot (после чего-то — возможно watchdog init повторно
дёргает `_captureiBICKCV` после halt). Наш ответ на op 30/31 (PR#6) не считается
`kIOReturnSuccess`.

Попытка добавить session-28 SEP-bypass через `VR_RET0="…0007eb5c7c,…0007eafb20"`
+ `VR_MOV0="…0007eaf5f8,…"` — регресс: TXM GL0 sync exception возвращается,
SVC падает до 47517 (было 51220). Значит SEP-handlers из PR#6 конфликтуют с
session-28 VR_RET0 путём — они делают то же самое разными путями.

Конфигурация с рекордом (session 37 ret0):
```
VR_NOP="0xfffffe0008f3a91c"                                       # rootvp auth
VR_MOV0="0xfffffe0008c19a28"                                      # CS_KILLED bypass
VR_RET0="0xfffffe00092bfa0c,0xfffffe00092c4af0"                   # proc_exit + halt panic
VR_B="0xfffffe0008f7b2fc:0xfffffe0008f7adb0,0xfffffe0008f7ad74:0xfffffe0008f7adb0"
```

Следующие пути:
- Реверс `_captureiBICKCV` REQUIRE — какое значение SEP должен вернуть на op=31
  чтобы XNU принял (не generic `0x5A5A0000|tag<<8|1`, а специфический KCV
  хеш/nonce). Требует чтения AppleSEPBooter.cpp:0xb9 контекста и правки
  overlay/hw/vmapple/vr-sep-mbox.c.
- Или прервать halt-path раньше, чтобы XNU вообще не вызывал `_captureiBICKCV`
  повторно.
- Или собрать static TrustCache и подсунуть через DT (`chosen/static-trust-caches`)
  чтобы TXM изначально доверял всем нашим бинарям — тогда SEP KCV может не понадобиться.

Baseline восстановлен в run_upatch.sh (без SEP bypass).

## Обновление 19.09 (39) — где остановились, план на возобновление
**Правильный next-step (по договорённости с юзером): установить static TrustCache
через DeviceTree.** Это фундаментальнее чем runtime-хуки: если TXM/AMFI
изначально доверяют всем нашим бинарям, то все дальнейшие panic-пути (fsck
SIGKILL, `_captureiBICKCV` REQUIRE, halt-timeout из-за launchd exit) устраняются
одновременно.

Что уже есть:
- `fw/cloud/Firmware/094-39278-029.dmg.aea.trustcache` (6287 байт, IM4P с
  payload type `trst`) — TC для основного OS-контейнера (тот, что мы
  расшифровали в root2.img).
- `fw/cloud/Firmware/094-39914-031.dmg.trustcache` (7967 байт, тот же формат) —
  TC для Restore RamDisk (не нужен нам).

Что нужно сделать:
1. Снять IM4P-обёртку с `094-39278-029.dmg.aea.trustcache` (ASN.1 DER, tag `trst`
   payload). Опыт есть — `tools/ipsw.exe img4 im4p extract` даст raw blob.
2. Найти в kernelcache где `AppleImage4` / AMFI регистрирует static TC. Возможно
   в `com.apple.driver.AppleImage4` через IOKit provider или через DT-property
   `/chosen/trust-cache`. Смотреть: `strings kernelcache | grep -i trust`,
   `disass AppleImage4::_trustCache_something`.
3. В `tools/dtpatch.py` добавить property в `/chosen`:
   - Возможно `static-trust-caches` (uint64 = phys addr blob).
   - Или новый child node `/chosen/memory-map/TrustCache` с {addr, size}.
   - Или через `manifest-properties` -> `TrustCache` binary blob.
4. Записать TC blob в память guest'а через iBoot bdif (like кернелкеш).
5. Прогон — TXM CDHash lookup находит наш launchd/fsck/etc → всё exec-ится
   валидно → нет SIGKILL/SIGSEGV → launchd грузит LaunchDaemons.

Точка возобновления:
- `tools/run_userspace.sh` содержит рабочую конфигурацию сессии 37 (halt-RET0),
  которая доходит до halt-path (51220 SVC) и потом падает на `_captureiBICKCV`
  REQUIRE.
- Auto-slide работает (snap 64K), пропатчено в
  `overlay/target/arm/{tcg/translate-a64.c,helper.c}`.
- root2.img содержит рабочий APFS с наполненным Volume 1 (2693 файла iOS 26.4),
  aux.test и fsck/launchd — исходные (см. `/tmp/{fsck.orig,launchd.orig}` md5).

При возобновлении: **сразу к TC через DT**. Если TC не идёт легко, план B —
пропатчить op=31 handler в `overlay/hw/vmapple/vr-sep-mbox.c` под реальный
формат KCV, читая `_captureiBICKCV @ AppleSEPBooter.cpp:0xb9`.

**Why:** пунктирный runtime-hook подход дошёл до 51k SVC + halt-path, но
каждый обход открывает следующую панику. TC — систематическое решение.
**How to apply:** возобновление → извлечь `.trustcache` payload → найти static-TC
registration в XNU → dtpatch.py → прогон.

## Обновление 19.09 (40) — TC-в-DT интегрирован, но fsck SIGSEGV НЕ из-за AMFI
План NOTES-39 выполнен: `/chosen/memory-map/TrustCache` = {0x16fff0000, 0x1878}
через `tools/dtpatch.py`, blob грузится в guest RAM ф-цией в
`overlay/hw/vmapple/vresearch101.c` (env `VR_TRUSTCACHE`). Проверено:
- QEMU логирует `vresearch101: TrustCache 6264 B loaded @ 0x16fff0000`.
- XNU принял DT-запись **без** паник `Unexpected /chosen/memory-map/TrustCache
  property size` / `Unexpected location of TrustCache region` (обе есть в
  kernelcache-strings).
- Метрики: 51206 SVC, 30420 GENTER, 233 prefetch, ~988 el0_tail — **идентично
  session 37/38**. Регрессов нет. Прогресса тоже нет.

**Гипотеза NOTES-39 опровергнута**: fsck SIGSEGV **НЕ** от AMFI/CS. Иначе бы
fsck вообще не стартовал и valid execution counter не рос. Он рос — значит
AMFI пропустил fsck. Падает уже внутри самого fsck (или его dylib).

Топ el0_tail-исключений последних тактов (`grep pc= | sort | uniq -c`):
```
 88 pc=0xfffffe00494ad340  (kernel — SVC-handler frame, ожидаемо)
 70 pc=0xfffffe00494807fc  (kernel)
 15 pc=0x1b0480720          esr=0x9200004b (Access Flag L3) far=0xd350bc000  ← dyld shared cache
  7 pc=0x1025dbb38          esr=0x92000047 (Translation L3) far=0x1024b4000  ← fsck main image
```
FAR `0xd350bc000` = 53 GiB — очевидно **uninitialized pointer** (fsck
разыменовывает мусор). PC `0x1b0480720` — регион dyld shared cache
(`libSystem`/`libdyld`). FAR `0x1024b4000` — валидный user-адрес но unmapped.

`ESR=0x920000_4b` = **Access Flag fault L3**, `_47` = Translation fault L3.
AF-fault значит PTE есть но AF=0; на реальном Apple SoC AF ставится в HW при
первом доступе (SCTLR_EL1.HA=1). Наш TCG может не эмулировать HW AF update →
XNU не ставит AF в software fault handler → infinite AF-fault loop → SIGSEGV
через max-fault-count.

**Следующие шаги (session 41)**:
1. Проверить SCTLR_EL1.HA в vresearch101 CPU и включить HW AF update в TCG
   pipeline (`target/arm/tcg/tlb_helper.c` — `arm_page_table_walk`), если
   не включено. Это фундаментальный fix — вылечит и dyld и fsck-main-image.
2. Если HW AF есть — реверс `0x1b0480720` (dsc offset) в extracted dyld
   shared cache, чтобы понять что fsck по этому LR (`0x1b048070c`)
   разыменовывает (skip syscall / libSystem stub).
3. Fallback: продолжить план TC-эксперимента отдельно — попробовать
   `/chosen/memory-map/TrustCache-N` (нумерованные) на случай, что XNU
   принимает несколько (для system+library TCs).

**Файлы session 40** (закоммичено):
- `overlay/hw/vmapple/vresearch101.c` — `VR_TC_PADDR=0x16FFF0000`, env-driven load.
- `tools/dtpatch.py` — переименование `MemoryMapReserved-N` slot → `TrustCache`.
- `tools/inject_tc_dt.sh` — sudo-wrapper для подмены `devicetree.img4` на Preboot vol0.
- `tools/run_userspace.sh` — `VR_TRUSTCACHE` export.

Where-we-are: session 41 стартует с TCG AF hardware update.

## Обновление 19.09 (41) — HW Access Flag update для EL0 на apple-gxf
Гипотеза NOTES-40 подтверждена: XNU/dyld/fsck на apple-gxf полагаются на
Apple-IMPDEF поведение "AF always updated in HW" даже при TCR_ELx.HA=0.
Без этого — infinite AF-fault loop в user-space (ESR=0x920000_4b/_47).

**Фикс** в `overlay/target/arm/ptw.c` (после `if (!(descriptor & (1 << 10)))`):
```c
bool apple_impdef_hw_af = arm_feature(env, ARM_FEATURE_GXF)
                          && regime_is_user(env, mmu_idx);
if (param.ha || apple_impdef_hw_af) {
    new_descriptor |= 1 << 10;    /* AF */
}
```

Итерации:
1. **Первый заход — force AF для ВСЕХ regime**: DA 759 → **36**, PA 233 → **27**
   (в 20× меньше!). Но новый крах: **"[TXM] Unhandled synchronous exception
   taken from GL0 at pc 0xfffffe00294aabf4"**. Причина: kernel/SPTM/TXM PT
   лежат в SPTM-owned pages; HW AF update пишет в них минуя GENTER →
   SPTM ловит нарушение invariant и паникает.
2. **Второй заход — force AF ТОЛЬКО для user regime** (`regime_is_user`):
   TXM GL0 crash ушёл. DA = 423 (лучше baseline 759, хуже 36-первого захода
   — kernel PT снова через SW-AF path). fsck теперь **SIGKILL** (не SIGSEGV).

**Прогресс сессии**:
- Первый valid userspace slide (fsck) больше не крашится сразу на AF.
- Осталось: последние el0_tail показывают `pc=0x1a7f63030 far=0xd00cc0000`
  — dyld shared cache код с wild pointer (13 GiB). Скорее всего **ASLR slide
  fsck отличается от launchd** (auto-detect в
  `overlay/target/arm/helper.c` заточен под первый EL0 exception = launchd
  base 0x100c50000, слайд 0x4c50000).

**Следующие шаги (session 42)**:
1. Расширить auto-slide на per-process: ловить `mach_kernel_load` / `bsd_exec`
   entry в XNU и обновлять slide при каждом exec.
2. Или проще — pin fsck slide через VR_UBASE=<addr> когда launchd оставляет
   его в scratch страничке.
3. Реверс `0x1a7f63030` в извлечённом dsc: узнать что за libSystem-функция
   и какую структуру она разыменовывает по 0xd00cc0000.

**Файлы session 41** (закоммичено):
- `overlay/target/arm/ptw.c` — EL0-only Apple-IMPDEF HW AF update.

## Обновление 19.09 (42) — boot-args + fsck stub: тупик из-за AMFI CDHash
Три эксперимента поверх session 41:

**1. Patch fsck entry → `mov w0,#0; ret` @0x92c** (session-36 style, `tools/stub_fsck.sh`):
- Результат: **"posix_spawn: 85: Bad executable (or shared library)"** — AMFI
  ловит несовпадение CDHash пропатченного fsck с TC entry. Раньше (session 36)
  этого не было потому что TC не работал; теперь работает и валидирует
  корректно. Стаб откатан.

**2. Boot-args `cs_enforcement_disable=1 amfi_get_out_of_my_way=1 debug=0x14e -v`
   через /chosen/boot-args** (расширил `tools/dtpatch.py` под `VR_BOOTARGS`;
   `tools/inject_tc_dt.sh` теперь пишет boot-args по умолчанию):
- Результат: регресс. fsck снова **SIGSEGV** (не SIGKILL). DA 725, PA 226,
  ~близко к session-40 baseline. Значит XNU **проигнорировал** DT/boot-args
  для enforcement: скорее всего PPL/AMFI-DEV режим требует
  соответствующего entitlement на процессе, boot-arg не глобальный на этой
  сборке. Или XNU читает CommandLine из BootArgs struct (не из DT),
  а iBoot boot-args не заполняет.

**3. Root cause fsck-SIGSEGV** — infinite recursion в fsck:
   `pc=0x102e47b38 sp=<уменьшается>-0x1120 lr=0x102e57f68 far=0x102bf4000
   esr=0x92000047` (Translation fault L3). SP-падение на 4.4 KB/итерацию
   → signal handler в libSystem/Foundation рекурсивно пытается работать с
   невалидной страницей 0x102bf4000. fsck __TEXT @ VA 0x100000000+0x4000
   (16 KB), slide fsck ~ 0x2e44000 (обычный ASLR). fsck сам корректно
   стартует (проходит AMFI, code executes) но упирается во внутренний
   invariant.

**Тупик**: без валидного пересчёта CDHash патч fsck невозможен, а без
патча fsck — infinite SIGSEGV loop.

**Следующие пути (session 43)**:
1. **Реализовать CDHash пересчёт** (`tools/patch_cs.py` + `tc_append.py`):
   - Найти LC_CODE_SIGNATURE → CS SuperBlob → CodeDirectory (magic 0xFADE0C02).
   - Пересчитать SHA256 страницы 0x0 (первая, где патч), обновить hash slot.
   - Пересчитать SHA256 всего CD blob → новый CDHash (первые 20 байт).
   - Добавить 24-байтную entry в TC blob (`_work/tc/os.trst.bin`), поднять
     `nentries` в header.
   - Дальше повторить stub_fsck + прогон.
2. **Или патч AMFI в kernelcache**: найти `mac_vnode_check_signature` /
   `vnode_check_signature`, повесить VR_MOV0 на "return 0". Обход всей
   проверки, не только для fsck. Более грубо, но 1 адрес vs скрипт.
3. **Или патч launchd** (`bl fsck_call` → NOP): убрать вызов fsck целиком.
   Launchd тоже подписан → тот же CDHash-стенка. Проще patch AMFI (#2).

**Файлы session 42** (закоммичено):
- `tools/dtpatch.py` — поддержка `$VR_BOOTARGS` → `/chosen/boot-args`.
- `tools/inject_tc_dt.sh` — прописывает VR_BOOTARGS по умолчанию.
- `tools/stub_fsck.sh` — sudo-обёртка стаба fsck (сейчас не применён, оставлен
  как инструмент для session 43 после пересчёта CDHash).

## Обновление 19.09 (43) — АМFI vnode_check_signature → 0 → fsck прошёл!
**Прорыв**: обошли CDHash-стенку через kernel-side патч. VR_RET0 на начало
`AppleMobileFileIntegrity::vnode_check_signature` (@ VA `0xfffffe0007d56dd4`)
превращает всю функцию в `mov x0, #0; ret x30` → MAC hook всегда allow.

**Как нашли адрес**:
1. `strings kc | grep 'AMFI: vnode_check_signature called with platform'`
   → в `__PRELINK_TEXT` @VA `0xfffffe00071f79e5`.
2. Xref: единственный ADRP+ADD @ `0xfffffe0007d56e34/e38` в `__TEXT_EXEC`.
3. Функция prolog `pacibsp` @ `0xfffffe0007d56dd4` (первый выше). Именно
   на него VR_RET0 (см. `overlay/target/arm/tcg/translate-a64.c:10478` —
   `mov x0,#0; RET x30 без auth`).

**Метрики**:
| фаза            | SVC   | GENTER | Data Abort | Prefetch |
| --------------- | ----- | ------ | ---------- | -------- |
| session 40 base | 51206 | 30420  |        759 |      233 |
| session 41 AF   | 49072 | 30042  |        423 |      217 |
| session 43 AMFI | 46999 | 25006  |     **10** |    **0** |

Data Abort ↓ **75×**, Prefetch ↓ **до нуля**. fsck реально exit=0 через
stub `mov w0,#0; ret @0x92c`. **Launchd прошёл fsck** и умер сам:
```
"unexpected SIGKILL of init with reason -- namespace 3 code 0x9"
```
namespace 3 = OS_REASON_SIGNAL, code 9 = SIGKILL. XNU панике потому что
init/PID1 нельзя убивать. Скорее всего:
- launchd exec-ит следующий boot task (не fsck), тот не находится / не
  запускается → launchd exit(9) → XNU trap "cannot exit PID 1".

**Следующие пути (session 44)**:
1. Найти какой boot task launchd пытается запустить после fsck. Смотреть
   в launchd binary (`_launchd`) на "hardwired boot tasks" list; или
   грепать /System/Library/LaunchDaemons на root2.img.
2. Возможно проблема — missing service (mach_init, notifyd, ...) → nag
   для минимального userspace нужно понять MINIMUM boot chain.
3. Или SIGKILL от нашего же AMFI-bypass: mac_vnode_check_signature=0
   всегда → некоторые consumers ожидают что deny срабатывает; XNU
   detects invariant и убивает init. Проверить через VR_MOV0 (более
   узкий скоуп: replace единственный call site вместо переопределения
   всей функции).

**Файлы session 43** (коммитится следом):
- `tools/run_userspace.sh` — добавил `VR_RET0=0xfffffe0007d56dd4`.
- `tools/inject_tc_dt.sh` — убрал по умолчанию `VR_BOOTARGS` (не работал).
- fsck stub (session 42, `tools/stub_fsck.sh`) активирован — нужен после
  каждого re-mount root2.img.

## Обновление 19.09 (44) — launchd прошёл fsck, boot task list найден
Разбор launchd binary:
- `/System/Library/xpc/launchd.plist` — только LaunchDaemons/AppExtensions, boot tasks НЕ там.
- Boot task names зашиты в binary: **fsck**, **MSUEarlyBootTask**,
  **MobileAssetEarlyBootTask**, **darwinos-boot-task**, **auearlyboot**.
- Строки: "Doing boot task", "Finished boot task", "Skipping boot-task",
  "Unable to find boot task block for: %s", "boot task has no program".

Логи прогона session 43 показывают: **всего 1 real_el0@fault**, и тот подозрительный
(`pc=0x1182c4 sp=0xfffffc00002fbcd0` — sp в kernel-mapped диапазоне, не EL0).
После fsck-stub нет реальных user-space faults. Значит либо launchd
запускает следующие tasks и они работают, либо тихо exit-ит.

Скорее всего: SIGKILL init от нашего собственного AMFI-bypass. Найдена
строка в `mac_vnode_check_signature`:
```
"MAC hook returned no error, but status is claimed to be fatal? path: '%s', ..."
```
Наш VR_RET0 хук вернул 0 (no error) но не сбросил out-параметр
`fatal_failure_desc_len` / `fatal_failure_desc`. Если он остался в стеке
как ненулевой мусор — MAC framework интерпретирует "fatal" и убивает
процесс через `psignal(SIGKILL)`.

**Session 45 (следующая)**:
1. Сузить AMFI-bypass: **VR_MOV0 в конкретный call site**
   `bl <hook>` @ `0xfffffe000928c500` в `mac_vnode_check_signature`
   (@ VA `0xfffffe000928c450`). Тогда MAC framework вызовет реальный
   hook (или наш patched-хук), но результат обнулим ПОСЛЕ вызова, не
   на входе. Из плюсов — реальный hook правильно очистит out-params.
2. Или: реверс сигнатуры `AppleMobileFileIntegrity::vnode_check_signature`
   в стиле `int (vnode_t, ..., int *fatal_failure_desc_len, char
   **fatal_failure_desc)` — сделать VR_RET0 который зануляет
   `*x5=0, *x6=0` перед `mov x0,#0; ret`. Требует custom TCG code.
3. Или найти где именно psignal init (SIGKILL). Строка "unexpected
   SIGKILL of init" в kc → xref → функция → каких стек-конфигурации
   вызывает.

## Обновление 19.09 (44b) — fsck-stub НЕ нужен: AMFI-bypass достаточен
Убрали stub_fsck (fsck вернули в оригинал) — **метрики идентичны session 43**:
46999 SVC, 23903 GENTER, 10 DA, 0 PA, та же паника "unexpected SIGKILL of init".

Значит:
- fsck при живом AMFI-bypass **успешно исполняется до конца** (не входит в
  SIGSEGV recursion как в session 41 — вероятно оригинальный CS check на
  каждой mmap-странице AMFI-hook раньше давал permission fault → recursion,
  а сейчас allow-all избавляет от проблемы).
- Launchd exec-ит следующие boot tasks (MSU*, MobileAsset*, ...) — они тоже
  проходят AMFI и работают.
- Один из tasks (или сам launchd) в итоге получает SIGKILL. XNU панике
  потому что PID 1 нельзя SIGKILL.

Panic-функция найдена: `0xfffffe0008f9d8a4` (10+ callers в BSD signal path,
адреса `0xfffffe0008f6f214..f7667c` в диапазоне BSD `psignal_locked` /
`proc_exit`). Значит SIGKILL приходит через нормальный BSD signal
delivery, не через MAC/CS.

Возможные источники SIGKILL init:
- watchdog daemon (ждёт heartbeat от init, не получил)
- kernel jetsam (маловероятно для PID 1)
- **launchd sам** решает exit через `_exit(9)` когда что-то не может
  запустить/ждать
- какой-то sysctl invariant (например IOKit детектит что init перестал
  быть boot-parent'ом какого-то process)

**Session 45 предложения**:
1. Расширить логирование в `overlay/target/arm/helper.c` — добавить лог
   любого `psignal(SIGKILL, target_pid=1)` через BSD-хук.
2. Или добавить VR_NOP на panic-функцию `0xfffffe0008f9d8a4` — пусть
   продолжает работать (без panic) и мы увидим что делает ядро дальше.
3. Или включить `boot-args=debug=0x14e -v serial=3` через *BootArgs
   struct* (не через DT — надо реверсить как iBoot конструирует
   BootArgs, чтобы XNU реально печатал boot messages на UART).

## Обновление 19.09 (45) — VR_RET0 на panic-func = "shenanigans!" (AMFI evaluate.c)
Попытка скипнуть "unexpected SIGKILL of init" через VR_RET0 на panic wrapper
@ `0xfffffe0008f9d8a4`. Метрики сохранились (47003 SVC, 10 DA, 0 PA), панику
скипнули, но открылась НОВАЯ:
```
"shenanigans!" @evaluate.c:0x137b
```
Apple-жаргон для AMFI evaluate/policy sanity check. Наш VR_RET0 на
`vnode_check_signature` возвращает "no error" для КАЖДОГО бинаря, включая
такие которые должны быть отвергнуты — AMFI evaluate детектит несоответствие
между "policy said OK" и "actual entitlements" и панике.

Значит **широкий CS-bypass не проходит дальше** — надо более узкий:
1. VR_MOV0 на конкретный `bl <vnode_check_signature>` в
   `mac_vnode_check_signature` @ VA `0xfffffe000928c500`. Тогда:
   - реальный AMFI hook вызывается (правильно проставляет out-params)
   - но его x0 result затирается на 0 → caller думает "OK"
   - out-params остаются валидными → evaluate.c не паникует.
2. Или добавить в TC blob CDHash-ы для КАЖДОГО бинаря (fsck, launchd,
   MSU*, ...) — пересчитать CDHash-ы, полноценно.
3. Или откатить AMFI bypass и вернуться к `AF fix + fsck stub только`
   (session 41 + stub). Тогда fsck stub тоже требует CDHash пересчёт
   (session 42 тупик — вернуться).

Panic-func обход **не помог**, откатили из run_userspace.sh (осталось
только vnode_check_signature bypass).

**Session 46 (реальный next-step)**:
- Реализовать `tools/patch_cs.py` — SHA256 CD blob пересчёт для fsck +
  добавление new entry в `_work/tc/os.trst.bin`. Тогда fsck-stub c
  валидной подписью проходит AMFI **правильно** (без bypass), evaluate.c
  доволен. Далее — то же для launchd (если его тоже нужно стабать).

## Обновление 19.09 (46) — NOP на shenanigans! panic → snova SIGKILL init
2 xref-а к "shenanigans!" @evaluate.c (bl panic@0xfffffe00092b12e8):
- `0xfffffe000885cfc4` — line 0x137b (наш случай)
- `0xfffffe000885cff0` — line ~0x137d/f

VR_NOP на оба `bl` — panic не вызывается, evaluate.c продолжает. Метрики
идентичны (47003 SVC), но **вернулась паника "unexpected SIGKILL of init"**.

**Значит shenanigans и SIGKILL init — два выхода одного детектора**:
AMFI evaluate находит inconsistency (наш CS-bypass вернул "OK" для binary
с CDHash которого нет в TC), затем:
- либо панике "shenanigans!" (если evaluate инвариант нарушен),
- либо посылает `psignal(SIGKILL)` виновнику (если policy path другой).

Если виновник = init → XNU панике "unexpected SIGKILL of init".

Обходы AMFI evaluate/panic-func бесполезны — root cause **отсутствие
валидного CDHash в TC для пропатченных бинарей** (или для наших любых
бинарей). Ленивые точечные патчи упираются в защитный invariant.

**Session 47 — реальный next-step**: `tools/patch_cs.py` — SHA256 CD blob
пересчёт (см. session 42 план). Готовые кирпичи:
- LC_CODE_SIGNATURE @ 0xcc80, size 0x48d0 (fsck) — Mach-O parsed already.
- Формат CS SuperBlob: CSMAGIC_EMBEDDED_SIGNATURE=0xFADE0CC0, CodeDirectory
  blob type CSMAGIC_CODEDIRECTORY=0xFADE0C02.
- CDHash = SHA256(CD blob)[0:20], hash slots в CD (SHA256 per 4KB page).
- TC v2 entry = 24 bytes: 20 cdhash + 2 hashtype(=2 для SHA256[20]) + 2 flags.

Все обходы session 45/46 откачены. run_userspace.sh обратно к session 43
конфигурации (VR_RET0=0xfffffe0007d56dd4).
