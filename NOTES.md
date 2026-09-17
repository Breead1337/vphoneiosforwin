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
