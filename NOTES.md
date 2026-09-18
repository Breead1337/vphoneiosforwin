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

