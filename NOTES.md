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
