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
