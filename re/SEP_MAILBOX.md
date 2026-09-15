# VZ vresearch1 SEP mailbox — reversed from AVPBooter.vresearch1.bin

MMIO base (DT `sep` reg): **0x30250000** (arm-io 0x10000000 + 0x20250000). IRQ SPI 0x14/0x15.

## AP-side driver structures (in guest RAM)
- **Mailbox object array @ 0x70028a30**, stride **0x1a0**, up to **3** objects (idx 0..2).
  - `+0x00` (u64): MMIO base pointer (= 0x30250000)                [FUN_00106748: `*obj + off`]
  - `+0x10` (u64): secondary base (DMA/ring region)                [FUN_00106788: `*(obj+0x10)+off`]
  - `+0x140` (u16): mailbox TYPE = **0x101** or **0x200** (version/kind)
  - `+0x142` (u8): flag (enables timestamp write block)
  - `+0x143` (u8): bit0 flag (skip-body when set)
  - `+0x145` (u8): ==1 → actually enqueue message into ring (FUN_00106674)
  - `+0x174` (u32): MMIO **doorbell** register offset (AP writes 0x10 here)
  - `+0x178` (u32): MMIO register offset (send index / status; read+masked)
  - `+0x17c` (u32): MMIO reg offset ← timestamp low  (from cntpct FUN_00100370)
  - `+0x180` (u32): MMIO reg offset ← timestamp high
  - validity: `*(short*)(obj+0x140) != 0`
- **Message ring base @ 0x70028a00** (param to enqueue FUN_00106674).
- `_DAT_7002add8`: saved token used around enqueue (FUN_00106b20).

## Send path (AP → SEP)   FUN_001063dc → FUN_00106674 → FUN_0010d450
1. Validate obj type (0x101/0x200), obj[0]!=0.
2. If type has bits 0x60: program an address reg via FUN_00106640 (OOL/DMA addr, masked 0xffffff800).
3. If `+0x142`==1: read reg[+0x178], clear bit1, write cntpct → reg[+0x17c]/reg[+0x180], set reg[+0x178] |= 2. (timestamped kick)
4. If `+0x145`==1: FUN_0010d450 writes the message descriptor into ring@0x70028a00.
5. Write **0x10** to doorbell reg[+0x174]  (this is the MMIO 0x18/0x200 pokes seen live).

## Recv path (SEP → AP)   FUN_0010d5c4  (the busy-wait we hit)
Reads response entries from the mailbox object's sub-ring:
- `obj[8]` (u64 at +0x40) = current entry ptr, bounded by `obj[9]`(+0x48)/`obj[10]`(+0x50).
- `entry` fields: `entry[0]`(off) → `word = *(obj[0]+ *entry)`;  `entry[1]`(+4)=?, `entry[2]`(+8)=payload offset.
- Check `word & 0xC0000` != 0 → **panic 0x81** (error bits set in slot).
- Check `word & 0x10000` (bit16): if clear → a 16-byte payload is ready:
  copies 16 bytes from `*(obj[0..? ) + entry[2]` (actually `*obj + payload_off`) into caller buf x23, clears +0xc, calls FUN_0010d814 (commit/advance), returns 0.
  if set → not ready; if w27==0 return -1 (nonblocking); else check timeout (FUN_001280c8, deadline from cntpct) → on timeout FUN_0010d844(0xAE) return -2.
- Timeout source: FUN_001280a0 = read cntpct (thunk_FUN_00100370) → time now; FUN_001280c8(deadline,delta)= now-deadline>=delta.

## Live MMIO trace (current latching stub)
```
w 0x10<-1 ; w 0x14<-0x80000000 ; r 0x14->0x80000000 ; w 0x18<-0x1111
w 0x200<-0x367ff ; w 0x208<-0 ; r 0x1c ; r 0x20 ; r 0x100 ; r 0x108 (polls forever)
```
Interpretation: 0x10/0x14 = IOP doorbell + status(bit31=ready). 0x18 = message word / kick.
0x200/0x208 = 64-bit AP→SEP register (msg or OOL index, 0x367ff). 0x100/0x108 = 64-bit SEP→AP.
0x1c/0x20 = SEP status/index polled for response.

## What the SEP model must do (next step)
On doorbell (write to the offset AVPBooter uses, i.e. 0x18 and/or 0x200):
1. Read the message descriptor AVPBooter wrote into ring@0x70028a00 (format TBD from FUN_0010d450 params).
2. Produce a BOOTSTRAP response (Inferno sep-sim.c: op 1 PING→101 PING_ACK, 2 GET_STATUS→102,
   3 GENERATE_NONCE→103, 5 BOOT_TZ0→105, 6 BOOT_IMG4→106, 7 LOAD_ART→107 ...).
3. Write response entry into the object sub-ring (obj[8] slot) with word bit16=0, error bits clear,
   16-byte payload at obj+entry[2]; advance index reg 0x100/0x1c; raise SEP IRQ (SPI 0x14).

## Still TODO to reverse
- Exact ring descriptor / entry stride at 0x70028a00 and obj[8] sub-ring (from FUN_0010d450 full params + the enqueue).
- Which MMIO offset is the response-ready index the recv polls (0x1c vs 0x100).
- 64-bit message word bit layout (endpoint/tag/opcode) — cross-check Inferno sep-sim KeystoreMessage / message union.

## LIVE RAM dump (added dump_ram on doorbell)
Early doorbell (0x18/0x200) writes fire BEFORE the obj array @0x70028a30 is populated (all zero there).
ring@0x70028a00 header = { u64 0x0013da03, u64 0x0013dcb8, u64 0x68 } → a C++ message object:
- 0x13dcb8 = ROM **class descriptor**: {0x13d320, 0x13dcb9, inst=0x700289ec, size=**0x1a0**, 0x2b}
  (size 0x1a0 == mailbox object stride → this class IS the mailbox object; instances ~0x700289ec).
- 0x13da03 = ROM descriptor: {0x13da01, inst=0x700285e8, 0x90, 0x1b, 0x10, 0x01}.
CONCLUSION: the SEP mailbox driver is fully C++/OO; messages are objects with ROM vtables/class
descriptors, serialized via vtable call in FUN_0010d450. Synthesizing valid SEP responses requires
reversing the serialization + the response object layout — multi-session effort. Fastest route is
likely to emulate at the *transport* level (indices+IRQ+payload copy) once the on-wire ring entry
(post-serialization) is captured, rather than modeling the C++ objects.

## РЕЗУЛЬТАТ: транспортный ответчик работает
Формат сообщения РАСКРЫТ: SEP msg = LE u64 { u8 ep; u8 tag; u8 op; u8 param; u32 data }.
Регистры: 0x200 = AP→SEP request word; 0x100/0x108 = SEP→AP response (16B); 0x1c/0x20 = status
(bit16=не готово, 0xC0000=ошибка; 0 = готово); 0x10/0x14/0x18 = ранний хендшейк (0x14 bit31, 0x18=0x1111).
Первый запрос = 0x367ff = ep 0xFF (BOOTSTRAP), tag 0x67, op 3 (GENERATE_NONCE).

Реализован ответчик (overlay/hw/vmapple/vr-sep-mbox.c): на запись 0x200 парсит запрос,
отвечает op = req_op+100 (BOOTSTRAP), кладёт слово в 0x100, статус 0x1c/0x20=0, дёргает IRQ.
→ AVPBooter ПРИНЯЛ ответ (op 103 NONCE_GENERATED), прочитал 0x100 -> 0x6767ff, и ПОШЁЛ ДАЛЬШЕ.

Дальше гость входит в FUN_0011b730 = большая SIMD-хеш-функция (измерение/проверка образа
secure boot). Это легитимная работа, медленная под TCG; за 90с реального времени не завершилась,
новых обращений к устройствам нет. Т.е. SEP-барьер #1 (nonce) пройден, идёт крипто-фаза.

## Следующее (по нарастающей)
- Дать корректные данные nonce (сейчас 0) и дождаться следующих BOOTSTRAP-операций:
  GET_NONCE_WORD(4)→104, BOOT_TZ0(5)→105 (загрузка SEP firmware AVPSEPBooter), BOOT_IMG4(6)→106.
- Возможно понадобится реально отдать образ TZ0/SEPFW в OOL-буфер (CONTROL_OP_SET_OOL_*).
- После secure-boot фазы AVPBooter грузит следующий образ (iBoot-эквивалент / kernelcache) с bdif-диска.

## Диагноз пост-nonce (200с прогон)
За 200с реального времени НЕ завершается, новых I/O нет → это runaway-цикл, не «медленно».
Горячие функции: FUN_0011b730 = SHA-компрессия (SIMD), FUN_001399c0 = SHA-финализация
(padding 0x80, big-endian swap дайджеста). Т.е. AVPBooter считает measured-boot SHA над регионом
в RAM, и хеш уходит в разнос — вероятно из-за неверной длины/потока (не настроены OOL-буферы SEP
и данные до GENERATE_NONCE). Ответ op=103 приняли, но одного ответа мало.

ВЫВОД: нужен ПОЛНЫЙ VZ-SEP bootstrap (правильные данные nonce + OOL + последовательность операций),
а не заглушка op+100. Это дни реверса клиента SEP в AVPBooter либо запуск реального AVPSEPBooter.

---

## Сессия 15.09 — мастер-таблица сообщений + формат кадра + транзакция

Отреверсен уровень ВЫШЕ транспорта: драйвер сообщений AP. Ключевое — найдена таблица
описаний всех типов сообщений SEP и точный 16-байтный формат кадра запрос/ответ.

### Драйвер (цепочка вызовов)
```
FUN_00105374 (boot stage)  -> FUN_00104438(stage)         issue сообщений на этапе загрузки
FUN_00104438               -> FUN_00106d50                до 8 повторов транзакции
FUN_00106d50               -> FUN_00106e0c                ОДНА транзакция (send + wait resp)
FUN_00106e0c               -> FUN_001063dc(2,..)          arm/select mailbox #2
                           -> FUN_001070b4(idx,sub,..)    собрать кадр в буфер 0x7002abd0
                           -> FUN_001068ac(2,..,0x10,..)  ФИЗ. обмен 16 байт (vtable)
                           -> FUN_00107124(idx,..)        ждать ответ с нужным op
                           -> FUN_00111154(..)            вычитать OOL-данные в буфер вызывающего
```

### Мастер-таблица сообщений @0x13dd20 (ROM off 0x3dd20), 32 записи × 0x38
Раскладка записи:
- `+0x00` u8  — **req op** (id сообщения)
- `+0x01` u8  — **resp op = req op + 100** (подтверждено на уровне данных)
- `+0x02` u8  — под-селектор кадра (кладётся в кадр, см. ниже)
- `+0x03` u8  — размер элемента OOL: {0,1,4}
- `+0x04` u32 — **таймаут ответа, мкс** (1e6/2e6/5e6/10e6 = 1/2/5/10 с)
- `+0x08` u32 — **длина OOL-данных** (0 если данных нет)
- `+0x0c` u32 — one-time флаг (разовая задержка/инициализация перед первой отправкой)
- `+0x30` u8  — bit0: «без ожидания ответа»

Декодированные записи (только заполненные):

| idx | req op | resp op | esz | timeout | datalen | назначение (гипотеза) |
|----:|:------:|:-------:|:---:|--------:|--------:|-----------------------|
| 0  | 0x01 | 101 | 0 | 1s  | 0   | PING |
| 1  | 0x02 | 102 | 0 | 1s  | 0   | GET_STATUS |
| 2  | 0x03 | 103 | 0 | 1s  | 0   | GENERATE_NONCE |
| 3  | 0x04 | 104 | 1 | 1s  | 20  | **читать nonce (20 B OOL)** |
| 4  | 0x0a | 110 | 0 | 1s  | 0   | |
| 5  | 0x0f | 115 | 0 | 2s  | 0   | |
| 6  | 0x10 | 116 | 0 | 2s  | 0   | |
| 13 | 0x05 | 105 | 0 | 5s  | 0   | BOOT_TZ0 |
| 14 | 0x06 | 106 | 0 | 5s  | 0   | BOOT_IMG4 |
| 15 | 0x14 | 116 | 0 | 2s  | 0   | |
| 16 | 0x12 | 114 | 0 | 2s  | 0   | (one-time) |
| 17 | 0x13 | 115 | 0 | 2s  | 0   | |
| 18 | 0x15 | 117 | 0 | 2s  | 0   | |
| 19 | 0x20 | 132 | 0 | 10s | 0   | (one-time) |
| 20 | 0x16 | 118 | 0 | 2s  | 0   | |
| 21 | 0x19 | 125 | 0 | 10s | 0   | (one-time) |
| 22 | 0x1a | 126 | 4 | 2s  | 64  | **64 B OOL** |
| 23 | 0x1b | 127 | 0 | 2s  | 0   | |
| 24 | 0x11 | 113 | 0 | 2s  | 0   | |
| 25 | 0x17 | 123 | 0 | 5s  | 0   | (one-time) |
| 26 | 0x18 | 124 | 0 | 5s  | 0   | (one-time) |
| 27 | 0x1c | 128 | 0 | 10s | 0   | (one-time) |
| 28 | 0x1d | 129 | 4 | 2s  | 144 | **144 B OOL** |
| 29 | 0x1e | 130 | 0 | 2s  | 0   | |
| 30 | 0x1f | 131 | 4 | 2s  | 32  | **32 B OOL** |
| 31 | 0x23 | 135 | 0 | 2s  | 0   | |

(idx 7..12 нулевые.) Индекс в таблице — НЕ op; op лежит в `+0x00`.

### 16-байтный кадр запроса (буфер @0x7002abd0, строит FUN_001070b4)
- `[0]` = **0xFF** (ep = BOOTSTRAP), константа в начале FUN_001070b4
- `[1]` = tag  (= descriptor `+0x02`)
- `[2]` = **op** (= descriptor `+0x00`, req op)
- `[3]` = param (под-индекс/counter; для многоэлементных = esz*chunk)
- `[4:8]`  = data32 (param_3)
- `[8:16]` = extra (param_4)

Сверка с live: первый запрос `0x367ff` = байты LE `ff 67 03 00` → ep 0xFF, tag 0x67, **op 0x03**
(GENERATE_NONCE), data 0. Совпало.

### Кадр ответа (16 байт, читает FUN_00107124)
Приходит через FUN_00106820 (vtable-обмен) в локальный буфер:
- `resp[2]` = **op ответа**; должен равняться descriptor `+0x01` (= req op + 100).
- `resp[2] < 200`  → успех; результат копируется из 0x7002abd0 через FUN_00111154.
- `resp[2] == 200` → продолжать ждать.
- `resp[2] == 0xFF` → ошибка (возврат 0xff).
Ретраи: на таймаут (-2) до 5 раз с добором ожидания (op+100 поллинг).

### Физический обмен = vtable (подтверждает: протокол объектный, не RTKit)
`FUN_001068ac`/`FUN_00106820` берут mailbox-объект (FUN_00106bc4), суб-объект `obj[0xf]`
(в границах `obj[0x10]..obj[0x11]`) и вызывают метод по указателю:
- send:  `*(obj[0xf] + 0x28)` → FUN_0010d450 (enqueue: пишет поля кадра в кольцо, дергает
  vtable-сериализатор `*(msg+8)`, в конце пишет сентинел **0x1111** в MMIO base + off).
- recv:  `*(obj[0xf] + 0x18)` → FUN_0010d5c4 (читает слово из MMIO base + entry[0]; bit16=не готово;
  `&0xC0000`=ошибка→panic 0x81; при готовности копирует 16 B по entry[2]).

### Что это даёт модели SEP (vr-sep-mbox.c)
Теперь известно ТОЧНО, что ответчик обязан вернуть на каждый op:
1. кадр ответа с `[0]=0xFF`, `[2]=req_op+100`, ошибки/`0xff` не ставить;
2. для op с datalen>0 — положить ровно столько OOL-байт (op4→20 nonce, op0x1a→64,
   op0x1d→144, op0x1f→32); GENERATE_NONCE(op3) сам данных не отдаёт — nonce читается
   отдельным op4.
3. соблюдать bit16-«готово» в статус-слове и поднимать IRQ SEP→AP.

### RESUME (следующий шаг)
- Снять формат КОЛЬЦА/записи (obj[8] sub-ring, entry stride) из полного FUN_0010d450 + FUN_00106bc4,
  чтобы recv увидел ответ там, где ждёт (MMIO base + entry[0]/entry[2]), а не в «плоских» регистрах.
- Дать НАСТОЯЩИЙ 20-байтный nonce на op4 и обработать OOL SET_ADDR/SIZE (descriptor esz/datalen).
- Порядок ожидаемых op на ранней загрузке снять трассой (run1 T=200, grep «sep-mbox: req»).

### Адресация объекта мейлбокса (аксессоры)
Объект возвращает FUN_00106bc4 (обёртка FUN_00106b48), выбор — по армленному индексу (mailbox #2).
- `FUN_00106748(off)` → `obj[0] + off`         — MMIO-регистр (obj[0] = base 0x30250000)
- `FUN_00106788(off)` → `*(obj+0x10) + off`     — вторичная база: кольцо дескрипторов в RAM
- `FUN_00106640()`    → `*(obj+0x18) + 0x50000` — окно OOL/DMA (сюда идут OOL-данные, напр. 20 B nonce)
Значит для op с datalen>0 модель SEP кладёт данные в регион `*(obj+0x18)+0x50000`, а recv читает
статус-слово из `obj[0] + entry[0]` (MMIO). Осталось снять init entry[0]/entry[2] (setup кольца).

### Живой трейс 15.09 — op3 ПРИНЯТ, зависание уже пост-nonce
Прогон T=30 c текущей flat-register заглушкой:
- SEP-запрос ровно один: `ep=0xff op=3` (GENERATE_NONCE).
- Гость читает ответ РОВНО ОДИН РАЗ: `0x1c, 0x20, 0x100, 0x108` — ни ретрая, ни паники
  (нет FUN_00105548 с 0x81/0x9d), ни второго SEP-op. Значит **op3-ответ принят**
  (resp[2]=103 совпал с ожидаемым req+100), хендшейк op3 пройден.
- op4 (чтение 20-B nonce) гость на этой стадии НЕ шлёт.

Профиль после ответа (T=12, `-d exec,nochain`, 211k TB):
- горячее: **0x110f9c = 117k** — это `FUN_00110f50` = **memset** (0x40-разворот);
- вперемешку `0x100040/0x100080` = векторы sync-abort/irq (ROM@0x100000) = demand-paging по ходу;
- кластер `0x119cc8..0x119d10` по ~1024 = блочный цикл (похоже SHA-компрессия);
- короткого периода в хвосте нет → не тугой 3-4-TB цикл, а тяжёлая заливка+хеш.

Вывод: барьер — НЕ транспорт op3, а **пост-nonce measured-boot**: большой memset + хеш с
непрерывными abort-векторами. Либо (а) легитимно медленный TCG-SHA большого региона, либо
(б) runaway memset из-за размера, взятого из данных, которые заглушка сейчас отдаёт нулями
(inline resp[4:16] и/или невыданный OOL). memset (FUN_00110f50) генерик — вызывающих много
(в т.ч. хеш FUN_0011b730), точный источник размера пиннится только трейсом адреса возврата.

### RESUME (уточнённый)
1. Снять, читает ли драйвер inline-поля ответа op3 (resp[4:8]/[8:16]) и куда идёт это значение
   (кандидат на «размер memset»). Отдать в заглушке ненулевой правдоподобный ответ и сверить.
2. Трейс с адресами возврата (bt/watch на 0x110f50), поймать РАЗМЕР живого memset:
   растёт ли число abort-векторов линейно со временем (runaway) или выходит на плато (медленный хеш).
3. Если нужен nonce — реализовать op4: положить 20 B в OOL-окно (obj+0x18 + 0x50000), выставить
   bit16-«готово» и IRQ; порядок op снять более длинным прогоном.

### Причина зависания найдена: runaway memset с мусорной длиной
Снят live размер аргумента memset (FUN_00110f50) через `-d cpu,exec` (дамп регистров перед TB):
- memset вызывается с **len (X2) ≈ 0xfffffc00_xxxxxxxx** (адресного масштаба, ~2^60 байт);
- dst (X0) — высокие VA `0xfffffc0000000000` / `0xfffffc0100000000` (ранний kernel/SPTM AS);
- цикл `while (7 < len) { *p=val; len-=8; p++ }` при таком len не завершается = **runaway**,
  а abort-векторы (0x100040) — demand-paging по мере заливки. Это НЕ медленный TCG-SHA.

Обёртка — FUN_001113a0 (bounds-checked memset): `memset(dst=x0, val=x1, len=x5)`; len приходит
из вызывающего. Значение адресного масштаба ⇒ длина посчитана как `end-start` (или взята из поля),
где одно из слагаемых пришло из **занулённой структуры**, которую должен был заполнить SEP-ответ
(inline resp[4:16] и/или OOL-nonce), — сейчас заглушка отдаёт нули.

Оговорка: при `-d cpu` дамп регистров и exec-строка чередуются, поэтому точный X2 может быть смещён
на один TB; но ПОРЯДОК величины (адрес-как-размер, мусор) однозначен во всех «чётных» входах.

### Следующий конкретный шаг
1. Найти вызывающего FUN_001113a0 (кто кладёт x5) и поле-источник длины; сверить, что оно
   происходит из ответа SEP (op3 inline или последующий op) — тогда правильный ответ убирает мусор.
2. В vr-sep-mbox.c отдавать НЕнулевой правдоподобный ответ op3 (и, если требуется, OOL-nonce на op4),
   прогнать заново и смотреть, исчез ли runaway memset (len станет вменяемым).

### ПОПРАВКА: не runaway memset, а HALT на HVC #0 (гипервызов)
Прошлый вывод («runaway memset с мусорной длиной») ОШИБОЧЕН — он опирался на смещённый дамп
`-d cpu` (регистры и exec-строка чередуются, X2 читался на TB позже). Перепроверка окнами времени:

```
T=8 : totalTB=211536 distinctTB=3073 maxPC=0x13c000 aborts=5119 sepReq=1 uart=0
T=24: totalTB=211536 distinctTB=3073 maxPC=0x13c000 aborts=5119 sepReq=1 uart=0
```
Числа T=8 и T=24 ИДЕНТИЧНЫ → выполнение доходит до точки и полностью прекращается (не медленный
memset — тот дал бы рост TB). memset'ы конечны: `FUN_00105b48` заливает регион 0x70074000 длиной
`FUN_001040cc()` = **константа 0x38c000** (~3.7 МБ), в один проход.

Последний исполненный TB = **0x103370 = `FUN_00103370` = `HVC #0`** (CallHyperVisor(0)).
После HVC — ни одного TB (даже вектора исключения) → гипервызов из EL1 не обслуживается и не
возвращается, CPU встаёт. HVC вызывается из measured-boot `FUN_0011b730` (SHA-подобная) и ДОЛЖЕН
вернуться (FUN_00103370 = обёртка `hvc #0; ret`).

Итог по стопу: барьер сейчас — **паравиртуальный HVC-интерфейс к хосту VZ**, а не SEP.
SEP-находки в силе: транспорт, мастер-таблица @0x13dd20, формат кадра, op3-хендшейк приняты —
op3 отвечает корректно, гость идёт дальше и упирается уже в HVC.

### Что делать
- Снять ABI гипервызова: x0..x7 на входе в HVC (по коду вокруг FUN_00103370 и вызывающего в
  FUN_0011b730) — что за сервис (кандидаты: измерение/лог/маппинг/консоль VZ). Реверснуть
  диспетчер HVC на стороне хоста в com.apple.Virtualization.VirtualMachine (проект vza64/vzvm).
- Реализовать в машине vresearch101 обработчик HVC (EL2 conduit): вернуть корректный результат в
  x0 и продолжить, как делает vmapple-конвейер в upstream QEMU.
- Дальше — снять следующую партию HVC/SEP-обменов трассой после того, как первый HVC начнёт возвращать.

### Уточнение: это PSCI_SYSTEM_RESET из measured-boot (осознанный boot-abort)
Машина ставит psci-conduit=HVC (vresearch101.c:262), QEMU обслуживает PSCI. Оба HVC идут из
одного места LR=0x11b7d8 (внутри FUN_0011b730, measured-boot/SHA):
- HVC#1: X0=0x84000000 = PSCI_VERSION (проба),
- HVC#2: X0=0x84000009 = PSCI_SYSTEM_RESET.
Значит гость НЕ висит и НЕ делает runaway — measured-boot `FUN_0011b730` проваливает проверку и
**сознательно ребутит** систему (reset-on-failure). totalTB не растёт, потому что reset машины у нас
не перезапускает прогон в окне timeout. Причина провала — измерение/nonce от SEP сейчас пустышки.

Связка с SEP: чтобы measured-boot прошёл, нужен КОРРЕКТНЫЙ SEP-ответ (реальный nonce/измерение),
а не заглушка. Барьер вернулся к SEP, но теперь точно локализован: FUN_0011b730 + ветка на reset.

### Следующий шаг (точный)
- Реверс FUN_0011b730 у 0x11b7xx: какое условие (сравнение хеша/статуса SEP) ведёт в reset-ветку.
- Что именно сравнивается: снять буфер измерения и ожидаемое значение (откуда берётся — из OOL SEP
  или из IMG4 манифеста). Тогда понять, какой SEP-ответ (op3 inline / op4 nonce / OOL) должен быть.

### Подтверждение reset без -d cpu (чистый метод)
Прогон `-no-reboot -no-shutdown -d exec` 15 с: rc=124 (процесс жив, CPU заморожен), ROM-вход
0x100000 исполнен РОВНО 1 раз (нет reboot-петли), последний TB = 0x103370 (HVC #0). Комбинация
`-no-reboot`(reset→shutdown) + `-no-shutdown`(не выходить) даёт именно такую заморозку ⇒ гость
инициировал **PSCI SYSTEM_RESET**. Это надёжно, без косвенного `-d cpu`.

ПОПРАВКА к прошлому: привязка HVC к LR=0x11b7d8 НЕнадёжна — `-d cpu` печатает регистры со сдвигом
на TB, x30 там левый (0x11b7d8 = возврат после `bl 0x119084`, бит-тест). Что реально знаем твёрдо:
последний TB = HVC; X0 на HVC = PSCI (0x84000000 VERSION в начале, 0x84000009 RESET на выходе).
FUN_00119084 = бит-тест 256-битной карты (bit N в [buf+0x20..+0x40], N<0x101) — часть логики, но её
связь с reset не доказана (нужен надёжный трейс).

### Надёжный метод для след. шага (без -d cpu)
Инструментировать HVC В САМОЙ машине: временно перехватить гипервызов (свой обработчик EL2/PSCI-хук в
overlay) и печатать X0..X7 + ELR_EL2 (истинный адрес возврата) при каждом HVC. Тогда:
1. увидеть ТОЧНО, откуда зовётся SYSTEM_RESET (ELR), и всю цепочку до него;
2. поймать, какая проверка (какое сравнение/бит) в measured-boot проваливается;
3. связать с конкретным SEP-ответом (op3 inline / op4 nonce / OOL), который надо отдать не нулями.
Альтернатива — поставить gdb-multiarch (нужна сеть в WSL) и bp на 0x103370 с bt.

### КОРЕНЬ: firebloom bounds-panic → PSCI_SYSTEM_RESET (HVC-логгер в машине)
Вставлен надёжный лог HVC прямо в arm_handle_psci_call (overlay/target/arm/tcg/psci.c: печать
X0..X7 + LR + PC/ELR). Прогон дал ТОЧНО:
```
HVC/PSCI x0=0x84000000 ... x6=0x14690b x7=0xa0 lr=0x11d6ac pc=0x103374 el=1   (PSCI_VERSION)
HVC/PSCI x0=0x84000009 ... x7=0xa0            lr=0x11d6ac pc=0x103374 el=1   (PSCI_SYSTEM_RESET)
```
Оба HVC из lr=0x11d6ac — это reboot-рутина в хвосте FUN_0011b730 (Ghidra склеила блоки в одну функцию).
Аргументы указывают на панику: x6=0x14690b = ROM-строка "main", рядом 0x146900="...loom_panic"
(**firebloom_panic** — Apple memory-safety), формат 0x1468eb = " (%zu < %zu)\n" (assert границ).

Вывод (корень): boot-abort = **firebloom bounds-check паника в main** ("(%zu < %zu)"), т.е. какое-то
поле пришло из занулённой структуры → указатель/длина вне [lo,hi) → firebloom_panic → reboot.
Всюду в AVPBooter стоят проверки `lo <= p && p < hi` с FUN_0012ea7c() на провале — это та же
firebloom-инструментация. Наши SEP-ответы пустышки ⇒ поле ноль ⇒ проверка падает.

### Следующий шаг
- Снять, КАКАЯ проверка первой падает: логировать в машине обращения к FUN_0012ea7c/firebloom_panic
  сайтам (или bp), поймать первый bounds-fail ДО reboot и его адрес.
- Связать поле с конкретным SEP-ответом (op3 inline resp[4:16] / op4 20-B nonce / OOL) и отдать его
  не нулями в vr-sep-mbox.c; проверить, что firebloom-паника уходит.

### Причина reboot = код 0xa0 (firebloom bounds), диспетчер FUN_0011b730
Реальная ветка на reboot (дизасм):
```
0x11b994: sub w16, w19, #0xc0 ; 0x11b998: cmp w16,#0x21 ; 0x11b99c: b.hi 0x11bb78
0x11bb78: cmp w19, #0xa0      ; 0x11bb7c: b.eq 0x11d690  (reboot: PSCI_VERSION+SYSTEM_RESET)
```
FUN_0011b730 — это ДИСПЕТЧЕР статусов (switch по w19-0xc0 через jump-table @0x11e5b8), а НЕ SHA
(Ghidra склеила блоки). w19 = x7-аргумент функции (0x11b754: mov x19,x7). В HVC-логе x7=0xa0 →
диспетчер получает код **0xa0 (=160)** и уводит в reboot. Это firebloom-abort («firebloom_panic»,
"main", "(%zu < %zu)") — bounds-check провалился, reason=0xa0.

Итог: boot-abort — детерминированная реакция на **код ошибки 0xa0**, пришедший в FUN_0011b730.
Осталось найти ИСТОЧНИК 0xa0 (кто вызывает FUN_0011b730 с x7=0xa0 — Ghidra не видит, tail-call/ptr):
это точка, где реально падает bounds-check из-за занулённого SEP-поля.

### Следующий шаг
- Найти источник 0xa0: трасса TB прямо перед первым входом в FUN_0011b730 (entry 0x11b730) —
  вызывающий и что он проверял. Либо залогировать в машине вход 0x11b730 с dump x0..x7.
- Оттуда — к конкретному SEP-полю; отдать его не нулями в vr-sep-mbox.c и проверить исчезновение 0xa0.
