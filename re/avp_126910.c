// ===== 0x00126910 -> FUN_00126910 @ 00126910

undefined8 FUN_00126910(ulong param_1,ulong param_2,ulong param_3)

{
  if (param_2 <= param_1 && param_1 < param_3) {
    return *(undefined8 *)(param_1 + 0x20);
  }
                    /* WARNING: Subroutine does not return */
  FUN_0012ea7c();
}


