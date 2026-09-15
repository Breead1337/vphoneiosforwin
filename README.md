# vphoneiosforwin

Попытка запустить iOS-гостя (как в [vphone-cli](https://github.com/Lakr233/vphone) от Lakr233)
на **Windows x86-64**. Прямой порт невозможен: vphone работает через Apple **Virtualization.framework
(VZ)** — это аппаратная виртуализация на Apple Silicon, её на x86 нет. Поэтому путь другой —
**эмулятор**: своя QEMU-машина `vresearch101` на базе форка **Inferno** (в нём уже есть Apple
GXF/SPRR/PAC в TCG), которая грузит настоящую boot-цепочку `vresearch1` из Apple cloudOS.

> ⚠️ Это **ресёрч**, а не продукт. На сегодня загружается настоящий `AVPBooter` Apple на x86 и
> достигнут SEP-хендшейк — до экрана iOS отсюда месяцы/фронтир. Подробности пути и ограничений —
> в [`NOTES.md`](NOTES.md).

## С чего начать
Читать в порядке: **[`CREATE.md`](CREATE.md)** (что и как делали, что качали и откуда, как собрать и
запустить) → [`NOTES.md`](NOTES.md) (журнал вех) → [`re/SEP_MAILBOX.md`](re/SEP_MAILBOX.md) (реверс
SEP-мейлбокса, текущий барьер).

## Что в репозитории
| Путь | Что это |
|------|---------|
| `overlay/` | Наш код поверх Inferno: машина `vresearch101`, модель SEP-мейлбокса, bdif/aes |
| `re/` | Реверс-инжиниринг: карта SEP-мейлбокса + декомпил-выжимки из AVPBooter |
| `tools/` | Скрипты сборки/запуска/трассировки (WSL) + Ghidra headless |
| `NOTES.md` | Журнал: что сделано, следующий шаг, стратегические выводы |

## Чего в репозитории НЕТ (и почему)
Прошивки Apple и вендор-бинари **не выкладываются** — это проприетарные бинарники Apple (копирайт),
да и весят десятки ГБ. Каждый участник качает их сам (легально, со своим Apple ID где нужно) —
пошагово в [`CREATE.md`](CREATE.md):

- `fw/` — cloudOS 26.4 IPSW, macOS 26.6.2, `AVPBooter`/`AVPSEPBooter`, распакованные iBoot/SEP/kernel;
- `src/` — клон форка Inferno (QEMU, GPL) — берётся отдельно, `overlay/` накатывается сверху;
- `tools/ipsw.exe`, `tools/ghidra_*_PUBLIC/` — сторонние инструменты (blacktop/ipsw, Ghidra).

## Благодарности
[Lakr233/vphone](https://github.com/Lakr233/vphone) · форк Inferno (ChefKiss, Apple-silicon в TCG) ·
[blacktop/ipsw](https://github.com/blacktop/ipsw) · Ghidra.
